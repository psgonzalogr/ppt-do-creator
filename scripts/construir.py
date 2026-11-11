#!/usr/bin/env python3
"""Construye una presentación DO (HTML autocontenido + PDF) desde una carpeta de proyecto.

Uso:
    python3 scripts/construir.py ejemplo
    python3 scripts/construir.py mi_presentacion --salida salida --sin-pdf

La carpeta de proyecto contiene:
    deck.json            nombre, pie, canal, archivo
    diapositivas.html    las <section class="slide" data-title="..."> de la presentación
    notas.json           {"Título de la diapositiva": ["idea 1", "idea 2"], ...}
    estilos.css          (opcional) CSS propio de esta presentación
    imagenes/            (opcional) fotos y documentos usados con {{img:archivo.jpg}}

Marcadores que se resuelven en diapositivas.html y estilos.css:
    {{icon:nombre}}       ícono Lucide en línea (assets/iconos/nombre.svg)
    {{iconinner:nombre}}  solo el contenido del ícono, para usarlo dentro de un <svg> propio
    {{img:archivo}}       imagen incrustada como data URI (busca en imagenes/ y luego en assets/logos/)
"""
import argparse, base64, html, json, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTES = os.path.join(RAIZ, 'assets', 'fuentes')
ICONOS = os.path.join(RAIZ, 'assets', 'iconos')
LOGOS = os.path.join(RAIZ, 'assets', 'logos')

MIME = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'svg': 'image/svg+xml',
        'webp': 'image/webp', 'gif': 'image/gif'}


