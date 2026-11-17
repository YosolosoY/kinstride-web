#!/usr/bin/env bash
# Publicación semanal de los datos de eventos (autorizada por Mateo 2026-11-17). Corre en un clon aparte, así no toca su copia de trabajo.
# Regenera, audita y, SOLO si la auditoría pasa y hay cambios reales, hace commit + push y avisa por Telegram. Si falla, avisa y no publica.
set -uo pipefail
CLON="$HOME/.local/share/kinstride-eventos/kinstride-web"
avisa() { printf '%b' "$1" | ssh homeserver 'python3 ~/sistema/avisar_telegram.py' || true; }
if [ ! -d "$CLON/.git" ]; then mkdir -p "$(dirname "$CLON")"; git clone -q https://github.com/YosolosoY/kinstride-web.git "$CLON" || { avisa "🔴 Eventos: no pude clonar el repositorio"; exit 1; }; fi
cd "$CLON" || exit 1
git checkout -q -- . 2>/dev/null; git pull -q --rebase origin main || { avisa "🔴 Eventos: no pude actualizar el clon; no se publicó nada"; exit 1; }
[ -d .venv ] || { python3 -m venv .venv && .venv/bin/pip install -q beautifulsoup4; }
cp datos/eventos.json /tmp/eventos_antes.json 2>/dev/null || echo '{"eventos":[]}' > /tmp/eventos_antes.json
if ! salida=$(./actualizar_eventos.sh 2>&1); then
  avisa "🔴 Eventos: la actualización semanal falló y NO se publicó.\n$(printf '%s' "$salida" | tail -4)"; git checkout -q -- .; exit 1
fi
git add -A
if [ -z "$(git diff --cached --name-only | grep -v '^sitemap.xml$')" ]; then git reset -q --hard; exit 0; fi   # solo cambió la fecha del sitemap: no hay nada que publicar
resumen=$(python3 - <<'PY'
import json
a = {(e['ciudad'], e['id']): e for e in json.load(open('/tmp/eventos_antes.json'))['eventos']}
b = json.load(open('datos/eventos.json'))['eventos']
nuevos = [e for e in b if (e['ciudad'], e['id']) not in a]
conf = [e for e in b if e['estado'] == 'confirmada' and (e['ciudad'], e['id']) in a and a[(e['ciudad'], e['id'])]['estado'] != 'confirmada']
quitados = [k for k in a if k not in {(e['ciudad'], e['id']) for e in b}]
l = [f"{len(b)} eventos en total ({sum(1 for e in b if e['estado'] == 'confirmada')} confirmados). Nuevos: {len(nuevos)}. Pasaron a confirmados: {len(conf)}. Retirados: {len(quitados)}."]
for e in conf[:8]: l.append(f"• Confirmado: {e['nombre']} ({e['ciudad']}) {e.get('fecha_inicio') or ''}")
for e in nuevos[:6]: l.append(f"• Nuevo: {e['nombre']} ({e['ciudad']})")
print('\n'.join(l))
PY
)
git commit -q -m "Eventos: actualización semanal $(date +%F)" -m "Datos del radar, descripciones y páginas regenerados; auditoría sin fallos." || exit 1
if git push -q origin main; then avisa "📅 Eventos publicados ($(date +%F)).\n${resumen}\nRevisa: https://getkinstride.com/events/ y https://getkinstride.com/es/eventos/"; else avisa "🔴 Eventos: la auditoría pasó pero el push falló; los cambios NO están en vivo."; fi
