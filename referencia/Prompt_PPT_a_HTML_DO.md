# Prompt: convertir presentaciones PowerPoint en presentaciones HTML animadas (Departamento de Desarrollo Organizacional, HRA)

> **Cómo usar este prompt:** copia todo el texto desde la línea «INICIO DEL PROMPT» hasta el final y pégalo en un asistente de IA que pueda leer archivos y entregar archivos (por ejemplo, Claude con ejecución de código). Adjunta:
> 1. El archivo **.pptx** original (y si lo tienes, su exportación en **.pdf**, para que el asistente vea cómo se ve cada diapositiva).
> 2. Los **logos** de la carpeta `logos` del kit: `DO_vertical_color.png` y `Hospital_Regional_Antofagasta.png` (obligatorios). Agrega `Calidad_de_Vida.png`, `SOGA.png` u otros solo si la presentación los usa.
> 3. **Muy recomendado:** el archivo **`Plantilla_Ejemplo_DO.html`** (incluido en el kit) como **implementación de referencia**. Contiene el motor completo (navegación, barra inferior, ir a número, vista del presentador, modo PDF) y ejemplos de componentes. Así el asistente reutiliza el mismo motor y el resultado queda idéntico en comportamiento.
>
> Completa los campos entre corchetes de la sección «Datos de esta presentación».

---

## INICIO DEL PROMPT

Actúa como diseñador de presentaciones y desarrollador front-end. Tu tarea es transformar la presentación PowerPoint adjunta en una **presentación HTML animada, autocontenida y profesional** para el Departamento de Desarrollo Organizacional (DO) del Hospital Regional de Antofagasta Dr. Leonardo Guzmán, y además entregar un **PDF** de la misma presentación para enviar a los participantes.

Trabaja en este orden: (1) lee y extrae todo el contenido, (2) planifica el diseño diapositiva por diapositiva, (3) construye, (4) revisa visualmente cada diapositiva y corrige, (5) entrega con un informe breve. No me pidas aprobación entre pasos salvo que haya una ambigüedad que cambie el resultado.

### 1. Datos de esta presentación

- Nombre de la presentación: [ej. «Retroalimentación Efectiva»]
- Curso o módulo (si aplica): [ej. «Curso de Líderes · Nivel 2»]
- Imágenes que **deben mantenerse** tal cual (fotos, documentos, capturas, logos de otras unidades): [ej. «foto de la actividad en la diapo 16; páginas del descriptor en diapos 6 a 9»]
- Diapositivas que necesitan una explicación gráfica animada especial: [ej. «diapo 5: conductos regulares de comunicación ascendente y descendente»]
- ¿Agregar diapositiva de objetivo de la sesión si no existe?: [sí / no]
- Nombre de carpeta para el sitio ppt.do-hra.cl: [ej. `retroalimentacion-efectiva`]

### 2. Entregables

1. **`[Nombre]_DO.html`**: un solo archivo HTML que funcione sin internet. Todo va incrustado: CSS, JavaScript, fuentes (WOFF2 en base64), logos e imágenes (data URI; fotos en JPEG optimizado de unos 1000–1700 px de ancho). Nada de CDN ni recursos externos.
2. **`[Nombre]_DO.pdf`**: una página por diapositiva, en 16:9 (1920 × 1080 px), con el contenido llenando toda la hoja, sin franjas blancas, con todos los elementos visibles y en su estado final.
3. **Notas del presentador**: un borrador breve (2 a 4 ideas) por diapositiva, incluido dentro del HTML.
4. **Informe final** en el chat: qué rehiciste gráficamente y qué cambios de contenido hiciste (correcciones, unificaciones, agregados), para que yo los revise.

Si además existe el sitio ppt.do-hra.cl, entrega el HTML con el nombre `index.html` dentro de la carpeta indicada y una tarjeta nueva para la portada del sitio, con el mismo estilo que las existentes.

### 3. Reglas de contenido (no negociables)

