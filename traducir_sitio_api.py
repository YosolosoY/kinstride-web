#!/usr/bin/env python3
"""Traduce con Sonnet 5.5 (API de lotes, mitad de precio) los textos de datos/i18n-sitio/faltan-<idioma>.json.
Se corre en el homeserver, donde está la llave (nunca copiarla a otra máquina):
    python3 traducir_sitio_api.py pt fr de it      → datos/i18n-sitio/nuevas-<idioma>.json
Necesita datos/glosario-i18n.json (el glosario de la app). Luego: python3 idiomas_sitio.py importar"""
import json, sys, time, urllib.request
from pathlib import Path
D = Path(__file__).parent / 'datos'
KEY = open('/srv/automatizacion/recordatorios/anthropic_api_key').read().strip()
MODELO, P_IN, P_OUT = 'claude-sonnet-5-5', 1 / 1e6, 5 / 1e6  # lotes: −50 %
NOM = {'pt': ('portugués de Brasil', 'você'), 'fr': ('francés', 'tu'), 'de': ('alemán', 'du'), 'it': ('italiano', 'tu')}
LIMITE_CHARS = 5000
tope = float(sys.argv[sys.argv.index('--tope-usd') + 1]) if '--tope-usd' in sys.argv else 0.50
langs = [a for a in sys.argv[1:] if a in NOM]
glos = json.load(open(D / 'glosario-i18n.json'))

def sistema(lang):
    tabla = '\n'.join(f'{k} = {v[lang]}' for k, v in glos.items() if v.get(lang) and v[lang] != k)
    return f"""Eres localizador profesional. Traduces al {NOM[lang][0]} las páginas web de Kinstride (getkinstride.com): una app Android que convierte tus caminatas en un viaje de fantasía (tono cercano y sobrio; tratamiento «{NOM[lang][1]}»). Hay texto de marketing, de la política de privacidad y de borrado de datos (exactitud legal: no añadas, quites ni suavices nada), de la sección para artistas y de un test.
REGLAS: 1) Entrada: bloques «### huella» seguidos del texto en inglés (a veces con HTML), separados por una línea en blanco; salida: SOLO los mismos bloques «### huella» (la misma huella) seguidos de la traducción, sin comentarios ni comillas añadidas ni JSON. 2) Conserva EXACTAMENTE todas las etiquetas HTML y sus atributos (href, data-*, class…), en el mismo orden y número; traduce solo el texto visible. 3) Conserva números, URLs, correos, {{llaves}}, nombres de marca y de producto (Kinstride, Google Play, Google Drive, Health Connect, Firebase, Supabase, Umami, Discord, TikTok, Instagram, YouTube, Android, Pro, GPS, XP) y los nombres propios (Aldith, Wenna, Tilda Bramble, Hadda Corbel, Sir Osric, Wren Ashby). 4) Adapta separadores numéricos y formatos al idioma (2,865 km → 2.865 km o 2 865 km según la norma). 5) Títulos y encabezados: mayúscula de oración según la norma del idioma, no de cada palabra (salvo nombres propios del glosario). Los <title> ≤ 60 caracteres y las descripciones ≤ 155 cuando el original ya cabe. 6) GLOSARIO OBLIGATORIO (inglés = traducción; respeta género): «stride» = la zancada (ver glosario); la raza/linaje y sus nombres son los del glosario.
{tabla}"""

def http(url, body=None, method='GET'):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, method=method,
                                 headers={'x-api-key': KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json'})
    return urllib.request.urlopen(req, timeout=600).read()

reqs, meta, cota = [], {}, 0.0
for lang in langs:
    faltan = json.load(open(D / 'i18n-sitio' / f'faltan-{lang}.json'))
    sis = sistema(lang); lote, n = {}, 0
    def cerrar():
        global n, cota
        if not lote: return
        cid = f'{lang}-{n}'; n += 1
        reqs.append({'custom_id': cid, 'params': {'model': MODELO, 'max_tokens': 6000, 'output_config': {'effort': 'low'},  # sin esto Sonnet 5.5 «piensa» con este prompt y gasta el máximo sin traducir
                                                    'system': [{'type': 'text', 'text': sis, 'cache_control': {'type': 'ephemeral'}}],
                                                   'messages': [{'role': 'user', 'content': '\n\n'.join(f'### {h}\n{t}' for h, t in lote.items())}]}})
        cota += (len(sis) + len(json.dumps(lote))) / 2.2 * P_IN + len(json.dumps(lote)) / 1.8 * P_OUT
        lote.clear()
    for h, t in faltan.items():
        if sum(len(v) for v in lote.values()) + len(t) > LIMITE_CHARS: cerrar()
        lote[h] = t
    cerrar()
print(f'{len(reqs)} peticiones · cota de costo ${cota:.2f} (lotes)', flush=True)
if cota > tope: sys.exit(f'cota > tope ${tope}')
b = json.loads(http('https://api.anthropic.com/v1/messages/batches', {'requests': reqs}, 'POST')); bid = b['id']; print('lote', bid, flush=True)
while True:
    time.sleep(20)
    b = json.loads(http(f'https://api.anthropic.com/v1/messages/batches/{bid}'))
    if b['processing_status'] == 'ended': break
res, gasto = {l: {} for l in langs}, 0.0
for linea in http(b['results_url']).decode().splitlines():
    r = json.loads(linea); lang = r['custom_id'].split('-')[0]
    if r['result']['type'] != 'succeeded': print('falló', r['custom_id'], r['result']['type']); continue
    m = r['result']['message']; u = m['usage']
    gasto += (u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) * 1.25 + u.get('cache_read_input_tokens', 0) * 0.1) * P_IN + u.get('output_tokens', 0) * P_OUT
    txt = ''.join(x.get('text', '') for x in m['content']).strip()
    import re
    bloques = dict((h, t.strip()) for h, t in re.findall(r'^### (\w+)\n(.*?)(?=^### |\Z)', txt, flags=re.S | re.M))
    if not bloques: print('sin bloques', r['custom_id'], '· stop=', m.get('stop_reason')); continue
    res[lang].update(bloques)
    if m.get('stop_reason') != 'end_turn': print('aviso: respuesta cortada', r['custom_id'], m.get('stop_reason'))
for lang in langs:
    (D / 'i18n-sitio' / f'nuevas-{lang}.json').write_text(json.dumps(res[lang], ensure_ascii=False, indent=1)); print(lang, len(res[lang]), 'traducidos')
print(f'costo real ≈ ${gasto:.3f}')
