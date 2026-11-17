#!/usr/bin/env python3
"""Junta los candidatos del radar (homeserver: ~/sistema/eventos/crudo/<fecha>/*.json) con los eventos ya verificados a mano
(datos/eventos_manual.json) y escribe datos/eventos.json, que lee generar_eventos.py.

    python3 consolidar_eventos.py semilla      # una sola vez: convierte el piloto verificado a mano en eventos_manual.json
    python3 consolidar_eventos.py traer        # copia del homeserver los .json del radar a datos/eventos-crudo/
    python3 consolidar_eventos.py              # consolida: manual manda sobre radar; descarta lo que no cumple las reglas

Reglas de calidad (precisión sobre cantidad):
  · «confirmada» exige url_oficial + evidencia (cita) y que el dominio no sea un agregador; si no, baja a «solo_terceros».
  · «sin_2027» exige última edición conocida.
  · Se quitan duplicados por nombre normalizado + ciudad; online-only y eventos fuera de las ciudades se descartan.
"""
import json
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).parent
DATOS = RAIZ / 'datos'
CRUDO = DATOS / 'eventos-crudo'
PILOTO = Path.home() / 'Projects/kinstride/archivo/trabajo/eventos-piloto/eventos.json'
AGREGADORES = ('fancons.com', 'animecons.com', 'rostercon.com', 'eventbrite', 'meetup.com', 'facebook.com', 'instagram.com', 'tiktok.com', 'reddit.com',
               'thepopverse.com', 'allevents', 'eventeny.com', 'anihk.com', 'cantonfair', 'jufair', 'tickpick', 'wikipedia', 'dittobase', 'eventsforgamers')

CIUDAD_DE = {'Los Angeles': 'los-angeles', 'San Diego': 'san-diego', 'Chicago': 'chicago', 'New York': 'new-york', 'Atlanta': 'atlanta', 'Houston': 'houston', 'Denver': 'denver', 'Santiago': 'santiago', 'Bogotá': 'bogota', 'Bogota': 'bogota'}

# palabra clave (en el tipo/comunidades/nombre) -> categoría
CATEGORIAS = [
    ('trek', r'trek|hike|hiking|senderis|caminata|trail|5k|10k|run\b|carrera|marathon|marat[oó]n'),
    ('faire', r'renaissance|medieval|faire|\bsca\b|larp|renacentist'),
    ('tcg', r'magic|pok[eé]mon|yu-?gi-?oh|flesh and blood|lorcana|vampir|torneo|tournament|prerelease|commander|\bfnm\b|cartas|trading card|tcg'),
    ('fandom', r'tolkien|harry potter|dune|sanderson|cosmere|reading day|smial|moot|hobbit|star trek|doctor who|tardis|fantas[ií]a y libros'),
    ('anime-comic', r'anime|manga|cosplay|comic|k-?pop|videojuego|video game|pop'),
    ('convention', r'.'),
]


def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'\b(20\d\d|annual|the|con|convention|festival|expo)\b', ' ', s)
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def slug(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'\b20\d\d\b', '', s)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:60].rstrip('-')


def categoria(*textos):
    t = ' '.join(x for x in textos if x).lower()
    for c, rx in CATEGORIAS:
        if re.search(rx, t):
            return c
    return 'convention'


GENERICAS = {'de', 'la', 'el', 'los', 'las', 'del', 'en', 'y', 'and', 'the', 'of', 'torneos', 'torneo', 'eventos', 'evento', 'tienda', 'store', 'grupo', 'salidas', 'diarios', 'meetup',
             'festival', 'fest', 'championship', 'championships', 'series', 'serie', 'edicion', 'party', 'night', 'noche', 'noches', 'feria', 'magic', 'gathering', 'the', 'a'}
SINONIMOS = {'campeonato': 'championship', 'campeonatos': 'championship', 'championships': 'championship', 'regional': 'regional', 'pokemon': 'pokemon'}


def nucleo(nombre):
    """Palabras que identifican al evento (sin lo que va entre paréntesis ni después de ':')."""
    base = re.split(r'[(:\u2014]| - ', nombre or '')[0]
    pal = [SINONIMOS.get(w, w) for w in norm(base).split()]
    return {w for w in pal if w not in GENERICAS}


def misma(a, b):
    na, nb = nucleo(a), nucleo(b)
    if not na or not nb:
        return norm(a) == norm(b)
    if na == nb:
        return True
    menor, mayor = (na, nb) if len(na) <= len(nb) else (nb, na)
    return menor <= mayor and (len(menor) >= 2 or len(mayor) <= 2)


VOZ_AGENTE = re.compile(r"(\bnot (named|stated|specified|listed|announced|indicated|shown)\b|\bfetched\b|third-party|\bI (could|did|found|couldn|saw|opened)|\bmy\b|no pude|no encontr|encontr[ée]|\babr[ií]\b|no se indica|no figura|no especific|no indicad|seg[uú]n (un|el|la|los|las) (art|list|sitio|resultado)|sin confirmar|no confirmad|\bunknown\b|desconoc|\?|e\.g\.|p\. ej\.|\(per\s|\b(does|did|do) not\b|n\x27t\b|the page|la p[aá]gina no|\bfancons\b|\bsource:)", re.I)