- **Puedes redactar mejor, pero no cambiar el contenido.** Corrige ortografía, tildes, concordancia y puntuación; mejora la fluidez; usa lenguaje inclusivo institucional («las y los funcionarios», «funcionario/a»). No agregues ideas nuevas, cifras, leyes ni ejemplos que no estén en el original.
- Escribe en **español formal institucional de Chile**, natural y sin relleno burocrático ni frases de IA («cabe destacar», «en este sentido», «es fundamental», guiones largos decorativos).
- **Títulos:** cada palabra con mayúscula inicial, **excepto conectores** (y, o, de, del, la, las, el, los, para, en, un, una, a, con, por, su, que). Ejemplo: «Herramientas para la Colaboración», «Motivación a través del Compromiso». **Las preguntas van en tipo oración:** «¿Qué es un líder?». Los rótulos pequeños sobre el título (eyebrows) van en mayúsculas sostenidas por CSS.
- **Texto justificado** en párrafos y cuadros de texto (`text-align: justify; text-align-last: left`). **Nunca cortes palabras con guion** (`hyphens: manual`, jamás `hyphens: auto`). En columnas angostas o tarjetas pequeñas (menos de ~45 caracteres por línea), alinea a la izquierda, porque el justificado deja espacios enormes; avísalo en el informe.
- Si el original tiene **incoherencias** (por ejemplo, una etapa rotulada distinto en dos diapositivas), unifícalas y repórtalas.
- Si agregas rótulos de apoyo (nombres de secciones, «Para reflexionar», etiquetas de un diagrama derivadas del texto), deben resumir el contenido existente, no inventarlo. Repórtalos.
- Mantén las citas y sus autores. Si un apellido o referencia parece mal escrito, corrígelo solo si estás seguro, y avísalo.
- Datos de contacto (correos, anexos, ubicaciones): cópialos exactos y muéstralos como texto seleccionable.

### 4. Identidad visual de DO

**Paleta** (definir como variables CSS):

| Token | Color | Uso |
|---|---|---|
| `--navy` | `#0B2D4F` | Títulos, fondos oscuros |
| `--blue` | `#2462AC` | Acento principal |
| `--ocean` | `#0E7AC2` | Rótulos, números |
| `--teal` | `#0E6E92` | Variante |
| `--cyan` | `#00A9E6` | Brillos, puntos, énfasis |
| `--aqua` | `#33B6C2` | Variante clara |
| `--amber` | `#F2A33A` | Solo para contrastar un segundo flujo o una pregunta al grupo |
| `--bg` | `#F3F7FA` | Fondo claro |
| `--ink` | `#1E2B38` | Texto de cuerpo |
| `--muted` | `#5A6B7C` | Texto secundario |

Fondo oscuro (portada, portadillas de módulo, actividades, cierre): `radial-gradient(1200px 900px at 85% 30%, #174d80 0%, #0B2D4F 55%, #071f38 100%)`.

**Tipografía:**

- Títulos y rótulos: **Montserrat** (700, 800, 900; itálica 300 para el «y Equipo» de las portadas).
- Texto: **Source Sans 3** (400, 600, 700).
- Escala en un escenario de 1920 × 1080: título 56–66 px, portada 120–150 px, párrafo 26–31 px, tarjetas 22–27 px y nunca menos de 19 px.

**Logos:** en **todas** las diapositivas, abajo a la derecha, dentro de una cápsula blanca con sombra suave: logo del Hospital, separador fino y logo **vertical a color** de DO, ambos de unos 84 px de alto. Abajo a la izquierda van el número «07 / 27» en una píldora y el texto «[Nombre de la presentación] · Desarrollo Organizacional».

**Motivo gráfico:** un anillo de círculos de colores inspirado en el isologo de DO (círculos sobre una circunferencia punteada que gira lento), grillas de puntos que se desplazan y círculos de marca que flotan en los bordes. Íconos: **Lucide** (SVG en línea, trazo `currentColor`), dentro de cajas redondeadas con degradado cyan→azul.

**Estilo de las diapositivas de contenido:**

