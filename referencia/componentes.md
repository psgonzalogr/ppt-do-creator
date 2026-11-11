# Guía rápida del motor DO

Todo lo que sigue ya está implementado en `motor/motor.html`; solo hay que usar las clases en `diapositivas.html`. Para ver cada componente en contexto, usa `scripts/catalogo.py` sobre las presentaciones de `referencia/ejemplos_completos/` y copia el marcado de la diapositiva que más se parezca.

## 1. Estructura de una diapositiva

```html
<section class="slide" data-title="Título Corto" data-steps="3">
  …contenido en px dentro de un escenario de 1920 × 1080…
</section>
```

- `class="slide"` fondo claro; `class="slide dark"` fondo oscuro (portada, portadillas, actividades, cierre).
- `data-title` es obligatorio, único y es la clave de `notas.json`. Aparece en la miniatura de la barra inferior y en el presentador.
- `data-steps="N"` (opcional): la presentación se detiene N veces dentro de la diapositiva. Mientras avanza, la diapositiva recibe las clases `st1`, `st2`… (acumulativas). Los elementos con `data-step="k"` aparecen cuando existe `stk`. En PDF todos los pasos quedan activos.
- Zona de contenido segura: `<div class="pad">` (92 px arriba, 120 px a los lados, 150 px abajo). Los logos y el pie ocupan los 150 px inferiores: no los tapes.

## 2. Animaciones de entrada

Agrega `a` más una variante a cada elemento que deba entrar escalonado, y `style="--i:N"` para el orden (cada unidad de `--i` retrasa 90 ms).

| Clase | Entra… |
|---|---|
| `a u` | desde abajo |
| `a d` | desde arriba |
| `a l` / `a r` | desde la izquierda / derecha |
| `a p` | con efecto «pop» (escala) |
| `a f` | con fundido |
| `a g` | creciendo en vertical (barras, desde la base) |
| `a gx` | creciendo en horizontal (líneas, barras de avance) |

Al volver a una diapositiva las animaciones se reinician. **Regla:** un elemento con `.a` no debe tener además otra `animation` en la misma regla; pon el bucle en un hijo.

## 3. Movimiento continuo (toda diapositiva debe tener al menos uno)

- **Íconos Lucide** (`{{icon:nombre}}`): flotan solos. Ciertos íconos tienen microanimación según su significado: `refresh-ccw` gira; `megaphone`, `users`, `timer`, `pencil`, `message-circle` se balancean; `heart-pulse`, `check`, `shield-check`, `target` laten; `lightbulb`, `sparkles`, `star`, `crown`, `award` brillan; `map-pin`, `arrow-right`, `zoom-in` rebotan; `eye-off` parpadea.
- `.float`: flotar suave de cualquier elemento.
- `.grid-dots`: grilla de puntos que se desplaza (`<div class="grid-dots" style="right:110px;top:84px"></div>`).
- **Anillos decorativos** (círculos de marca sobre circunferencia punteada que gira): `<svg class="deco ring spin" data-ring="7" data-r="330" data-dot="58" style="right:-200px;top:70px;width:900px;height:900px"></svg>`. `data-ring` = cantidad de círculos, `data-r` = radio, `data-dot` = tamaño del círculo, `data-op` = opacidad; `rev` invierte el giro. Los decorativos de borde llevan la clase `deco` (el modo PDF los recorta).
- `.draw`: líneas que se dibujan al entrar. Pon la clase en un `<svg>` o `<g>` y usa `pathLength="1"` en cada `<path>`/`<line>`.
- `.flowline`: línea punteada que fluye. `.flowdots` + `<animateMotion>`: puntos que viajan por una línea (ver la diapositiva «Diagrama por pasos» de `ejemplo/`; `keyPoints="1;0"` invierte el sentido).
- `@keyframes ripple` (pulso): `animation: ripple 2s infinite` sobre un nodo con `border-radius`.
- Brillo que recorre un título o barra: degradado con `background-size:200%` y `animation: shim 6s linear infinite` (`<em>` de los títulos ya lo trae).

## 4. Piezas base