def sin_voz_agente(txt):
    """Quita las frases donde el agente habla de sí mismo o de lo que no pudo abrir: no deben llegar a una página pública."""
    if not txt:
        return None
    frases = re.split(r'(?<=[.!])\s+', txt.strip())
    ok = [f for f in frases if not VOZ_AGENTE.search(f)]
    return ' '.join(ok).strip() or None


def organizador_limpio(o):
    o = sin_voz_agente(re.sub(r'\s*\([^)]*\)', '', o or ''))
    return o if o and len(o) <= 80 else None


def lugar_limpio(l):
    if l and VOZ_AGENTE.search(l):
        return None
    if not l:
        return None
    if re.match(r'^(no indicad|no especificad|variable|n/?a\b|por confirmar|tbd|tba|unknown|desconocid|not (announced|specified|listed|stated))', l.strip(), re.I) or len(l) > 110:
        return None
    return l.strip()


FUERA_DE_MARCA = re.compile(r'\b(furry|furries|fursuit|adult[s]?[- ]only|18\+|21\+|nsfw|burlesque|erotic|fetish|kink|bdsm|swinger|cannabis|marijuana|420)\b', re.I)


def dominio_agregador(url):
    return any(a in (url or '').lower() for a in AGREGADORES)


def semilla():
    p = json.loads(PILOTO.read_text())['eventos']
    salida = []
    for e in p:
        c = CIUDAD_DE.get(e['ciudad'])
        if not c:
            continue
        est = {'oficial': 'confirmada', 'plataforma_organizador': 'confirmada', 'prensa_o_tercero': 'solo_terceros', 'sin_2027': 'sin_2027'}.get(e['estado'])
        if not est:
            continue
        m = re.search(r'(20\d\d-\d\d-\d\d) a (20\d\d-\d\d-\d\d)', e['fechas'])
        ini, fin = (m.group(1), m.group(2)) if m else (None, None)
        if est == 'sin_2027':
            ini = fin = None
        salida.append(dict(
            id=slug(e['nombre']), ciudad=c, nombre=re.sub(r'\s*20\d\d$', '', e['nombre']).strip(), tipo=categoria(e['tipo'], e['nombre']), comunidades=[],
            fechas_texto=e['fechas'], fecha_inicio=ini, fecha_fin=fin, recurrente=False, lugar=e.get('lugar'), organizador=e.get('organizador'),
            url_oficial=e['fuente'] if est == 'confirmada' else None, fuentes=[e['fuente']], estado=est,
            ultima_edicion=e['fechas'] if est == 'sin_2027' else None, descripcion=None, precio=e.get('precio'), evidencia=e.get('nota'),
            verificado='2026-11-17' if e['estado'] in ('oficial', 'plataforma_organizador', 'sin_2027') else None, nota=e.get('nota'), origen='manual'))
    (DATOS / 'eventos_manual.json').write_text(json.dumps(salida, ensure_ascii=False, indent=1))
    print(len(salida), 'eventos manuales')


def traer():
    CRUDO.mkdir(parents=True, exist_ok=True)
    subprocess.run(['rsync', '-a', '--include=*/', '--include=*.json', '--exclude=*', 'homeserver:sistema/eventos/crudo/', str(CRUDO) + '/'], check=True)
    subprocess.run(['rsync', '-a', 'homeserver:sistema/eventos/descripciones.json', str(DATOS / 'eventos-descripciones.json')], check=False)
    print(len(list(CRUDO.rglob('*.json'))), 'archivos de radar')


def desde_radar():
    vistos, salida = set(), []
    for f in sorted(CRUDO.rglob('*.json')):
        for e in json.loads(f.read_text()):
            if not e.get('nombre'):
                continue
            if FUERA_DE_MARCA.search(' '.join(str(e.get(k) or '') for k in ('nombre', 'tipo', 'nota', 'fechas_texto')) + ' ' + ' '.join(e.get('comunidades') or [])):
                continue  # la app es familiar (clasificación de edad en Play): fuera lo que no encaja con la marca
            c = e.get('_ciudad')
            estado = e.get('estado')
            url = e.get('url_oficial')
            ev = e.get('evidencia') or ''
            if estado == 'confirmada' and (not url or not ev or not re.search(r'\d', ev) or dominio_agregador(url)):
                estado = 'solo_terceros'
            if estado == 'sin_2027' and not e.get('ultima_edicion'):
                continue
            if estado not in ('confirmada', 'solo_terceros', 'sin_2027'):
                continue
            if re.search(r'online|virtual', (e.get('lugar') or '') + ' ' + (e.get('nota') or ''), re.I) and not e.get('lugar'):
                continue
            k = (c, norm(e['nombre']))
            if k in vistos:
                continue
            vistos.add(k)
            salida.append(dict(
                id=slug(e['nombre']), ciudad=c, nombre=re.sub(r'\s*20\d\d$', '', e['nombre']).strip(), tipo=categoria(e.get('tipo'), ' '.join(e.get('comunidades') or []), e['nombre']),
                comunidades=e.get('comunidades') or [], fechas_texto=sin_voz_agente(e.get('fechas_texto')) or e.get('fechas_texto'), fecha_inicio=e.get('fecha_inicio') if estado != 'sin_2027' else None,
                fecha_fin=e.get('fecha_fin') if estado != 'sin_2027' else None, recurrente=bool(e.get('recurrente')), lugar=lugar_limpio(e.get('lugar')), organizador=organizador_limpio(e.get('organizador')),
                url_oficial=url if estado != 'solo_terceros' else None, fuentes=[u for u in [url] + (e.get('url_fuente_extra') or []) if u], estado=estado,
                ultima_edicion=sin_voz_agente(e.get('ultima_edicion')), descripcion=None, precio=sin_voz_agente(e.get('precio')), evidencia=ev,
                verificado=e.get('_corrida') if estado != 'solo_terceros' else None, nota=e.get('nota'), origen='radar'))
    return salida