- Rótulo pequeño en mayúsculas con una línea a la izquierda (eyebrow).
- Título con la segunda parte en degradado de color.
- Tarjetas blancas de bordes redondeados (24–30 px) con sombra suave.
- Evita el «todo centrado» y las plantillas genéricas: cada diapositiva debe tener una composición pensada para su contenido.
- Reemplaza ilustraciones de Canva o clip-art por diagramas propios en SVG o CSS con los colores de DO, salvo las imágenes que te pedí mantener.

### 5. Motor de la presentación (comportamiento obligatorio)

Si te adjunto una presentación HTML de referencia (por ejemplo, `Plantilla_Ejemplo_DO.html`), **reutiliza su motor completo** (CSS base, JavaScript, vista del presentador, modo de impresión) y cambia solo las diapositivas, los textos del pie y el canal de sincronización. Si no la tienes, implementa lo siguiente:

**Escenario**

- Un contenedor fijo de 1920 × 1080 px escalado con `transform: scale()` para caber en cualquier pantalla, centrado y sin deformarse.
- Cada diapositiva es un `<section class="slide" data-title="...">` con posiciones en px dentro del escenario.

**Navegación**

| Acción | Teclas / gesto |
|---|---|
| Avanzar | → ↓ AvPág Espacio Enter N, **clic en la mitad derecha** de la diapositiva, rueda del mouse hacia abajo, deslizar a la izquierda en pantalla táctil |
| Retroceder | ← ↑ RePág Retroceso P, **clic en la mitad izquierda**, clic derecho (sin abrir el menú contextual), rueda hacia arriba, deslizar a la derecha |
| Ir a una diapositiva por número | Escribir el número con las teclas 0–9 (o G para enfocar el cuadro) y Enter |
| Saltar con la barra inferior | Pasar el mouse por la barra para ver miniaturas; clic o arrastrar para ir |
| Ir al inicio / al final | Inicio / Fin |
| Pantalla completa | F (también F5) |
| Pantalla negra | B o «.» (cualquier tecla la quita) |
| Vista del presentador | S |
| Mostrar u ocultar la ayuda de atajos | H o ? |
| Ampliar una imagen | Clic sobre imágenes marcadas como ampliables (documentos, capturas); clic o cualquier tecla cierra |

Los **presentadores inalámbricos** envían AvPág/RePág, así que deben funcionar sin configuración.

**Barra de navegación inferior (saltar entre diapositivas)**

- Franja fija a todo el ancho, abajo, de 6 px que crece a 16 px al pasar el mouse. Muestra el avance en degradado cian → aqua y una marca fina por cada diapositiva.
- Al pasar el mouse aparece, sobre el cursor, una **miniatura de la diapositiva** que corresponde a esa posición, con «n / total · título». La miniatura es la misma página en un iframe con `?embed&still`, mostrada en su estado final y controlada por `postMessage`.
- Clic o arrastre salta a la diapositiva bajo el cursor.

**Ir a una diapositiva escribiendo su número**

- La botonera inferior incluye un cuadro numérico «12 / 27».
- Teclear cualquier dígito (o G) enfoca el cuadro, muestra la miniatura de destino y salta con Enter. Si el número ya no admite otro dígito (por ejemplo, 3 en una presentación de 27), salta solo después de un instante.
- Escape cancela. Un número inválido marca el cuadro en rojo.
- Mientras el cuadro tiene el foco, las flechas no navegan. El Enter que confirma no debe avanzar además una diapositiva.

**Clic por mitades**

- Clic en la mitad izquierda retrocede; clic en la mitad derecha avanza. Se ignoran los clics sobre la botonera, la barra, la vista previa o imágenes ampliables.
- Al mover el mouse, un indicador sutil (degradado lateral con un círculo «‹» o «›») muestra qué hará el clic en ese lado.

**Otros elementos de la interfaz**

