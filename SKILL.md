---
name: ppt-do-creator
description: Crea presentaciones animadas del Departamento de Desarrollo Organizacional (DO) del Hospital Regional de Antofagasta con la línea gráfica oficial de DO, y entrega un HTML autocontenido y un PDF 16:9. Úsala cuando pidan una presentación, ppt, diapositivas o charla de DO/HRA, o convertir un PowerPoint o un texto al formato DO. No publica nada en ppt.do-hra.cl.
---

# Presentaciones DO (HTML animado + PDF)

Convierte el contenido que entregue la persona (un PowerPoint, un PDF, un Word, apuntes o una idea) en una presentación con la identidad visual de DO. El resultado son **dos archivos**: `Nombre.html` (un solo archivo, funciona sin internet, con vista del presentador) y `Nombre.pdf` (una página por diapositiva, 1920 × 1080).

## Límite importante

**Esta skill no publica en ppt.do-hra.cl.** Ese sitio lo administra la Jefatura de DO. Entrega siempre el HTML y el PDF a la persona; si quiere publicarla, que se los envíe a la Jefatura. No intentes subir, desplegar ni hacer commits en otros repositorios.

## Qué contiene esta carpeta

| Ruta | Para qué sirve |
|---|---|
| `motor/motor.html` | Motor completo: CSS de todos los componentes, navegación, barra inferior, vista del presentador, modo PDF. **No se edita.** |
| `scripts/construir.py` | Arma el HTML (y el PDF) desde una carpeta de proyecto. |
| `scripts/verificar.py` | Control de calidad automático y capturas de cada diapositiva. |
| `scripts/catalogo.py` | Lista las diapositivas de las presentaciones de referencia y extrae el marcado de una para reutilizarlo. |
| `ejemplo/` | Proyecto de ejemplo (12 diapositivas). **Copia esta carpeta** para empezar. |
| `referencia/ejemplos_completos/` | Dos presentaciones reales completas (27 y 36 diapositivas): fuente de composiciones. |
| `referencia/Prompt_PPT_a_HTML_DO.md` | Especificación completa del diseño y del motor. Léela si dudas de una regla. |
| `referencia/componentes.md` | Guía rápida de clases, animaciones, pasos y errores frecuentes. **Léela antes de escribir diapositivas.** |
| `assets/` | Logos, fuentes (Montserrat y Source Sans 3) e íconos Lucide. |

## Flujo de trabajo

1. **Preparar el entorno** (una vez): `pip install playwright pillow && playwright install chromium`. Si no se puede instalar, igual se construye el HTML y el PDF se saca a mano (ver README).
2. **Reunir los datos.** Pregunta solo lo que falte y cambie el resultado: nombre de la presentación, curso o módulo, imágenes que deben mantenerse, diapositivas que necesitan una explicación gráfica, si agregar diapositiva de objetivo. Si la persona ya dio contexto, no repitas preguntas.
3. **Leer todo el contenido** de los archivos adjuntos (`python-pptx` para .pptx; si hay PDF, mira también cómo se ve cada página).
4. **Planificar diapositiva por diapositiva** antes de escribir HTML: qué dice, qué composición usa y qué se mueve. Busca composiciones parecidas: `python3 scripts/catalogo.py referencia/ejemplos_completos/Retroalimentacion_Efectiva_DO.html` y luego `… 7` para ver el marcado de la diapositiva 7.
5. **Crear el proyecto:** copia `ejemplo/` a una carpeta nueva (por ejemplo `mi_presentacion/`), borra sus diapositivas y notas, y edita:
   - `deck.json`: `nombre` (título completo), `pie` (versión corta para el pie de página, máx. ~45 caracteres), `canal` (identificador único, minúsculas y guiones: `do-hra-mi-presentacion`), `archivo` (nombre de los archivos, sin espacios ni tildes).
   - `diapositivas.html`: las `<section class="slide" data-title="...">`.
   - `notas.json`: una lista de 2 a 4 ideas por diapositiva, con la clave igual al `data-title`.
   - `estilos.css`: CSS propio (opcional). `imagenes/`: fotos y documentos.
6. **Construir:** `python3 scripts/construir.py mi_presentacion` (usa `--optimizar` si hay fotos pesadas).
7. **Verificar:** `python3 scripts/verificar.py mi_presentacion/salida/Nombre.html`. Abre `contacto_1.png`, `contacto_2.png`… y luego cada `sNN.png` con el visor de imágenes: nada cortado, superpuesto, ilegible ni fuera de la diapositiva. Corrige, reconstruye y repite hasta que no haya errores graves ni avisos sin explicación.
8. **Entregar** el `.html` y el `.pdf` (envíalos como archivos) con un informe breve: qué diapositivas son diagramas animados y qué hace cada uno, los cambios de contenido que conviene revisar y los pendientes.

## Reglas de contenido (no negociables)