def consolidar():
    manual = json.loads((DATOS / 'eventos_manual.json').read_text()) if (DATOS / 'eventos_manual.json').exists() else []
    radar = desde_radar() if CRUDO.exists() else []
    PRIO = {'confirmada': 3, 'sin_2027': 2, 'solo_terceros': 1}
    lista = []  # (registro) ; se funde con el primero «misma» de su ciudad
    for e in radar + manual:
        e = dict(e)
        e['lugar'] = lugar_limpio(e.get('lugar'))
        for k, r in enumerate(lista):
            if r['ciudad'] == e['ciudad'] and misma(r['nombre'], e['nombre']):
                fuerte, debil = (e, r) if PRIO[e['estado']] > PRIO[r['estado']] or (PRIO[e['estado']] == PRIO[r['estado']] and e.get('origen') == 'manual') else (r, e)
                f = dict(fuerte)
                for kk, v in debil.items():
                    if f.get(kk) in (None, [], '') and v not in (None, [], ''):
                        f[kk] = v
                f['fuentes'] = list(dict.fromkeys((r.get('fuentes') or []) + (e.get('fuentes') or [])))
                f['origen'] = 'manual+radar' if {r.get('origen'), e.get('origen')} >= {'manual', 'radar'} else f.get('origen')
                f['nombre'] = min((r['nombre'], e['nombre']), key=len) if len(min(r['nombre'], e['nombre'], key=len)) >= 3 else f['nombre']
                lista[k] = f
                break
        else:
            lista.append(e)
    por = {(e['ciudad'], norm(e['nombre'])): e for e in lista}
    for e in por.values():  # «confirmada» exige fecha de inicio exacta (salvo recurrentes): una temporada sin días no está confirmada
        if e['estado'] == 'confirmada' and not e.get('fecha_inicio') and not e.get('recurrente'):
            e['estado'] = 'sin_2027' if e.get('ultima_edicion') else 'solo_terceros'
            if e['estado'] == 'solo_terceros':
                e['url_oficial'] = None
    for e in por.values():  # tras limpiar: sin_2027 sin última edición no sirve para una página
        if e['estado'] == 'sin_2027' and not e.get('ultima_edicion'):
            e['estado'], e['url_oficial'] = 'solo_terceros', None
    eventos = sorted(por.values(), key=lambda e: (e['ciudad'], e['fecha_inicio'] or '9999', e['nombre']))
    usados = {}
    for e in eventos:  # ids únicos por ciudad
        k = (e['ciudad'], e['id'])
        usados[k] = usados.get(k, 0) + 1
        if usados[k] > 1:
            e['id'] = f"{e['id']}-{usados[k]}"
    desc = json.loads((DATOS / 'eventos-descripciones.json').read_text()) if (DATOS / 'eventos-descripciones.json').exists() else {}
    for e in eventos:
        d = desc.get(f"{e['ciudad']}/{e['id']}")
        if d and not e.get('descripcion'):
            e['descripcion'] = d['descripcion']
    # completo (notas y citas internas del radar): NO se publica, solo para el vigilante del servidor
    (DATOS / 'eventos-completo.json').write_text(json.dumps({'actualizado': date.today().isoformat(), 'eventos': eventos}, ensure_ascii=False, indent=1))
    # público (datos/ se sirve en getkinstride.com): sin notas ni citas internas
    publicos = []
    for e in eventos:
        q = {k: v for k, v in e.items() if k not in ('nota', 'evidencia')}
        q['con_evidencia'] = bool(e.get('evidencia')) or 'manual' in (e.get('origen') or '')
        publicos.append(q)
    (DATOS / 'eventos.json').write_text(json.dumps({'actualizado': date.today().isoformat(), 'eventos': publicos}, ensure_ascii=False, indent=1))
    from collections import Counter
    print(len(eventos), 'eventos:', dict(Counter(e['ciudad'] for e in eventos)), dict(Counter(e['estado'] for e in eventos)))


if __name__ == '__main__':
    {'semilla': semilla, 'traer': traer}.get(sys.argv[1] if len(sys.argv) > 1 else '', consolidar)()
