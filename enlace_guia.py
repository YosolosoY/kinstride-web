"""Añade a las páginas EN (no es/pt/fr/de/it) el enlace del pie a la guía en inglés. Se corre DESPUÉS de `idiomas_sitio.py construir`.
No va en los generadores porque cambiaría el texto del pie en inglés y las 4 traducciones (pt/fr/de/it) quedarían sin traducir en esa línea.
Idempotente."""
import re
from pathlib import Path

ENLACE = ' · <a href="/guides/best-walking-rpg-apps-android/">Walking RPG apps</a>'
FUERA = {'es', 'pt', 'fr', 'de', 'it', 'node_modules', '.venv', 'guides', '.git', 'archivo'}
n = 0
for f in Path('.').rglob('index.html'):
    if f.parts[0] in FUERA:
        continue
    h = f.read_text()
    if 'guides/best-walking' in h:
        continue
    h2 = re.sub(r'(<p class="pie">(?:(?!</p>).)*?>Events</a>)( · <a href="https://www\.tiktok\.com)', lambda m: m.group(1) + ENLACE + m.group(2), h, count=1, flags=re.S)
    if h2 != h:
        f.write_text(h2); n += 1
print(f'enlace a la guía añadido en {n} páginas en inglés')
