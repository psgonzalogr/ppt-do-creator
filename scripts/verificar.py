#!/usr/bin/env python3
"""Control de calidad de una presentación DO ya construida.

Uso:
    python3 scripts/verificar.py ejemplo/salida/Plantilla_Ejemplo_DO.html

Revisa y reporta:
  1. Errores de consola del navegador.
  2. Navegación: clic por mitades, número + Enter, tecla H, pasos (data-steps).
  3. Modo PDF: ninguna diapositiva debe sobresalir del escenario de 1920 × 1080.
  4. Títulos (h1/h2) con la regla de mayúsculas de DO (aviso, revisar a mano).
  5. Texto con tamaño menor a 19 px (aviso).
  6. PDF: número de páginas igual al de diapositivas (si existe el .pdf junto al .html).
  7. Capturas de cada diapositiva en <html>_capturas/ y una hoja de contactos (contacto_N.png)
     para revisarlas a simple vista.
Código de salida 1 si hay errores graves.
"""
import os, re, sys
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    raise SystemExit('Falta Playwright: pip install playwright && playwright install chromium')

CONECTORES = {'y', 'o', 'e', 'u', 'de', 'del', 'la', 'las', 'el', 'los', 'lo', 'para', 'en', 'un', 'una', 'a', 'al', 'con',
              'por', 'su', 'sus', 'que', 'se', 'sin', 'sobre', 'entre', 'desde', 'hacia', 'como', 'ni'}


