#!/usr/bin/env bash
# Cuando la ficha pública de Kinstride en Google Play abre, pone TODO el sitio en «modo producción» sin intervención
# (pedido de Mateo 2026-11-18: «automáticamente actualices todo lo necesario, incluidas todas las páginas, commit y push»).
#   1 ¿abre la ficha? (HTTP 200 + «Kinstride» en el og:title)   2 clon aparte de kinstride-web: play.py LIVE=1, ./construir_sitio.sh (6 idiomas,
#   linajes, test, eventos, guía, artículo de artistas)   3 auditoría: ya no queda «prueba cerrada/tester» en ninguna página y la portada trae el enlace
#   con UTM   4 commit + push   5 dev-web (dev.monsalve.com.co): Kinstride «Disponible en Google Play» + botón   6 verifica en vivo y avisa por Telegram.
# Si algo falla ANTES del push no publica nada, avisa y reintenta a la hora siguiente (aviso de fallo como máximo cada 6 h).
# Ensayo sin publicar ni avisar: ENSAYO=1 ./activar_play.sh   (trata la ficha como abierta, trabaja en un clon temporal y no hace push)
# Instalación: ~/.config/systemd/user/kinstride-play.{service,timer} (cada hora) → copia de este script en ~/.local/share/kinstride-play/
set -uo pipefail
ESTADO="$HOME/.local/state"; mkdir -p "$ESTADO"
LISTO="$ESTADO/kinstride_play_activado"; FALLO="$ESTADO/kinstride_play_fallo"
ENSAYO="${ENSAYO:-0}"
PAQUETE="co.com.monsalve.kinstride"
FICHA="https://play.google.com/store/apps/details?id=$PAQUETE"
avisa() {
  if [ "$ENSAYO" = 1 ]; then printf '[AVISO] %b\n' "$1"; else printf '%b' "$1" | ssh homeserver 'python3 ~/sistema/avisar_telegram.py' || true; fi
}
falla() {  # aviso de fallo como máximo cada 6 h
  echo "$(date '+%F %H:%M') FALLO: $1"
  if [ "$ENSAYO" = 1 ] || [ -z "$(find "$FALLO" -mmin -360 2>/dev/null)" ]; then avisa "🔴 Kinstride ya está en Google Play, pero la actualización AUTOMÁTICA del sitio falló y NO se publicó nada.\n$1\nReintento en una hora."; [ "$ENSAYO" = 1 ] || touch "$FALLO"; fi
  exit 1
}
[ "$ENSAYO" = 1 ] || { [ -e "$LISTO" ] && exit 0; }

# 1) ¿abre la ficha?
if [ "$ENSAYO" != 1 ]; then
  vivo=$(python3 - "$FICHA" <<'PY'
import re, sys, urllib.error, urllib.request
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
try:
    r = urllib.request.urlopen(urllib.request.Request(sys.argv[1] + "&hl=en", headers={"User-Agent": UA}), timeout=30)
    cuerpo, codigo = r.read(3_000_000).decode("utf-8", "replace"), r.status
except urllib.error.HTTPError as e:
    cuerpo, codigo = "", e.code
except Exception:
    print("0"); raise SystemExit
m = re.search(r'og:title"\s+content="([^"]*)"', cuerpo) or re.search(r"<title[^>]*>([^<]*)</title>", cuerpo)
print("1" if codigo == 200 and m and "kinstride" in m.group(1).lower() else "0")
PY
)
  [ "$vivo" = 1 ] || exit 0
fi
exec 9>"$ESTADO/kinstride_play.lock"; flock -n 9 || exit 0

# 2) clon aparte (no toca la copia de trabajo de Mateo)
if [ "$ENSAYO" = 1 ]; then BASE=$(mktemp -d); else BASE="$HOME/.local/share/kinstride-play"; mkdir -p "$BASE"; fi
CLON="$BASE/kinstride-web"
if [ ! -d "$CLON/.git" ]; then git clone -q https://github.com/YosolosoY/kinstride-web.git "$CLON" || falla "No pude clonar kinstride-web."; fi
cd "$CLON" || falla "No existe el clon."
git checkout -q -- . 2>/dev/null; git clean -fdq 2>/dev/null
git pull -q --rebase origin main || falla "No pude actualizar el clon de kinstride-web."
[ -d .venv ] || { python3 -m venv .venv && .venv/bin/pip install -q beautifulsoup4; } || falla "No pude crear el entorno de Python."
[ -f play.py ] || falla "El repositorio aún no trae play.py (el interruptor); no se puede activar."
sed -i "s/os.environ.get('PLAY_LIVE', '0')/os.environ.get('PLAY_LIVE', '1')/" play.py
grep -q "os.environ.get('PLAY_LIVE', '1')" play.py || falla "No pude encender el interruptor en play.py."
salida=$(./construir_sitio.sh 2>&1) || falla "construir_sitio.sh falló: $(printf '%s' "$salida" | tail -3)"