- Botonera centrada abajo (anterior, número de diapositiva, siguiente, atajos, presentador, pantalla completa) que aparece al mover el mouse y se oculta junto con el cursor tras 2 s de inactividad, salvo que el cuadro de número tenga el foco. No debe tapar los logos.
- Aviso de atajos al cargar, durante ~6 s, que se puede volver a abrir con H. Debe incluir: avanzar y retroceder (teclas y clic por mitades), ir a una diapositiva (número + Enter o barra inferior), F, B, S y H.
- `#n` en la URL abre directo en la diapositiva n (por ejemplo `…/index.html#6`) y la URL se actualiza al navegar.

**Pasos dentro de una diapositiva (fragmentos)**

- Una diapositiva puede declarar `data-steps="N"`. «Avanzar» recorre los pasos antes de pasar a la siguiente diapositiva; «Retroceder» los deshace en orden inverso. Al llegar retrocediendo, la diapositiva aparece con todos sus pasos activos.
- Implementación: la diapositiva recibe las clases acumulativas `st1`, `st2`, `st3`; los elementos con `data-step="k"` aparecen cuando la diapositiva tiene `st{k}`. Úsalo para revelar ejemplos uno a uno o para activar flujos de un diagrama.

**Transición entre diapositivas (tipo «transformar», nunca a negro)**

- El fondo (claro u oscuro), los círculos de marca y el pie con logos son **capas persistentes** que no se apagan entre diapositivas. El fondo hace un fundido entre claro y oscuro (~1 s).
- Los círculos de marca se **desplazan** a nuevas posiciones en cada diapositiva (transición de `transform` de ~1,2 s) y flotan suavemente.
- El contenido saliente se va con un desplazamiento lateral y un fundido escalonado (~0,5 s; hacia la izquierda al avanzar, hacia la derecha al retroceder). El entrante entra escalonado: cada elemento con clase `.a` usa `--i` para su retardo (`calc(var(--i) * 90ms + 360ms)`), con variantes desde abajo, izquierda, derecha, «pop», fundido, crecimiento vertical y horizontal.
- Las líneas de diagramas se **dibujan** (`stroke-dasharray` con `pathLength="1"`).
- Al volver a una diapositiva, sus animaciones de entrada se reinician.

**Vista del presentador (tecla S)**

- Abre una ventana emergente con: la diapositiva **actual** (en vivo, con animaciones), la **siguiente** (estática, en su estado final; si quedan pasos, muestra el siguiente paso), las **notas** con botones A− / A+, un **cronómetro** con pausa y reinicio (T pausa), la **hora**, el número de diapositiva, los indicadores de paso, un selector «Ir a…», botones Anterior y Siguiente, y un indicador «Sincronizado / Sin conexión».
- Sincronización entre ventanas con `postMessage` (ventana que abrió ↔ emergente) más `BroadcastChannel` con un nombre único por presentación. Los comandos llevan un id para no duplicarse.
- La ventana del público difunde su estado `{cur, step}` en cada cambio. El teclado y el presentador inalámbrico funcionan en cualquiera de las dos ventanas.
- Las vistas previas son la misma página cargada en iframes con `?embed` (en vivo) y `?embed&still` (sin animaciones, todo visible), controladas por `postMessage`.
- Si el navegador lo permite (`getScreenDetails`), intenta llevar la presentación a pantalla completa en la pantalla extendida. Si no, muestra el aviso: «Lleva esta ventana al proyector y presiona F». Si se bloquean las ventanas emergentes, avisa cómo permitirlas.
- Las notas se escriben en cada diapositiva dentro de `<aside class="notes">` (ocultas en la presentación). Si una diapositiva tiene pasos, las notas indican qué ocurre en cada clic.

**Modo PDF (`?print=1`)**

