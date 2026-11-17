#!/usr/bin/env python3
"""Auditoría automática de las páginas de eventos antes de publicar (reglas de Mateo: cada punto = verificado / falla).

    python3 auditar_eventos.py

Revisa datos (datos/eventos.json) y HTML generado (events/, es/eventos/): título ≤65, descripción 70–165, canonical, un h1,
lang, og, favicons, JSON-LD válido, enlaces internos y de imagen que existen, idioma correcto del texto, sitemap, noindex del formulario,
y que ningún evento «confirmada» se muestre sin fuente oficial, fecha de verificación y cita.
"""
import html as _html
import json
import re
import sys
from pathlib import Path

R = Path(__file__).parent
fallos, ok = [], 0


def chequea(cond, msg):
    global ok
    if cond:
        ok += 1
    else:
        fallos.append(msg)


datos = json.loads((R / 'datos' / 'eventos.json').read_text())['eventos']
for e in datos:
    k = f"{e['ciudad']}/{e['id']}"
    if e['estado'] == 'confirmada':
        chequea(bool(e.get('url_oficial')), f'{k}: confirmada sin url_oficial')
        chequea(bool(e.get('verificado')), f'{k}: confirmada sin fecha de verificación')
        chequea(bool(e.get('con_evidencia')), f'{k}: confirmada sin cita de evidencia')
    if e.get('fecha_inicio') and e.get('fecha_fin'):
        chequea(e['fecha_inicio'] <= e['fecha_fin'], f'{k}: fecha_inicio > fecha_fin')
        chequea(e['fecha_inicio'][:4] in ('2026', '2027', '2028'), f'{k}: año raro {e["fecha_inicio"]}')
    if e['estado'] == 'sin_2027':
        chequea(bool(e.get('ultima_edicion')), f'{k}: sin_2027 sin última edición')

paginas = sorted(list((R / 'events').rglob('index.html')) + list((R / 'es' / 'eventos').rglob('index.html')))
sitemap = (R / 'sitemap.xml').read_text()
ES_EN = re.compile(r'\b(fechas|lugar|organiza|última|ultima|ciudad|evento|eventos)\b', re.I)
EN_ES = re.compile(r'\b(dates|venue|organizer|last edition|events)\b', re.I)
for p in paginas:
    url = '/' + str(p.parent.relative_to(R)).strip('/') + '/'
    es = url.startswith('/es/')
    h = p.read_text()
    t = re.search(r'<title>(.*?)</title>', h, re.S).group(1)
    d = _html.unescape(re.search(r'<meta name="description" content="(.*?)">', h, re.S).group(1))
    t = _html.unescape(t)
    chequea(len(t) <= 65, f'{url}: título {len(t)} car.')
    chequea(70 <= len(d) <= 165, f'{url}: descripción {len(d)} car.')
    chequea(f'<link rel="canonical" href="https://getkinstride.com{url}">' in h, f'{url}: canonical')
    chequea(h.count('<h1') == 1, f'{url}: h1 = {h.count("<h1")}')
    chequea(f'<html lang="{"es" if es else "en"}">' in h, f'{url}: lang')
    chequea(all(x in h for x in ('og:title', 'og:description', 'og:image', 'og:url')), f'{url}: og incompleto')
    chequea(all(x in h for x in ('/favicon.ico', '/img/favicon-96.png', '/favicon.png')), f'{url}: favicons')
    chequea('None' not in re.sub(r'<script.*?</script>', '', h, flags=re.S), f'{url}: aparece "None" en el texto')
    for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            json.loads(ld); chequea(True, '')
        except Exception:  # noqa: BLE001
            chequea(False, f'{url}: JSON-LD inválido')
    for href in re.findall(r'href="(/[^"#]*)"', h):
        if href.endswith(('.css', '.ico', '.png', '.jpg', '.webp')) or href.startswith('/fuentes'):
            chequea((R / href.lstrip('/')).exists(), f'{url}: falta archivo {href}')
        else:
            destino = R / href.strip('/') / 'index.html' if href != '/' else R / 'index.html'
            chequea(destino.exists(), f'{url}: enlace roto {href}')
    for src in re.findall(r'src="(/[^"]+)"', h):
        chequea((R / src.lstrip('/')).exists(), f'{url}: imagen que falta {src}')
    cuerpo = re.sub(r'<(script|style|header|footer)[^>]*>.*?</\1>', '', h, flags=re.S)
    cuerpo = re.sub(r'<a [^>]*>[^<]*(\.[a-z]{2,3}\b|/)[^<]*</a>', ' ', cuerpo)  # texto de URLs oficiales (en el idioma del organizador)
    cuerpo = re.sub(r'<[^>]+>', ' ', cuerpo)
    if not es:
        chequea(not ES_EN.search(cuerpo), f'{url}: texto en español en página inglesa: {ES_EN.search(cuerpo).group(0) if ES_EN.search(cuerpo) else ""}')
    else:
        chequea(not EN_ES.search(cuerpo), f'{url}: texto en inglés en página española: {EN_ES.search(cuerpo).group(0) if EN_ES.search(cuerpo) else ""}')
    if url.endswith(('/submit/', '/enviar/')):
        chequea('noindex' in h, f'{url}: el formulario debe ser noindex')
        chequea(f'https://getkinstride.com{url}' not in sitemap, f'{url}: el formulario no debe ir al sitemap')
    else:
        chequea(f'<loc>https://getkinstride.com{url}</loc>' in sitemap, f'{url}: falta en sitemap')
        chequea('index, follow' in h, f'{url}: debe ser indexable')
        if url.count('/') == 5 or (not es and url.count('/') == 4):  # página de evento
            chequea(bool(re.search(r"href=['\"]https?://[^'\"]+['\"] rel=['\"]noopener['\"]", h)), f'{url}: sin enlace al sitio oficial')

print(f'{len(paginas)} páginas, {ok} comprobaciones correctas, {len(fallos)} fallos')
for f in fallos:
    print('  ✗', f)
sys.exit(1 if fallos else 0)