# 3) auditoría antes de publicar
resto=$(grep -rliE "closed testing|prueba cerrada|test fermé|teste fechado|geschlossenen Test|test chiuso|apps/testing|lince-app-testers|Become a tester|Ser tester" --include=*.html . 2>/dev/null | grep -v '^./\.venv' | head -5)
[ -z "$resto" ] || falla "Quedan textos de prueba cerrada en: $(printf '%s' "$resto" | tr '\n' ' ')"
for f in index.html es/index.html pt/index.html fr/index.html de/index.html it/index.html lineages/elf/index.html guides/best-walking-rpg-apps-android/index.html; do
  [ -f "$f" ] && grep -q 'referrer=utm_source%3Dgetkinstride' "$f" || falla "Falta el enlace de Play con UTM en $f"
done
python3 auditar_eventos.py >/tmp/kinstride_auditoria.txt 2>&1 || falla "La auditoría de eventos falló: $(tail -3 /tmp/kinstride_auditoria.txt)"
git add -A
[ -n "$(git diff --cached --name-only | grep -v '^sitemap.xml$')" ] || falla "La reconstrucción no cambió nada: revisa a mano."
nuevas=$(git diff --cached --name-only | grep -c '\.html$')

# 4) commit + push
git commit -q -m "Kinstride ya está en Google Play: botones, textos y enlaces con UTM en todas las páginas" -m "Interruptor play.py en producción; sitio reconstruido en 6 idiomas (portada, linajes, test, eventos, guía, artículo de artistas); auditoría sin textos de prueba cerrada.

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>" || falla "No pude hacer commit."
if [ "$ENSAYO" = 1 ]; then echo "ENSAYO: commit creado en $CLON (páginas HTML cambiadas: $nuevas). Sin push."; else
  git push -q origin main || { git pull -q --rebase origin main && git push -q origin main; } || falla "El commit está listo pero el push falló (¿credenciales?)."
fi

# 5) dev-web (dev.monsalve.com.co)
DEV="$BASE/dev-web"
if [ ! -d "$DEV/.git" ]; then git clone -q https://github.com/YosolosoY/dev-web.git "$DEV" || falla "kinstride-web se publicó, pero no pude clonar dev-web."; fi
( cd "$DEV" && git checkout -q -- . && git pull -q --rebase origin main && python3 - <<PY && python3 generar.py >/dev/null && git add -A && { git diff --cached --quiet && echo "dev-web: sin cambios" || { git commit -q -m "Kinstride: disponible en Google Play (botón y estado)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>" && { [ "$ENSAYO" = 1 ] || git push -q origin main; }; }; }
import re
s = open("generar.py").read()
i = s.index('dict(id="kinstride"'); j = s.index("dict(id=", i + 5)
b = s[i:j]
b = b.replace("play=None,", 'play="$FICHA",', 1).replace('estado={"es": "En prueba cerrada", "en": "Closed testing"}', 'estado={"es": "Disponible en Google Play", "en": "Available on Google Play"}', 1)
assert b != s[i:j], "no cambió el bloque de Kinstride"
open("generar.py", "w").write(s[:i] + b + s[j:])
PY
) || avisa "🟠 Kinstride: el sitio getkinstride.com se publicó, pero dev.monsalve.com.co NO se pudo actualizar solo (revisar a mano)."

# 6) verificación en vivo (GitHub Pages tarda unos minutos) y aviso
if [ "$ENSAYO" = 1 ]; then echo "ENSAYO terminado (sin verificación en vivo ni marca)."; exit 0; fi
ok=0
for i in $(seq 1 12); do
  if curl -s https://getkinstride.com/ | grep -q 'referrer=utm_source%3Dgetkinstride' && curl -s https://dev.monsalve.com.co/ | grep -q "$PAQUETE"; then ok=1; break; fi
  sleep 30
done
touch "$LISTO"
if [ "$ok" = 1 ]; then
  avisa "🚀 Kinstride en Google Play: sitio actualizado y VERIFICADO en vivo ($nuevas páginas HTML cambiadas, 6 idiomas) + dev.monsalve.com.co.\n$FICHA\n\nTe toca (no se puede automatizar):\n• Search Console → pedir indexación de https://getkinstride.com/ , https://getkinstride.com/es/ y https://getkinstride.com/lineages/\n• Poner el enlace de Play en las bios de Instagram, TikTok, YouTube y Discord\n• Enviar los mensajes de archivo/trabajo/lanzamiento (enlaces con UTM en utm-enlaces.md)\n• Decirle a Claude «Play ya salió» para dejar la memoria al día."
else
  avisa "🟠 Kinstride en Google Play: el commit y push se hicieron, pero en 6 min no pude ver el cambio en vivo (GitHub Pages puede tardar más). Revisa https://getkinstride.com/ en un rato."
fi