- Puedes **redactar mejor, pero no cambiar el contenido**: no inventes ideas, cifras, leyes, nombres ni ejemplos que no estén en el material. Todo rótulo que agregues debe resumir lo que ya existe, y lo informas.
- Español formal institucional de Chile, sin relleno ni frases de IA («cabe destacar», «en este sentido», «es fundamental»). Lenguaje inclusivo institucional: «las y los funcionarios».
- **Títulos en mayúscula inicial en cada palabra, salvo conectores** (y, o, de, del, la, las, el, los, para, en, un, una, a, con, por, su, que). **Las preguntas van en tipo oración:** «¿Qué es un líder?». Los rótulos superiores (`eyebrow`) los pasa a mayúsculas el CSS.
- Texto **justificado** en párrafos (`text-align: justify; text-align-last: left`), salvo en columnas angostas (menos de ~45 caracteres por línea), que van a la izquierda. **Nunca cortes palabras con guion** (`hyphens: manual`).
- Si el original tiene incoherencias, unifícalas y repórtalas. Mantén citas y autores. Copia exactos los datos de contacto.
- No incluyas datos personales ni información confidencial que la persona no haya entregado para este fin. Nunca pongas contraseñas, tokens ni claves.

## Diseño (resumen)

- Escenario de 1920 × 1080 px. Paleta: navy `#0B2D4F`, blue `#2462AC`, ocean `#0E7AC2`, teal `#0E6E92`, cyan `#00A9E6`, aqua `#33B6C2`, amber `#F2A33A` (solo para contrastar), fondo `#F3F7FA`. Ya son variables CSS (`var(--navy)`, etc.).
- Títulos en Montserrat y texto en Source Sans 3. Tamaños: título 56–66 px, párrafo 26–31 px, tarjetas 22–27 px; **nunca menos de 19 px**.
- Los logos del Hospital y de DO, el número «07 / 27» y el pie con el nombre salen **automáticamente** en todas las diapositivas. Logos adicionales (Calidad de Vida, SOGA) se usan con `{{img:Calidad_de_Vida.png}}`.
- **Cada diapositiva tiene una composición pensada para su contenido y al menos un elemento en movimiento continuo.** Cuando el contenido describe un proceso, una relación o una estructura, hazlo diagrama animado en vez de lista. Evita el «todo centrado» y las listas con viñetas.
- Íconos: `{{icon:nombre}}` (Lucide, 1.500 disponibles en `assets/iconos/`). Si el nombre no existe, el constructor sugiere parecidos.
- Imágenes: `{{img:archivo.jpg}}` busca en `imagenes/` del proyecto y luego en `assets/logos/`. Fotos en JPEG de ~1000–1700 px de ancho.

## Anatomía mínima de una diapositiva

```html
<section class="slide" data-title="Título de la Diapositiva" data-steps="2">
  <div class="grid-dots" style="right:110px;top:84px"></div>
  <div class="pad">
    <div class="eyebrow a u">Módulo 01</div>
    <h2 class="a u" style="--i:1">Título <em>Destacado</em></h2>
    <div class="card a u" style="--i:3"><div class="iconbox">{{icon:users}}</div><p>Texto…</p></div>
    <div class="card a u" data-step="1" style="--i:4">Aparece con el primer avance</div>
  </div>
</section>
```

Fondo oscuro: `class="slide dark …"`. Detalle de animaciones (`a u l r p f d g gx`, `--i`), pasos, anillos decorativos, líneas que se dibujan y puntos que viajan: `referencia/componentes.md`.

## Errores frecuentes (evítalos)

1. Elemento con animación de entrada (`.a`) y animación continua propia en la misma regla: una anula a la otra y queda invisible. Pon el bucle en un hijo.
2. Clases propias que chocan con las del motor: **usa siempre el prefijo `mi-`** en `estilos.css` y en el marcado.
3. Texto que se sale de círculos, fichas o tarjetas; justificado con espacios enormes en columnas angostas.
4. Diagramas SVG con `viewBox` distinto del tamaño real del contenedor: las líneas quedan «corridas». Fija el tamaño del diagrama en px y dibuja las curvas desde los centros de los nodos.
5. Fotos de personas mal encuadradas: usa un marco de tamaño fijo con `object-fit:cover` y ajusta `object-position`.
6. Elementos decorativos que sobresalen del escenario y achican el PDF: el verificador lo detecta. Los decorativos de borde van como `<svg class="deco">`.
7. Notas del presentador faltantes o con el título distinto al `data-title`.

## Antes de entregar

- `verificar.py` sin errores graves y todas las capturas revisadas.
- PDF con tantas páginas como diapositivas, en 16:9, sin hoja en blanco al final.
- Títulos releídos con la regla de mayúsculas; todo el texto revisado en busca de faltas.
- Informe final con los cambios de contenido y los pendientes.
