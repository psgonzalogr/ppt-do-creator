#!/usr/bin/env python3
"""Explora las presentaciones de referencia para reutilizar sus diapositivas.

Uso:
    python3 scripts/catalogo.py referencia/ejemplos_completos/Retroalimentacion_Efectiva_DO.html
        → lista numerada: título, clases de la diapositiva, pasos (data-steps) y primeras palabras
    python3 scripts/catalogo.py referencia/ejemplos_completos/Retroalimentacion_Efectiva_DO.html 7
        → imprime el HTML de la diapositiva 7 (con las imágenes incrustadas abreviadas) listo para
          copiarlo a diapositivas.html y cambiar los textos

El CSS de todas esas diapositivas ya viene en motor/motor.html, así que el marcado copiado se ve igual.
Las fotos y documentos de la diapositiva copiada NO se copian: reemplázalos por {{img:archivo}} propios.
"""
import html, re, sys


def secciones(t):
    i0 = t.index('<div id="orbs"></div>') if '<div id="orbs"></div>' in t else 0
    i1 = t.index('<div id="progress">') if '<div id="progress">' in t else len(t)
    zona = t[i0:i1]
    return re.findall(r'<section class="slide.*?</section>', zona, re.S)


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    t = open(sys.argv[1], encoding='utf8').read()
    sec = secciones(t)
    if len(sys.argv) == 2:
        for i, s in enumerate(sec, 1):
            cab = re.match(r'<section class="slide([^"]*)" data-title="([^"]*)"([^>]*)>', s)
            clases, titulo, resto = cab.group(1).strip(), html.unescape(cab.group(2)), cab.group(3)
            pasos = re.search(r'data-steps="(\d+)"', resto)
            texto = re.sub(r'<aside class="notes">.*?</aside>', '', s, flags=re.S)
            texto = re.sub(r'<svg.*?</svg>', ' ', texto, flags=re.S)
            texto = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', texto)).split())
            print(f'{i:>3}. {titulo}  [{clases}]' + (f' pasos={pasos.group(1)}' if pasos else '') + f'\n     {texto[:110]}')
        return
    n = int(sys.argv[2])
    s = sec[n - 1]
    s = re.sub(r'<aside class="notes">.*?</aside>\n?', '', s, flags=re.S)
    s = re.sub(r'data:(image|font)/[\w+.\-]+;base64,[A-Za-z0-9+/=]+', '{{img:ARCHIVO}}', s)
    print(s)


if __name__ == '__main__':
    main()