def titulo_sospechoso(txt):
    txt = ' '.join(txt.split())
    if not txt or txt.startswith('¿') or txt.endswith('?'):
        return []  # las preguntas van en tipo oración
    mal = []
    for i, w in enumerate(txt.split(' ')):
        base = re.sub(r'^[«"“(¡¿]+|[»"”).,:;!?]+$', '', w)
        if not base or not base[0].isalpha():
            continue
        if i == 0 and base[0].islower():
            mal.append(base)
        elif i > 0 and base[0].islower() and base.lower() not in CONECTORES:
            mal.append(base)
    return mal


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    ruta = os.path.abspath(sys.argv[1])
    base = ruta[:-5] if ruta.endswith('.html') else ruta
    carpeta_cap = base + '_capturas'
    os.makedirs(carpeta_cap, exist_ok=True)
    graves, avisos = [], []

    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception as e:
            raise SystemExit('No hay navegador Chromium disponible para verificar '
                             f'({type(e).__name__}). Revisa a mano: abre el HTML en Chrome, recorre todas las '
                             'diapositivas y comprueba títulos, textos y que nada se salga de la diapositiva.')
        # ---- 1-2. consola y navegación (vista normal) -------------------------------------
        pg = b.new_page(viewport={'width': 1280, 'height': 720})
        errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: errores.append(m.text) if m.type == 'error' else None)
        pg.goto('file://' + ruta)
        pg.wait_for_timeout(900)
        total = pg.evaluate('document.querySelectorAll(".slide").length')
        h = lambda: pg.evaluate('location.hash')
        pg.mouse.click(1000, 300); pg.wait_for_timeout(250); a = h()
        pg.mouse.click(1000, 300); pg.wait_for_timeout(250); a2 = h()
        pg.mouse.click(200, 300); pg.wait_for_timeout(250); bb = h()
        if total >= 3:
            n = min(total, 3)
            pg.keyboard.press(str(n)); pg.wait_for_timeout(300)
            pg.keyboard.press('Enter'); pg.wait_for_timeout(500); c = h()
            if c != f'#{n}':
                graves.append(f'Ir a la diapositiva {n} con número + Enter dejó la URL en «{c}»')
        if a == a2 and total > 1:
            avisos.append(f'Clic en la mitad derecha no avanzó ({a} → {a2}); puede ser normal si la diapositiva tiene pasos (data-steps)')
        if bb != a and a != a2:
            graves.append(f'Clic en la mitad izquierda no retrocedió ({a2} → {bb}, se esperaba {a})')
        pg.keyboard.press('h'); pg.wait_for_timeout(300)
        if not pg.evaluate('!!document.getElementById("help") && getComputedStyle(document.getElementById("help")).opacity !== "0"'):
            avisos.append('La ayuda de atajos (H) no parece visible')
        for e in errores:
            graves.append('Consola del navegador: ' + e)
        pg.close()

        # ---- 3-5. modo PDF -------------------------------------------------------------------
        pg = b.new_page(viewport={'width': 1920, 'height': 1080})
        pg.goto('file://' + ruta + '?print=1')
        pg.wait_for_timeout(900)
        pg.evaluate('document.fonts.ready')
        dim = pg.evaluate('''() => ({sw: document.documentElement.scrollWidth, sh: document.documentElement.scrollHeight,
            slides: [...document.querySelectorAll('.slide')].map(s => { const r = s.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; })})''')
        if dim['sw'] > 1920:
            graves.append(f'PDF: el contenido ancho es {dim["sw"]} px (>1920): algún elemento sobresale y achicará el PDF')
        for i, (w, hh) in enumerate(dim['slides']):
            if (w, hh) != (1920, 1080):
                graves.append(f'Diapositiva {i + 1}: mide {w}×{hh} en modo PDF (debe ser 1920×1080)')
        # elementos fuera del escenario
        fuera = pg.evaluate('''() => { const out = [];
            document.querySelectorAll('.slide').forEach((s, i) => { const sr = s.getBoundingClientRect();
              s.querySelectorAll('*').forEach(el => { if (el.closest('svg') && el.tagName !== 'svg') return;
                if (el.closest('.notes') || el.closest('.deco') || el.classList.contains('deco')) return;
                const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 2) return;
                if (r.right > sr.right + 2 || r.bottom > sr.bottom + 2 || r.left < sr.left - 2 || r.top < sr.top - 2) {
                  out.push([i + 1, el.tagName.toLowerCase() + (el.className && el.className.baseVal === undefined ? '.' + String(el.className).split(' ')[0] : '')]); } }); });
            return out.slice(0, 40); }''')
        vistos = set()
        for i, nombre in fuera:
            if (i, nombre) not in vistos:
                vistos.add((i, nombre))
                avisos.append(f'Diapositiva {i}: «{nombre}» sobresale del borde (si es decorativo, debe ir dentro de un <svg> de 1920×1080 que lo recorte)')
        titulos = pg.evaluate('''() => [...document.querySelectorAll('.slide')].map((s, i) =>
            [...s.querySelectorAll('h1,h2')].map(h => { const sp = [...h.querySelectorAll(':scope > span')]; return [i + 1, sp.length ? sp.map(x => x.textContent).join(' ') : h.textContent]; }))''')
        for grupo in titulos:
            for i, txt in grupo:
                mal = titulo_sospechoso(txt)
                if mal:
                    avisos.append(f'Diapositiva {i}: título «{" ".join(txt.split())}» tiene palabras en minúscula inicial que no son conectores: {", ".join(mal)}')
        chicos = pg.evaluate('''() => { const out = []; document.querySelectorAll('.slide').forEach((s, i) => {
            s.querySelectorAll('p,li,span,div,b,td,h3,h4,small').forEach(el => {
              if (el.closest('.notes') || el.closest('.logos') || el.closest('.foot') || el.closest('.stephint') || el.closest('svg')) return;
              const t = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join('');
              if (!t) return; const fs = parseFloat(getComputedStyle(el).fontSize);
              if (fs < 19) out.push([i + 1, Math.round(fs), t.slice(0, 40)]); }); }); return out.slice(0, 30); }''')
        for i, fs, t in chicos:
            avisos.append(f'Diapositiva {i}: texto de {fs} px («{t}»); el mínimo recomendado es 19 px')
        # capturas
        rutas = []
        for i, el in enumerate(pg.query_selector_all('.slide')):
            r = os.path.join(carpeta_cap, f's{i + 1:02d}.png')
            el.screenshot(path=r)
            rutas.append(r)
        pg.close()
        b.close()

    # ---- 6. PDF -----------------------------------------------------------------------------
    ruta_pdf = base + '.pdf'
    if os.path.exists(ruta_pdf):
        datos = open(ruta_pdf, 'rb').read()
        paginas = len(re.findall(rb'/Type\s*/Page[^s]', datos))
        if paginas != total:
            graves.append(f'PDF: tiene {paginas} páginas y la presentación {total} diapositivas')
        caja = re.search(rb'/MediaBox\s*\[\s*0\s+0\s+([\d.]+)\s+([\d.]+)', datos)
        if caja:
            w, hh = float(caja.group(1)), float(caja.group(2))
            if abs(w / hh - 16 / 9) > 0.01:
                graves.append(f'PDF: proporción {w:.0f}×{hh:.0f} (debe ser 16:9)')
        print(f'PDF: {paginas} páginas, {os.path.getsize(ruta_pdf) // 1024} KB')
    else:
        avisos.append('No encontré el PDF junto al HTML; no se verificó')

    # ---- 7. hoja de contactos -----------------------------------------------------------------
    try:
        from PIL import Image
        por_hoja, cols = 6, 2
        for k in range(0, len(rutas), por_hoja):
            lote = rutas[k:k + por_hoja]
            tw, th = 960, 540
            filas = (len(lote) + cols - 1) // cols
            hoja = Image.new('RGB', (cols * tw, filas * th), 'white')
            for j, r in enumerate(lote):
                im = Image.open(r).convert('RGB').resize((tw, th))
                hoja.paste(im, ((j % cols) * tw, (j // cols) * th))
            hoja.save(os.path.join(carpeta_cap, f'contacto_{k // por_hoja + 1}.png'))
    except ImportError:
        avisos.append('Pillow no está instalado: no se generó la hoja de contactos (pip install pillow)')

    print(f'Diapositivas: {total}. Capturas en {carpeta_cap}')
    for g in graves:
        print('ERROR :', g)
    for av in avisos:
        print('AVISO :', av)
    if not graves:
        print('Sin errores graves. Revisa las capturas diapositiva por diapositiva antes de entregar.')
    sys.exit(1 if graves else 0)


if __name__ == '__main__':
    main()