- Todas las diapositivas se apilan una tras otra, cada una de 1920 × 1080 px con `break-after: page` (la última sin salto, para no generar una hoja en blanco). Se desactivan todas las animaciones, los elementos quedan visibles en su estado final, todos los pasos activos, y se ocultan la botonera, la ayuda, la barra de navegación, la vista previa, los indicadores laterales y las partículas en movimiento.
- Cada diapositiva lleva su propio fondo, pie con logos y círculos decorativos estáticos.
- Genera el PDF con Chromium/Playwright: `page.pdf(width="1920px", height="1080px", print_background=True, prefer_css_page_size=True)` y `@page { size: 1920px 1080px; margin: 0 }`.
- **Importante:** ningún elemento puede sobresalir del escenario de 1920 × 1080 en modo PDF (por ejemplo, círculos posicionados fuera del borde), aunque la diapositiva tenga `overflow: hidden`. Chrome los cuenta y **achica todo el PDF** (aparecen franjas blancas a la derecha y abajo). Dibuja los decorativos de borde dentro de un `<svg>` de 1920 × 1080 que los recorte. Verifica midiendo que el contenido llegue al borde de la página.

### 6. Animación: constante y al servicio de la explicación

**Toda diapositiva debe tener al menos un elemento en movimiento continuo** (no solo entradas y salidas), sutil y en bucle. Repertorio:

- **Íconos con microanimación según su significado:**
  - flotar suave (por defecto);
  - girar (actualizar o retroalimentación);
  - latir (corazón, check, escudo, diana);
  - brillar (ampolleta, estrella, corona);
  - rebotar (pin de ubicación, flecha);
  - balancearse (megáfono, reloj, conversación);
  - parpadear (ojo tachado).

  Asigna delays distintos entre tarjetas para que no se muevan al unísono.
- **Brillos que recorren elementos:** degradados animados en títulos, barras de progreso, líneas de tiempo y franjas de tarjetas; un reflejo que cruza pirámides, matrices o barras.
- **Pulsos (ripple)** en nodos de un diagrama, números de línea de tiempo y botones de pregunta.
- **Partículas o puntos que viajan** por líneas para mostrar un flujo: mensaje de emisor a receptor, recorrido de una secuencia, líneas de una red.
- **Escenas que explican un concepto**, por ejemplo: cuatro círculos que se funden en uno mayor («el todo es mayor que la suma de sus partes»), barras que se llenan, dos círculos de un diagrama de Venn que se acercan («acuerdo»), burbujas de diálogo que alternan entre dos personas.
- **Elementos decorativos lentos:** anillos que giran (60–90 s por vuelta), grillas de puntos que se desplazan y círculos que flotan.

**Explicaciones gráficas animadas.** Cuando el contenido describe un proceso, una relación o una estructura, **no lo dejes como lista: conviértelo en un diagrama animado.** Ejemplos ya probados en el Departamento:

- **Comunicación descendente y ascendente** en un organigrama:
  - Franjas de fondo para los niveles estratégico, táctico y operativo, cada una con su rótulo.
  - Nodos con las conexiones dibujadas al entrar.
  - Con `data-steps="3"`: el paso 1 hace bajar puntos celestes por las líneas desde la dirección (descendente); el paso 2 los apaga y hace subir puntos ámbar desde la operación (ascendente); el paso 3 muestra ambos a la vez.
  - Leyenda con dos píldoras que se encienden según el paso.
  - Puntos animados con `<animateMotion>` sobre el mismo `<path>` (`keyPoints="1;0"` para invertir el sentido).
- **Emisor → canal → receptor:** un punto que viaja por la línea.
- **Pirámides** (normativa, claves de la comunicación): niveles que aparecen de la base a la cima, un reflejo que la recorre y etiquetas conectadas con líneas punteadas.
- **Líneas de tiempo y secuencias** (ciclo de gestión del desempeño, pasos de una entrevista): línea que se dibuja, flujo que la recorre, nodos numerados que pulsan, fases con fondos de color y una flecha de retorno si el proceso es cíclico.
- **Matriz 2×2:** cuadrantes que aparecen en orden con un reflejo que los cruza.
- **Escalera o barras crecientes:** barras que crecen y un brillo que las sube.
- **Órbitas** (motivación intrínseca y extrínseca): un núcleo con satélites y partículas que salen del centro (lo interno) o llegan a él (lo externo).
- **Modelos con siglas** (BEST): letras grandes en fichas de color que saltan en secuencia; en el ejemplo, revelar cada paso con un clic.
- **Técnicas por capas** (sándwich): ilustración SVG propia cuyas capas caen y se apilan, con etiquetas alineadas a cada capa.