| Pieza | Uso |
|---|---|
| `.eyebrow` | Rótulo pequeño sobre el título, con línea a la izquierda. Escríbelo en tipo oración: el CSS lo pasa a mayúsculas. |
| `h2` con `<em>` | Título; lo que va en `<em>` toma el degradado de color. En portada: `<h1><span class="a u">Título</span><span class="a u amp">Segunda línea</span></h1>` (la segunda en itálica fina). |
| `.card` | Tarjeta blanca, radio 28 px, sombra suave. |
| `.iconbox` | Caja redondeada con degradado cian→azul para un ícono (76 px). |
| `.sec` + `.bign` | Portadilla de módulo (`slide dark sec`) con número gigante en contorno. Ver «Módulo 01» en `ejemplo/`. |
| `.chipx` | Píldora cian (por ejemplo, subtítulo de una portadilla). |
| `.obj` | Diapositiva de objetivos: tarjeta oscura con diana animada + tarjetas con ícono. |

## 5. Composiciones disponibles (ver `ejemplo/` y `ejemplos_completos/`)

Portada oscura con anillos · objetivo con diana · contenidos numerados · portadilla de módulo · cuadrícula de tarjetas con ícono · tabla comparativa (dos columnas) · diagrama organizacional con pasos (descendente/ascendente) · pirámide con brillo · línea de tiempo o flujo por fases · filas con letra grande (siglas, modelos) · citas destacadas · fichas de datos con cifras grandes · «Para reflexionar» con círculo ámbar «?» · actividad con foto tipo polaroid · órbitas, Venn, matriz 2×2, escalera de barras, sándwich por capas · conclusiones en tres ideas · cierre con anillos.

Para cualquier composición nueva escribe CSS propio en `estilos.css`.

## 6. CSS propio

- **Prefijo `mi-`** en todas las clases nuevas (`.mi-foto`, `.mi-nodo`) para no chocar con las del motor.
- Variables: `var(--navy)`, `--blue`, `--ocean`, `--teal`, `--cyan`, `--aqua`, `--amber`, `--bg`, `--ink`, `--muted`.
- Texto justificado: `text-align:justify; text-align-last:left; hyphens:manual`. En columnas angostas, `text-align:left`.
- Tamaño mínimo de letra: 19 px.
- Íconos dentro de diagramas: `.mi-diagrama > svg { … }` (usa `>` para no afectar a los íconos internos).
- En `estilos.css` puedes usar `{{img:archivo.jpg}}` (por ejemplo `background-image:url({{img:foto.jpg}})`). Para un ícono dentro de un `<svg>` propio en `diapositivas.html` usa `{{iconinner:nombre}}`.

## 7. Diagramas y fotos que salen bien

- **Diagramas SVG:** fija el contenedor en px (por ejemplo 800 × 700), usa un `viewBox` idéntico y calcula las coordenadas de las líneas desde los centros de los nodos. Si el `viewBox` y el contenedor difieren, las líneas se ven «corridas».
- **Etiquetas que no se salen:** deja holgura; un nodo de 330 × 76 px admite unas 28 letras por línea a 24 px.
- **Pasos con diagramas:** dibuja cada grupo de líneas dentro de su `data-step` para que no aparezcan antes que sus nodos.
- **Fotos de personas:** marco de tamaño fijo, `object-fit:cover` y `object-position` (por ejemplo `54% 40%`) para centrar rostros; revisa en la captura que ninguna cabeza quede cortada.
- **Imágenes ampliables** (documentos, capturas): pon `class="zoomable"` (o `doc`) en el contenedor de la imagen; al hacer clic se abre en pantalla completa y cualquier tecla la cierra. Ejemplo: «Descriptor de cargo» en `Liderazgo_y_Equipo_DO.html`.

## 8. Pie de página, logos y modo PDF

- El pie («07 / 27 · Nombre · Desarrollo Organizacional») y la cápsula de logos se agregan solos. El texto sale de `pie` en `deck.json`.
- Modo PDF (`?print=1`): todas las diapositivas apiladas, sin animaciones, con todos los pasos visibles. Ningún elemento debe sobresalir de 1920 × 1080: `verificar.py` lo comprueba.
- Si necesitas un PDF a mano: abre `Nombre.html?print=1` en Chrome → Ctrl+P → destino «Guardar como PDF» → márgenes «Ninguno» → activar «Gráficos de fondo».
