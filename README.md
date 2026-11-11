# ppt-do-creator · Presentaciones DO en HTML y PDF

Skill del equipo de Desarrollo Organizacional (DO) del Hospital Regional de Antofagasta para crear presentaciones animadas con la línea gráfica de DO. A partir de un PowerPoint, un texto o una idea, el asistente de IA entrega:

- **`Nombre.html`**: un solo archivo, funciona sin internet, con navegación por teclado y clic, barra de diapositivas, vista del presentador con notas y cronómetro.
- **`Nombre.pdf`**: una página por diapositiva en 16:9, para enviar a las y los participantes.

> **Esta skill no publica en ppt.do-hra.cl.** La publicación en ese sitio (con clave de Gestión) la realiza solo la Jefatura de DO. Si quieres que tu presentación se publique, envía el HTML y el PDF a la Jefatura.

Puedes ver cómo queda en `referencia/Plantilla_Ejemplo_DO.html` (ábrelo en Chrome) y en `referencia/ejemplos_completos/`.

## Cómo instalarla

### Claude (claude.ai, escritorio o móvil)

1. En GitHub, botón verde **Code → Download ZIP** de este repositorio.
2. En Claude: **Ajustes → Capacidades → Skills → Subir skill** y elige el ZIP.
3. Activa la skill **ppt-do-creator**.

### Claude Code

```bash
git clone https://github.com/psgonzalogr/ppt-do-creator ~/.claude/skills/ppt-do-creator
```

### ChatGPT u otro asistente

Sube la carpeta del repositorio (o el ZIP) a la conversación o al proyecto y pide: *«Lee `SKILL.md` y sigue sus instrucciones para crear mi presentación»*. Necesita poder ejecutar código Python para construir los archivos.

## Cómo usarla

Escribe al asistente, por ejemplo:

> Usa la skill ppt-do-creator. Convierte el PowerPoint adjunto en una presentación DO. Se llama «Gestión del Desempeño», es para el Curso de Líderes. Mantén las fotos de las diapositivas 5 y 12.

Adjunta tu material (.pptx, .pdf, .docx o texto) y, si tienes fotos, también. El asistente te devolverá el HTML y el PDF junto con un informe de los cambios de redacción para que los revises.

### Cómo presentar

| Acción | Tecla / gesto |
|---|---|
| Avanzar / retroceder | → ← , Espacio, AvPág / RePág, o clic en la mitad derecha / izquierda |
| Ir a una diapositiva | Escribir su número y Enter, o usar la barra inferior |
| Pantalla completa | F |
| Vista del presentador (notas, cronómetro, siguiente diapositiva) | S |
| Pantalla negra | B |
| Ayuda de atajos | H |

## Si trabajas a mano (sin asistente)

```bash
pip install -r scripts/requisitos.txt && playwright install chromium
cp -r ejemplo mi_presentacion          # edita deck.json, diapositivas.html y notas.json
python3 scripts/construir.py mi_presentacion
python3 scripts/verificar.py mi_presentacion/salida/MiArchivo.html
```

Los archivos quedan en `mi_presentacion/salida/`. Si no puedes instalar Playwright, genera el PDF desde Chrome: abre el HTML agregando `?print=1` al final de la dirección, **Ctrl+P → Guardar como PDF**, márgenes **Ninguno** y activa **Gráficos de fondo**.

## Contenido del repositorio

| Ruta | Descripción |
|---|---|
| `SKILL.md` | Instrucciones que lee el asistente. |
| `motor/motor.html` | Motor y estilos comunes (no se edita). |
| `scripts/` | `construir.py` (HTML + PDF), `verificar.py` (control de calidad), `catalogo.py` (explorar diapositivas de referencia), `empaquetar.py` (crear el ZIP). |
| `ejemplo/` | Proyecto de ejemplo para copiar. |
| `referencia/` | Prompt maestro, guía de componentes, ejemplo construido y dos presentaciones completas. |
| `assets/` | Logos, fuentes e íconos. |

## Cambios al repositorio

Los cambios entran por pull request y los fusiona la Jefatura de DO. No subas presentaciones con información confidencial ni datos personales a este repositorio: las presentaciones de cada persona se guardan fuera de él.

## Licencias de terceros

Fuentes **Montserrat** y **Source Sans 3** (SIL Open Font License 1.1) e íconos **Lucide** (licencia ISC, ver `assets/iconos/LICENSE-Lucide.txt`). Los logos pertenecen al Hospital Regional de Antofagasta y a su Departamento de Desarrollo Organizacional.
