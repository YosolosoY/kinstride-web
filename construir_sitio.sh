#!/usr/bin/env bash
# Reconstruye TODO el sitio (en, es, pt, fr, de, it) SIN publicar: generar → traducciones/hreflang → restaura privacidad pt/fr/de/it
# → quita enlaces solo-en/es → enlace de la guía. Uso: ./construir_sitio.sh   (PLAY_LIVE=1 ./construir_sitio.sh para el modo producción)
set -euo pipefail
cd "$(dirname "$0")"
python3 generar.py | tail -1
.venv/bin/python idiomas_sitio.py construir | tail -1
git checkout -- de/datenschutz/index.html fr/confidentialite/index.html it/privacy/index.html pt/privacidade/index.html  # construir pisa estas 4 (traducidas a mano)
python3 - <<'PY'
import re
from pathlib import Path
for lang in ('pt', 'fr', 'de', 'it'):
    for f in Path(lang).rglob('index.html'):
        h = f.read_text()
        h2 = re.sub(r' · <a href="/events/">[^<]*</a>', '', h)
        h2 = re.sub(r'<a href="/events/">[^<]*</a>', '', h2)
        if h2 != h:
            f.write_text(h2)
PY
python3 enlace_guia.py
