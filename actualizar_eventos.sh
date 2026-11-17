#!/usr/bin/env bash
# Actualiza el sitio de eventos de punta a punta, SIN publicar (no hace commit ni push).
#   1 trae del homeserver lo que descubrió el radar   2 consolida (manual + radar)   3 sube el maestro al homeserver (vigilante)
#   4 genera páginas   5 traducciones y hreflang (idiomas_sitio construir)   6 restaura privacidad pt/fr/de/it   7 audita
set -euo pipefail
cd "$(dirname "$0")"
PY=.venv/bin/python
$PY consolidar_eventos.py traer
$PY consolidar_eventos.py
scp -q datos/eventos-completo.json homeserver:sistema/eventos/eventos.json
python3 generar.py | tail -1
$PY idiomas_sitio.py construir | tail -1
git checkout -- de/datenschutz/index.html fr/confidentialite/index.html it/privacy/index.html pt/privacidade/index.html  # construir pisa estas 4 (traducidas a mano)
# el centro de eventos es solo en/es: se quita su enlace de las páginas pt/fr/de/it
python3 - <<'PY'
import re
from pathlib import Path
n = 0
for lang in ('pt', 'fr', 'de', 'it'):
    for f in Path(lang).rglob('index.html'):
        h = f.read_text()
        h2 = re.sub(r' · <a href="/events/">[^<]*</a>', '', h)
        h2 = re.sub(r'<a href="/events/">[^<]*</a>', '', h2)
        if h2 != h:
            f.write_text(h2); n += 1
print(f'enlace de eventos quitado de {n} páginas pt/fr/de/it')
PY
python3 auditar_eventos.py
echo "Listo. Nada publicado: revisa 'git status' y publica solo cuando se ordene."