def b64(ruta, mime):
    with open(ruta, 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode()


def bloque_fuentes():
    css = ''
    for w in (400, 500, 600, 700, 800, 900):
        css += (f"@font-face{{font-family:Montserrat;font-style:normal;font-weight:{w};font-display:block;"
                f"src:url({b64(os.path.join(FUENTES, f'montserrat-latin-{w}-normal.woff2'), 'font/woff2')}) format('woff2')}}\n")
    for w in (300, 400, 600):
        css += (f"@font-face{{font-family:Montserrat;font-style:italic;font-weight:{w};font-display:block;"
                f"src:url({b64(os.path.join(FUENTES, f'montserrat-latin-{w}-italic.woff2'), 'font/woff2')}) format('woff2')}}\n")
    for w in (400, 600, 700):
        css += (f"@font-face{{font-family:'Source Sans 3';font-style:normal;font-weight:{w};font-display:block;"
                f"src:url({b64(os.path.join(FUENTES, f'source-sans-3-latin-{w}-normal.woff2'), 'font/woff2')}) format('woff2')}}\n")
    return css


def leer_icono(nombre):
    ruta = os.path.join(ICONOS, nombre + '.svg')
    if not os.path.exists(ruta):
        sugeridos = [f[:-4] for f in os.listdir(ICONOS) if f.endswith('.svg') and nombre.split('-')[0] in f][:8]
        raise SystemExit(f'ERROR: no existe el ícono «{nombre}». Parecidos: {", ".join(sugeridos) or "(ninguno)"}')
    return re.sub(r'<!--.*?-->', '', open(ruta, encoding='utf8').read(), flags=re.S).strip()


def resolver(texto, carpeta_img, cache_img):
    def icono(m):
        return re.sub(r'\s+', ' ', leer_icono(m.group(1)))

    def icono_interno(m):
        s = leer_icono(m.group(1))
        interno = re.search(r'>\s*(.*)</svg>', s.split('<svg', 1)[1], re.S).group(1)
        return ('<g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
                'stroke-linejoin="round">' + re.sub(r'\s+', ' ', interno) + '</g>')

    def imagen(m):
        n = m.group(1)
        if n not in cache_img:
            for base in (carpeta_img, LOGOS):
                ruta = os.path.join(base, n)
                if os.path.exists(ruta):
                    cache_img[n] = b64(ruta, MIME.get(n.rsplit('.', 1)[-1].lower(), 'application/octet-stream'))
                    break
            else:
                raise SystemExit(f'ERROR: no encuentro la imagen «{n}» ni en imagenes/ ni en assets/logos/')
        return cache_img[n]

    texto = re.sub(r'\{\{iconinner:([\w-]+)\}\}', icono_interno, texto)
    texto = re.sub(r'\{\{icon:([\w-]+)\}\}', icono, texto)
    texto = re.sub(r'\{\{img:([\w.\-]+)\}\}', imagen, texto)
    return texto


def inyectar_notas(t, notas):
    partes = re.split(r'(?=<section class="slide)', t)
    faltan, usadas, res = [], set(), []
    for p in partes:
        mm = re.match(r'<section class="slide[^"]*" data-title="([^"]+)"', p)
        if mm:
            clave = html.unescape(mm.group(1))
            if clave not in notas:
                faltan.append(clave)
            usadas.add(clave)
            lis = ''.join('<li>' + x + '</li>' for x in notas.get(clave, []))
            k = p.index('</section>')
            p = p[:k] + '<aside class="notes"><ul>' + lis + '</ul></aside>\n' + p[k:]
        res.append(p)
    sobran = [k for k in notas if k not in usadas]
    return ''.join(res), faltan, sobran


def optimizar_imagenes(carpeta):
    try:
        from PIL import Image
    except ImportError:
        print('AVISO: Pillow no está instalado; no se optimizaron las imágenes (pip install pillow).')
        return
    for n in sorted(os.listdir(carpeta)):
        if not n.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        ruta = os.path.join(carpeta, n)
        im = Image.open(ruta)
        if im.width > 1700 or os.path.getsize(ruta) > 600_000:
            im.thumbnail((1700, 1700))
            if n.lower().endswith('.png') and im.mode in ('RGBA', 'LA', 'P'):
                im.save(ruta, optimize=True)
            else:
                im.convert('RGB').save(ruta, quality=80, optimize=True)
            print(f'  imagen optimizada: {n} → {os.path.getsize(ruta) // 1024} KB')


def pdf_desde_html(ruta_html, ruta_pdf):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1920, 'height': 1080})
        errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: errores.append(m.text) if m.type == 'error' else None)
        pg.goto('file://' + os.path.abspath(ruta_html) + '?print=1')
        pg.wait_for_timeout(800)
        pg.evaluate('document.fonts.ready')
        n = pg.evaluate('document.querySelectorAll(".slide").length')
        pg.pdf(path=ruta_pdf, width='1920px', height='1080px', print_background=True, prefer_css_page_size=True)
        b.close()
    return n, errores


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('proyecto', help='carpeta del proyecto (ej. ejemplo)')
    ap.add_argument('--salida', help='carpeta de salida (por defecto <proyecto>/salida)')
    ap.add_argument('--sin-pdf', action='store_true', help='solo genera el HTML')
    ap.add_argument('--optimizar', action='store_true', help='reduce las imágenes de imagenes/ (máx. 1700 px, JPEG 80)')
    a = ap.parse_args()

    pr = os.path.abspath(a.proyecto)
    salida = os.path.abspath(a.salida or os.path.join(pr, 'salida'))
    cfg = json.load(open(os.path.join(pr, 'deck.json'), encoding='utf8'))
    for k in ('nombre', 'canal', 'archivo'):
        if not cfg.get(k):
            raise SystemExit(f'ERROR: deck.json necesita el campo «{k}»')
    cfg.setdefault('pie', cfg['nombre'])
    if not re.fullmatch(r'[A-Za-z0-9_\-]+', cfg['archivo']):
        raise SystemExit('ERROR: «archivo» en deck.json solo admite letras, números, guion y guion bajo (sin espacios ni tildes)')
    carpeta_img = os.path.join(pr, 'imagenes')
    if a.optimizar and os.path.isdir(carpeta_img):
        optimizar_imagenes(carpeta_img)

    motor = open(os.path.join(RAIZ, 'motor', 'motor.html'), encoding='utf8').read()
    slides = open(os.path.join(pr, 'diapositivas.html'), encoding='utf8').read()
    if not re.search(r'<section class="slide[^"]*" data-title="', slides):
        raise SystemExit('ERROR: diapositivas.html no contiene ninguna <section class="slide" data-title="...">')
    ruta_css = os.path.join(pr, 'estilos.css')
    extra = open(ruta_css, encoding='utf8').read() if os.path.exists(ruta_css) else ''
    ruta_notas = os.path.join(pr, 'notas.json')
    notas = json.load(open(ruta_notas, encoding='utf8')) if os.path.exists(ruta_notas) else {}

    cache = {}
    logos = ('<div class="logos"><img src="{{img:Hospital_Regional_Antofagasta.png}}" alt="Hospital Regional de Antofagasta">'
             '<span class="sep"></span><img src="{{img:DO_vertical_color.png}}" alt="Desarrollo Organizacional"></div>')
    logos = resolver(logos, carpeta_img, cache).replace('\\', '\\\\').replace("'", "\\'")

    t = (motor.replace('{{DIAPOSITIVAS}}', slides).replace('{{ESTILOS_EXTRA}}', extra)
         .replace('{{fonts}}', bloque_fuentes()))
    t = t.replace('{{logos}}', logos)
    t = t.replace('{{NOMBRE}}', html.escape(cfg['nombre'], quote=False)).replace('{{PIE}}', html.escape(cfg['pie'], quote=False))
    t = t.replace('{{CANAL}}', cfg['canal'])
    t = resolver(t, carpeta_img, cache)
    t, faltan, sobran = inyectar_notas(t, notas)

    pendientes = sorted(set(re.findall(r'\{\{[^}]*\}\}', t)))
    if pendientes:
        raise SystemExit('ERROR: marcadores sin resolver: ' + ', '.join(pendientes[:8]))
    if re.search(r'https?://[^"\')\s]+\.(?:woff2?|ttf|css|js)\b', t):
        print('AVISO: hay recursos externos (CDN); la presentación debe funcionar sin internet.')

    os.makedirs(salida, exist_ok=True)
    ruta_html = os.path.join(salida, cfg['archivo'] + '.html')
    open(ruta_html, 'w', encoding='utf8').write(t)
    n = len(re.findall(r'<section class="slide', t))
    print(f'HTML: {ruta_html}  ({os.path.getsize(ruta_html) // 1024} KB, {n} diapositivas)')
    if faltan:
        print('AVISO: diapositivas sin notas del presentador: ' + '; '.join(faltan))
    if sobran:
        print('AVISO: notas.json tiene títulos que no coinciden con ninguna diapositiva: ' + '; '.join(sobran))

    if not a.sin_pdf:
        ruta_pdf = os.path.join(salida, cfg['archivo'] + '.pdf')
        try:
            total, errores = pdf_desde_html(ruta_html, ruta_pdf)
        except Exception as e:  # Playwright o Chromium no disponibles
            print(f'AVISO: no se pudo generar el PDF automáticamente ({type(e).__name__}: {str(e)[:120]}).')
            print('  Instala las dependencias: pip install playwright && playwright install chromium')
            print('  o genera el PDF a mano: abre el HTML con «?print=1» al final de la dirección, Ctrl+P, '
                  'destino «Guardar como PDF», márgenes «Ninguno» y activa «Gráficos de fondo».')
            return
        print(f'PDF:  {ruta_pdf}  ({os.path.getsize(ruta_pdf) // 1024} KB)')
        if errores:
            print('AVISO: errores en la consola del navegador:', errores[:5])
        if total != n:
            print(f'AVISO: el navegador contó {total} diapositivas y el archivo declara {n}')
    print('Listo. Ejecuta scripts/verificar.py para revisar el resultado.')


if __name__ == '__main__':
    main()