En la sección «Datos de esta presentación» te indico diapositivas específicas, pero **identifica tú también las oportunidades** y propón la representación más clara. Respeta `prefers-reduced-motion` si es simple hacerlo.

### 7. Estructura sugerida de la presentación

- **Portada** oscura: rótulo (curso o departamento), título grande en dos líneas (la segunda en itálica fina celeste), barra de acento, Departamento y Hospital, anillos girando.
- **Objetivo de la sesión** (si existe o si lo pido): objetivo general en tarjeta oscura con una diana animada y objetivos específicos en tarjetas con íconos.
- **Portadillas de módulo** oscuras con un número gigante en contorno («01», «02»…), un rótulo «Módulo 01» y el título.
- **Diapositivas de contenido** con composiciones variadas: dos columnas, tarjetas, diagramas, citas destacadas, fichas de datos con cifras grandes (por ejemplo «1989 · 2004 · 163 artículos»), «Para reflexionar» con un círculo ámbar «?» que pulsa cuando el original plantea una pregunta al grupo.
- **Actividad:** fondo oscuro, rótulo «¡Actividad!», foto en marco tipo polaroid con chinches e íconos flotando.
- **Cierre:** «¡Muchas Gracias!» y datos de contacto si los hay.

### 8. Errores frecuentes que debes evitar

1. **Especificidad de CSS:** si un elemento con animación de entrada (`.a`) también tiene una animación continua propia, una anula a la otra y el elemento puede quedar invisible. Pon la animación continua en un hijo o pseudo-elemento, o declara ambas en una sola regla (`animation: entrada …, bucle …`).
2. **Colisión de clases:** no reutilices nombres genéricos (`.b1`, `.lg`, `.bub`, `.num`) para cosas distintas; usa prefijos por componente.
3. **Íconos SVG sin tamaño:** fija `svg { width: 1em; height: 1em }` para los íconos y no apliques reglas de tamaño de diagrama (`.algo svg { width: 1920px }`) a los íconos internos; usa `> svg`.
4. **Texto que se sale** de círculos, fichas o tarjetas: revisa cada diagrama y ajusta el tamaño o la posición de las etiquetas.
5. **Justificado con espacios enormes** en columnas angostas: usa alineación izquierda ahí.
6. **PDF achicado** por elementos fuera del borde (ver modo PDF).
7. **Hoja en blanco al final del PDF** por el salto de página de la última diapositiva.
8. **Imágenes pesadas:** comprime las fotos y documentos (JPEG de calidad ~80); la presentación completa debería pesar menos de ~5 MB.

### 9. Control de calidad antes de entregar

- Genera una captura de **cada diapositiva** en modo PDF y revísala: nada cortado, superpuesto ni fuera de la diapositiva, ningún texto ilegible, logos en todas.
- Prueba en el navegador: avanzar y retroceder con teclado, clic en cada mitad, rueda y pasos; la barra inferior (miniatura y salto); escribir un número y Enter; la tecla H; la ampliación de imágenes; la vista del presentador (que avance la presentación del público desde la ventana del presentador y que la vista previa muestre el paso siguiente). Revisa que la consola no tenga errores.
- Verifica en el PDF: número de páginas igual al de diapositivas, tamaño 1920 × 1080, contenido hasta el borde.
- Relee todos los títulos con la regla de mayúsculas y todo el texto buscando faltas.

### 10. Informe final (en el chat, breve)

1. Archivos entregados y cómo usar la presentación (clic por mitades, número + Enter, barra inferior, S presentador, F pantalla completa, H ayuda, B negro).
2. Qué diapositivas rediseñaste como diagramas animados y qué hace cada uno (especialmente las que tienen pasos por clic).
3. Lista de cambios de contenido para revisar: correcciones, unificaciones, rótulos agregados y referencias dudosas.
4. Pendientes, si los hay (por ejemplo, un logo faltante con un espacio reservado).

## FIN DEL PROMPT
