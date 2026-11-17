"""Eventos de fantasía, juegos y anime por ciudad (Santiago en español; 7 ciudades de EE. UU. en inglés). Lo llama generar.py.

Datos: datos/eventos.json (lo escribe consolidar_eventos.py a partir del radar y de lo verificado a mano).
Páginas: centro (/events/, /es/eventos/), una por ciudad, una por evento verificado y el formulario para organizadores.

Reglas de contenido (precisión sobre cantidad):
  · Solo tienen página propia los eventos «confirmada» (fecha leída en la web del organizador) y los «sin_2027» con sitio oficial
    y última edición conocida. Los «solo_terceros» aparecen únicamente en la lista de la ciudad, rotulados como no confirmados.
  · Nada de afirmaciones sobre el evento que no vengan de los datos; el ángulo de linajes es nuestra opinión y se dice así.
  · No se traducen a pt/fr/de/it (un evento local habla un solo idioma): idiomas_sitio.py solo toma su lista fija de páginas.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

import generar_linajes as GL

WEBHOOK = 'https://n8n.monsalve.com.co/webhook/kinstride-evento'
HOY = date.today().isoformat()
MIN_CIUDAD = 3  # una ciudad con menos eventos verificados no tiene página (sería contenido delgado)

CIUDADES = {
    'santiago': dict(lang='es', nombre='Santiago', pais='Chile'),
    'los-angeles': dict(lang='en', nombre='Los Angeles', pais='USA'),
    'san-diego': dict(lang='en', nombre='San Diego', pais='USA'),
    'chicago': dict(lang='en', nombre='Chicago', pais='USA'),
    'new-york': dict(lang='en', nombre='New York City', pais='USA'),
    'atlanta': dict(lang='en', nombre='Atlanta', pais='USA'),
    'houston': dict(lang='en', nombre='Houston', pais='USA'),
    'denver': dict(lang='en', nombre='Denver', pais='USA'),
}
BASE = {'en': '/events/', 'es': '/es/eventos/'}
INICIO = {'en': '/', 'es': '/es/'}
OTRA = {'en': '/es/', 'es': '/'}
MESES = {'en': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
         'es': ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']}

# categoría -> (linaje, etiqueta en/es)
CAT = {
    'convention': ('mediano', {'en': 'tabletop, RPG and gaming conventions', 'es': 'convenciones de juegos de mesa y rol'}),
    'anime-comic': ('ascuano', {'en': 'anime, comic and cosplay events', 'es': 'eventos de anime, cómics y cosplay'}),
    'tcg': ('gnomo', {'en': 'card tournaments and game nights', 'es': 'torneos de cartas y noches de juego'}),
    'fandom': ('humano', {'en': 'fantasy and book fandom gatherings', 'es': 'encuentros de fantasía y libros'}),
    'faire': ('arboreo', {'en': 'faires, LARP and medieval events', 'es': 'ferias medievales, LARP y rol en vivo'}),
    'trek': ('enano', {'en': 'treks, trail and costume runs', 'es': 'trekking, trail y carreras temáticas'}),
}
TOMA = {
    'en': {
        'convention': 'Convention days are long and full of stops: halls, queues, tables, panels. That profile is the one Kinstride calls a Halfling.',
        'anime-comic': 'Anime and comic conventions move in bursts: a sprint to a panel, a crawl through the dealers’ room, another sprint. Kinstride calls that pattern Emberkin.',
        'tcg': 'Getting to a tournament or a store night is a short hop of quick little steps. Kinstride’s Gnome is built on exactly that.',
        'fandom': 'Fan gatherings pull in people who like a bit of everything. Humans are Kinstride’s hardest lineage to earn, because they refuse to be just one thing.',
        'faire': 'A faire is an all-day wander across the grounds, slow and ambling for hours. Slow walks that go on for hours are the Barkfolk way.',
        'trek': 'A trek or trail event asks for climbing. In Kinstride, Dwarves are defined by real ascent and a steady pace.'},
    'es': {
        'convention': 'Los días de convención son largos y llenos de paradas: salas, filas, mesas, paneles. Ese perfil es el que Kinstride llama Mediano.',
        'anime-comic': 'Las convenciones de anime y cómics se mueven a ráfagas: carrera a un panel, paseo lento por la zona de tiendas, otra carrera. Kinstride llama Ascuano a ese patrón.',
        'tcg': 'Llegar a un torneo o a una noche de tienda es un salto corto de pasitos rápidos. El Gnomo de Kinstride se define justo por eso.',
        'fandom': 'Los encuentros de fans reúnen a gente a la que le gusta un poco de todo. El Humano es el linaje más difícil de Kinstride, porque se niega a ser una sola cosa.',
        'faire': 'Una feria medieval es un paseo de todo el día por el recinto, lento y de horas. Las caminatas lentas de horas son lo del Arbóreo.',
        'trek': 'Un trekking o una carrera de trail pide subir. En Kinstride, el Enano se define por el desnivel real y el ritmo parejo.'},
}
L = {
    'en': dict(
        loc='en_US', eventos='Events', h_hub='Fantasy, tabletop and anime events near you',
        hub_desc='Conventions, card tournaments, fantasy fan gatherings and faires in {n} US cities, with dates checked against the organizer’s own page.',
        hub_t='Fantasy, Tabletop & Anime Events by City (2027)',
        hub_intro='Conventions, tournaments, faires and fan gatherings for people who play, read and dress up. We only call a date confirmed when we have read it on the organizer’s own page, and we say when we last checked.',
        ciudad_t='Fantasy, gaming & anime events in {c} (2027)', ciudad_t_title='Fantasy, Gaming & Anime Events in {c} (2027)',
        ciudad_desc='{n} fantasy, tabletop, card-game and anime events around {c}: {k} with dates confirmed on the official page, plus those still waiting for 2027 dates.',
        ciudad_intro='Events around {c}. Each listing says whether its date is confirmed on the organizer’s own page. Last update: {f}.',
        s_conf='Dates confirmed', s_rep='Reported, not yet confirmed by the organizer', s_pend='Waiting for 2027 dates', s_rec='Recurring and local', s_pasado='Already happened',
        st_conf='Confirmed on the official site', st_rep='Reported by media or listings; not yet confirmed by the organizer', st_pend='2027 dates not announced yet', st_rec='Recurring',
        f_fechas='Dates', f_estado='Status', f_lugar='Venue', f_ciudad='City', f_org='Organizer', f_precio='Price', f_oficial='Official site', f_ultima='Last edition', f_chequeo='Last checked',
        t_conf='{n} {a}: Dates, Location & Details', t_conf2='{n} {a}: Dates & Location', t_pend='{n} 2027: What We Know So Far', t_rec='{n} in {c}: Schedule & Location', t_rec2='{n}: Schedule & Location',
        d_conf='{n}: {f}{l}. Dates read on the organizer’s page, checked {v}. Venue, official link and the lineage that fits.',
        d_pend='When is {n} 2027? The organizer has not announced dates yet. Last edition: {u}. We check its page and update this one when they do.',
        d_rec='{n}: recurring events in {c}{l}. Schedule checked on the organizer’s page on {v}.',
        linaje_t='Which lineage would walk {n}?', linaje_n='This is our own take from Kinstride’s lineage rules, not data about the event.', test='Take the 1-minute lineage test',
        fuentes_t='Sources and updates', fuentes_p='Dates come from the organizer’s page linked above. We check it regularly and update this page when something changes. Kinstride is not affiliated with {n} or its organizers; event names belong to their owners.',
        mas_t='More events in {c}', hub_link='All cities', volver='All events', envia_t='Know an event we are missing?', envia_p='Organizers and fans can send us an event. We check it against the organizer’s page before listing it.', envia_b='Send an event',
        ya_pasado='Ended {f}', cuenta='{n} events tracked', sin_fecha='Not announced yet', ult='Last edition: {u}',
        f_t='Send an event', f_desc='Organizers and fans: send us a convention, tournament, meetup or fan gathering. We check it against the official page before it goes up.',
        f_h1='Send an event', f_intro='Tell us about a convention, tournament, store night, meetup or fan gathering. We check it against the organizer’s own page before listing it, and we never list it without a source.',
        lb_nombre='Event name', lb_url='Link to the official page, ticket page or post', lb_ciudad='City', lb_fecha='Date or schedule', lb_tipo='Type', lb_msg='Anything else (optional)', lb_mail='Your email, only if you want a reply (optional)',
        enviar='Send', ok='Thanks. We will check it and list it if it passes.', err='Something went wrong. Please try again in a moment.', otra_ciudad='Another city',
        priv='We use your email only to reply about this listing and delete it once the event is checked or on request; see the', priv_link='privacy policy', sin_js='This form needs JavaScript.'),
    'es': dict(
        loc='es_419', eventos='Eventos', h_hub='Eventos de fantasía, juegos y anime cerca de ti',
        hub_desc='Convenciones, torneos de cartas, encuentros de fantasía y ferias en Santiago de Chile, con fechas comprobadas en la página del organizador.',
        hub_t='Eventos de fantasía, juegos y anime en Santiago (2027)',
        hub_intro='Convenciones, torneos, ferias y encuentros para quienes juegan, leen y se disfrazan. Solo llamamos «confirmada» a una fecha cuando la leímos en la página del propio organizador, y decimos cuándo la revisamos por última vez.',
        ciudad_t='Eventos de fantasía, juegos y anime en {c} (2027)', ciudad_t_title='Eventos de fantasía, juegos y anime en {c} (2027)',
        ciudad_desc='{n} eventos de fantasía, juegos de mesa, cartas y anime en {c}: {k} con fecha confirmada en la página oficial, más los que esperan fechas de 2027.',
        ciudad_intro='Eventos en {c}. Cada ficha dice si su fecha está confirmada en la página del propio organizador. Última actualización: {f}.',
        s_conf='Fecha confirmada', s_rep='Informados, sin confirmar por el organizador', s_pend='Esperando fechas de 2027', s_rec='Recurrentes y locales', s_pasado='Ya ocurrieron',
        st_conf='Confirmada en el sitio oficial', st_rep='Informada por medios o listados; aún sin confirmar por el organizador', st_pend='Fechas de 2027 aún sin anunciar', st_rec='Recurrente',
        f_fechas='Fechas', f_estado='Estado', f_lugar='Lugar', f_ciudad='Ciudad', f_org='Organiza', f_precio='Precio', f_oficial='Sitio oficial', f_ultima='Última edición', f_chequeo='Última revisión',
        t_conf='{n} {a}: fechas, lugar y detalles', t_conf2='{n} {a}: fechas y lugar', t_pend='{n} 2027: lo que sabemos', t_rec='{n} en {c}: horarios y lugar', t_rec2='{n}: horarios y lugar',
        d_conf='{n}: {f}{l}. Fechas leídas en la página del organizador, revisadas el {v}. Lugar, enlace oficial y el linaje que le calza.',
        d_pend='¿Cuándo es {n} 2027? El organizador aún no anuncia fechas. Última edición: {u}. Revisamos su página oficial y actualizamos esta cuando lo haga.',
        d_rec='{n}: eventos recurrentes en {c}{l}. Horario comprobado en la página del organizador el {v}.',
        linaje_t='¿Qué linaje caminaría {n}?', linaje_n='Es nuestra opinión a partir de las reglas de linajes de Kinstride, no un dato del evento.', test='Haz el test de linaje de 1 minuto',
        fuentes_t='Fuentes y actualizaciones', fuentes_p='Las fechas salen de la página del organizador enlazada arriba. La revisamos con regularidad y actualizamos esta página cuando algo cambia. Kinstride no tiene relación con {n} ni con sus organizadores; los nombres de los eventos pertenecen a sus dueños.',
        mas_t='Más eventos en {c}', hub_link='Todas las ciudades', volver='Todos los eventos', envia_t='¿Conoces un evento que falte?', envia_p='Organizadores y fans pueden enviarnos un evento. Lo comprobamos contra la página del organizador antes de publicarlo.', envia_b='Enviar un evento',
        ya_pasado='Terminó el {f}', cuenta='{n} eventos en seguimiento', sin_fecha='Aún sin anunciar', ult='Última edición: {u}',
        f_t='Enviar un evento', f_desc='Organizadores y fans: envíanos una convención, torneo, meetup o encuentro de fans. Lo comprobamos en la página oficial antes de publicarlo.',
        f_h1='Enviar un evento', f_intro='Cuéntanos de una convención, torneo, noche de tienda, meetup o encuentro de fans. Lo comprobamos contra la página del propio organizador antes de publicarlo y nunca lo publicamos sin fuente.',
        lb_nombre='Nombre del evento', lb_url='Enlace a la página oficial, de entradas o a la publicación', lb_ciudad='Ciudad', lb_fecha='Fecha u horario', lb_tipo='Tipo', lb_msg='Algo más (opcional)', lb_mail='Tu correo, solo si quieres respuesta (opcional)',
        enviar='Enviar', ok='Gracias. Lo comprobaremos y lo publicaremos si corresponde.', err='Algo salió mal. Inténtalo de nuevo en un momento.', otra_ciudad='Otra ciudad',
        priv='Usamos tu correo solo para responder sobre este evento y lo borramos al revisarlo o si lo pides; mira la', priv_link='política de privacidad', sin_js='Este formulario necesita JavaScript.'),
}
PRIV = {'en': '/privacy/', 'es': '/es/privacidad/'}
ENVIAR = {'en': '/events/submit/', 'es': '/es/eventos/enviar/'}


def titulo_ok(base, marca=' | Kinstride'):
    """Con la marca si cabe en 65 caracteres; si no, sin ella."""
    return base + marca if len(base + marca) <= 65 else base


def nombre_titulo(n, tope=34):
    """Nombre corto para el <title>: sin lo que va entre paréntesis o tras ':'; si aún es largo, se corta."""
    base = re.split(r'\s*[(:]|\s[–—-]\s', n)[0].strip() or n
    return base if len(base) <= tope else cortar(base, tope)


def esc(x):
    return html.escape(str(x), quote=True) if x is not None else ''


def fecha_txt(e, lang):
    """'5–8 feb 2027' / 'Feb 5–8, 2027'; si no hay fechas exactas, el texto del evento."""
    a, b = e.get('fecha_inicio'), e.get('fecha_fin') or e.get('fecha_inicio')
    if not a:
        return None
    ya, ma, da = (int(x) for x in a.split('-'))
    yb, mb, db = (int(x) for x in b.split('-'))
    m = MESES[lang]
    if lang == 'en':
        if (ya, ma, da) == (yb, mb, db):
            return f'{m[ma - 1]} {da}, {ya}'
        return f'{m[ma - 1]} {da}–{db}, {ya}' if (ya, ma) == (yb, mb) else f'{m[ma - 1]} {da} – {m[mb - 1]} {db}, {yb}'
    if (ya, ma, da) == (yb, mb, db):
        return f'{da} {m[ma - 1]} {ya}'
    return f'{da}–{db} {m[ma - 1]} {ya}' if (ya, ma) == (yb, mb) else f'{da} {m[ma - 1]} – {db} {m[mb - 1]} {yb}'


def cortar(s, n):
    if len(s) <= n:
        return s
    return s[:n].rsplit(' ', 1)[0].rstrip(',;:–-') + '…'


def fechas_mostrar(e, lang):
    """Fechas exactas si las hay; si no, el texto de fechas del organizador (p. ej. una temporada)."""
    return fecha_txt(e, lang) or (cortar(e.get('fechas_texto') or '', 120) or None)


def tiene_pagina(e):
    return (e['estado'] == 'confirmada' and e.get('url_oficial')) or (e['estado'] == 'sin_2027' and e.get('url_oficial') and e.get('ultima_edicion'))


def ruta_ev(e, lang):
    return f"{BASE[lang]}{e['ciudad']}/{e['id']}/"


def ruta_ciudad(c, lang):
    return f"{BASE[lang]}{c}/"


def clasificar(e):
    if e.get('recurrente') and e['estado'] != 'sin_2027':
        return 'rec'
    if e['estado'] == 'solo_terceros':
        return 'rep'
    if e['estado'] == 'sin_2027':
        return 'pend'
    if not e.get('fecha_fin') and e.get('fecha_inicio') and e['fecha_inicio'] < HOY:
        return 'pasado'
    if e.get('fecha_fin') and e['fecha_fin'] < HOY:
        return 'pasado'
    return 'conf'


def cabeza(lang, titulo, desc, url, extra='', og_tipo='website', umami=''):
    l = L[lang]
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{og_tipo}">
<meta property="og:site_name" content="Kinstride">
<meta property="og:locale" content="{l['loc']}">
<meta property="og:image" content="{SITIO}/img/{'compartir-es.jpg' if lang == 'es' else 'compartir.jpg'}">
<meta property="og:image:width" content="1024">
<meta property="og:image:height" content="500">
<meta property="og:image:alt" content="{'Logo de Kinstride sobre un mapa de fantasía ilustrado' if lang == 'es' else 'Kinstride logo over an illustrated fantasy map'}">
<meta property="og:url" content="{SITIO}{url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{SITIO}{url}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/img/favicon-96.png" type="image/png" sizes="96x96">
<link rel="icon" href="/favicon.png" type="image/png" sizes="32x32">
<link rel="icon" href="/img/icono-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="/img/icono-180.png">
<meta name="theme-color" content="#1B1C1F">
<link rel="preload" href="/fuentes/saira-extra-condensed-normal-900.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fuentes/saira-extra-condensed-normal-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fuentes/schibsted-grotesk-normal-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/estilo.css">
{umami}{extra}
</head>
<body class="sub">
'''


def migas(items):
    return GL.miga(SITIO, items)


def item_lista(e, lang, con_estado=False):
    l = L[lang]
    f = (esc(cortar(e.get('fechas_texto') or '', 90)) if clasificar(e) == 'rec' else None) or fecha_txt(e, lang)
    if e['estado'] == 'sin_2027' and not e.get('recurrente'):
        f = l['sin_fecha'] + (' · ' + l['ult'].format(u=esc(cortar(e['ultima_edicion'], 90))) if e.get('ultima_edicion') else '')
    elif not f:
        f = esc(cortar(e.get('fechas_texto') or '', 90)) or l['sin_fecha']
    nombre = esc(e['nombre'])
    if tiene_pagina(e):
        nombre = f'<a href="{ruta_ev(e, lang)}">{nombre}</a>'
    elif e.get('fuentes'):
        nombre = f'{nombre} <small>(<a href="{esc(e["fuentes"][0])}" rel="noopener nofollow">source</a>)</small>' if lang == 'en' else f'{nombre} <small>(<a href="{esc(e["fuentes"][0])}" rel="noopener nofollow">fuente</a>)</small>'
    lugar = f' · {esc(cortar(e["lugar"], 80))}' if e.get('lugar') else ''
    return f'<li><b>{nombre}</b><br><span class="dato">{f}{lugar}</span></li>'


def pagina_ciudad(c, evs, lang, umami, srd):
    l, cd = L[lang], CIUDADES[c]
    n, k = len(evs), sum(1 for e in evs if clasificar(e) in ('conf', 'rec'))
    titulo = titulo_ok(l['ciudad_t_title'].format(c=cd['nombre']))
    desc = cortar(l['ciudad_desc'].format(n=n, c=cd['nombre'], k=k), 160)
    grupos = {g: [e for e in evs if clasificar(e) == g] for g in ('conf', 'rec', 'pend', 'rep', 'pasado')}
    secs = ''
    for g, tit in (('conf', 's_conf'), ('rec', 's_rec'), ('pend', 's_pend'), ('rep', 's_rep'), ('pasado', 's_pasado')):
        if grupos[g]:
            secs += f'<h2>{l[tit]}</h2><ul class="eventos">' + ''.join(item_lista(e, lang) for e in grupos[g]) + '</ul>'
    cuerpo = f'''<main class="principal">
<div class="ancho">
<p class="miga"><a href="{BASE[lang]}">{l['eventos']}</a> › {esc(cd['nombre'])}</p>
<h1>{esc(l['ciudad_t'].format(c=cd['nombre']))}</h1>
<p class="intro">{esc(l['ciudad_intro'].format(c=cd['nombre'], f=fecha_larga(HOY, lang)))} {esc(l['cuenta'].format(n=n))}.</p>
{secs}
<section class="resumen tester"><h2>{l['envia_t']}</h2><p>{l['envia_p']}</p><p class="botones"><a class="boton" href="{ENVIAR[lang]}" data-umami-event="enviar-evento">{l['envia_b']}</a></p></section>
{GL.cta(lang)}
</div>
</main>
'''
    ld = migas([('Kinstride', INICIO[lang]), (l['eventos'], BASE[lang]), (cd['nombre'], ruta_ciudad(c, lang))])
    return ruta_ciudad(c, lang), cabeza(lang, titulo, desc, ruta_ciudad(c, lang), ld, umami=umami) + GL.barra(lang, OTRA[lang]) + cuerpo + GL.pie(lang, srd)


def fecha_larga(iso, lang):
    y, m, d = (int(x) for x in iso.split('-'))
    return f'{MESES["en"][m - 1]} {d}, {y}' if lang == 'en' else f'{d} {MESES["es"][m - 1]} {y}'


def pagina_evento(e, evs, lang, umami, srd, linajes):
    l, cd = L[lang], CIUDADES[e['ciudad']]
    n, c = e['nombre'], cd['nombre']
    f = fechas_mostrar(e, lang)
    anio = (e.get('fecha_inicio') or '2027')[:4]
    corto = cortar((e.get('lugar') or '').split(',')[0], 46) if e.get('lugar') else ''
    if not f:
        f = 'dates on the official page' if lang == 'en' else 'fechas en la página oficial'
    lugar = (f' · {corto}' if corto else '')
    v = fecha_larga(e['verificado'], lang) if e.get('verificado') else fecha_larga(HOY, lang)
    est = clasificar(e)
    nt = nombre_titulo(n)
    if est == 'pend':
        titulo, desc = l['t_pend'].format(n=nt), l['d_pend'].format(n=n, u=cortar(e['ultima_edicion'].rstrip('. '), 70))
    elif est == 'rec':
        titulo = l['t_rec'].format(n=nt, c=c)
        if len(titulo) > 65:
            titulo = l['t_rec2'].format(n=nt)
        desc = l['d_rec'].format(n=n, c=c, f=cortar(e.get('fechas_texto') or '', 60), l=lugar, v=v)
    else:
        titulo, desc = l['t_conf'].format(n=nt, a=anio), l['d_conf'].format(n=n, f=f or '', l=lugar, v=v)
        if len(titulo) > 65:
            titulo = l['t_conf2'].format(n=nt, a=anio)
    titulo = titulo_ok(titulo)
    if len(desc) > 165 or len(desc) < 70:
        desc = (desc.split('. ')[0] + '. ' + desc.split('. ')[1] + '.') if desc.count('. ') >= 1 and len(desc.split('. ')[0] + desc.split('. ')[1]) < 160 else cortar(desc, 160)
    if len(desc) < 70:
        desc += ' Official link, venue and the lineage that fits.' if lang == 'en' else ' Enlace oficial, lugar y el linaje que le calza.'
    lin_id, cat_txt = CAT[e['tipo']]
    lin = next(x for x in linajes['razas'] if x['id'] == lin_id)
    estado_txt = {'conf': l['st_conf'], 'pasado': l['st_conf'], 'pend': l['st_pend'], 'rec': l['st_rec']}[est]
    filas = ''
    filas += f"<tr><th scope='row'>{l['f_fechas']}</th><td>{esc((cortar(e.get('fechas_texto') or '', 160) if est == 'rec' else None) or f or l['sin_fecha'])}</td></tr>"
    filas += f"<tr><th scope='row'>{l['f_estado']}</th><td>{estado_txt}</td></tr>"
    if est == 'pend' and e.get('ultima_edicion'):
        filas += f"<tr><th scope='row'>{l['f_ultima']}</th><td>{esc(cortar(e['ultima_edicion'], 160))}</td></tr>"
    if e.get('lugar'):
        filas += f"<tr><th scope='row'>{l['f_lugar']}</th><td>{esc(e['lugar'])}</td></tr>"
    filas += f"<tr><th scope='row'>{l['f_ciudad']}</th><td><a href='{ruta_ciudad(e['ciudad'], lang)}'>{esc(c)}</a></td></tr>"
    if e.get('organizador'):
        filas += f"<tr><th scope='row'>{l['f_org']}</th><td>{esc(e['organizador'])}</td></tr>"
    if e.get('precio'):
        filas += f"<tr><th scope='row'>{l['f_precio']}</th><td>{esc(e['precio'])}</td></tr>"
    oficial_txt = re.sub(r'^https?://(www\.)?', '', e['url_oficial']).rstrip('/')[:60]
    filas += f"<tr><th scope='row'>{l['f_oficial']}</th><td><a href='{esc(e['url_oficial'])}' rel='noopener'>{esc(oficial_txt)}</a></td></tr>"
    filas += f"<tr><th scope='row'>{l['f_chequeo']}</th><td>{esc(v)}</td></tr>"
    resumen = esc(e['descripcion']) if e.get('descripcion') else ''
    otros = [x for x in evs if x is not e and x['ciudad'] == e['ciudad'] and x['estado'] != 'solo_terceros'][:5]
    otros_html = ''
    if otros:
        otros_html = f"<h2>{l['mas_t'].format(c=esc(c))}</h2><ul class='eventos'>" + ''.join(item_lista(x, lang) for x in otros) + '</ul>'
    cuerpo = f'''<main class="principal">
<div class="ancho">
<p class="miga"><a href="{BASE[lang]}">{l['eventos']}</a> › <a href="{ruta_ciudad(e['ciudad'], lang)}">{esc(c)}</a></p>
<h1>{esc(n) if est == 'rec' else esc(n) + ' ' + anio}</h1>
{f'<p class="intro">{resumen}</p>' if resumen else ''}
<div class="tabla"><table><tbody>{filas}</tbody></table></div>
<h2>{esc(l['linaje_t'].format(n=n))}</h2>
<div class="ev-linaje"><a href="{GL.url_linaje(lang, lin_id)}"><img src="/img/raza-{lin_id}.webp" alt="{esc(lin['nombre'])}" width="360" height="480" loading="lazy"></a>
<div><p>{TOMA[lang][e['tipo']]}</p><p>{esc(lin['nombre'])}: {esc(lin['resumen'])}.</p><p class="nota">{l['linaje_n']}</p><p><a href="{GL.RUTA[lang]['test']}">{l['test']}</a></p></div></div>
<h2>{l['fuentes_t']}</h2>
<p>{esc(l['fuentes_p'].format(n=n))}</p>
{otros_html}
{GL.cta(lang)}
</div>
</main>
'''
    ld = migas([('Kinstride', INICIO[lang]), (l['eventos'], BASE[lang]), (c, ruta_ciudad(e['ciudad'], lang)), (n, ruta_ev(e, lang))])
    return ruta_ev(e, lang), cabeza(lang, titulo, desc, ruta_ev(e, lang), ld, umami=umami) + GL.barra(lang, OTRA[lang]) + cuerpo + GL.pie(lang, srd)


def pagina_hub(lang, evs, umami, srd):
    l = L[lang]
    por = {c: [e for e in evs if e['ciudad'] == c] for c, d in CIUDADES.items() if d['lang'] == lang}
    ciudades = [c for c in por if len(por[c]) >= MIN_CIUDAD]
    prox = sorted([e for e in evs if CIUDADES[e['ciudad']]['lang'] == lang and clasificar(e) == 'conf' and tiene_pagina(e)], key=lambda e: e['fecha_inicio'] or '9999')[:10]
    tarjetas = ''.join(f'<li><b><a href="{ruta_ciudad(c, lang)}">{esc(CIUDADES[c]["nombre"])}</a></b><br><span class="dato">{esc(l["cuenta"].format(n=len(por[c])))}</span></li>' for c in ciudades)
    prox_html = f'<h2>{l["s_conf"]}</h2><ul class="eventos">' + ''.join(item_lista(e, lang) + '' for e in prox) + '</ul>' if prox else ''
    titulo = titulo_ok(l['hub_t'])
    desc = cortar(l['hub_desc'].format(n=len(ciudades)), 160)
    cuerpo = f'''<main class="principal">
<div class="ancho">
<h1>{l['h_hub']}</h1>
<p class="intro">{l['hub_intro']}</p>
<ul class="eventos ciudades">{tarjetas}</ul>
{prox_html}
<section class="resumen tester"><h2>{l['envia_t']}</h2><p>{l['envia_p']}</p><p class="botones"><a class="boton" href="{ENVIAR[lang]}" data-umami-event="enviar-evento">{l['envia_b']}</a></p></section>
{GL.cta(lang)}
</div>
</main>
'''
    ld = migas([('Kinstride', INICIO[lang]), (l['eventos'], BASE[lang])])
    return BASE[lang], cabeza(lang, titulo, desc, BASE[lang], ld, umami=umami) + GL.barra(lang, OTRA[lang]) + cuerpo + GL.pie(lang, srd)


TIPOS = {'en': [('convention', 'Tabletop / RPG / gaming convention'), ('anime-comic', 'Anime, comic or cosplay'), ('tcg', 'Card tournament or game night'), ('fandom', 'Tolkien, Harry Potter, Dune, fantasy books'), ('faire', 'Faire, LARP or medieval'), ('trek', 'Trek, trail or costume run')],
         'es': [('convention', 'Convención de juegos de mesa / rol'), ('anime-comic', 'Anime, cómics o cosplay'), ('tcg', 'Torneo de cartas o noche de juego'), ('fandom', 'Tolkien, Harry Potter, Dune, libros de fantasía'), ('faire', 'Feria, LARP o medieval'), ('trek', 'Trekking, trail o carrera temática')]}


def pagina_formulario(lang, umami, srd):
    l = L[lang]
    ciudades = ''.join(f'<option value="{c}">{esc(d["nombre"])}</option>' for c, d in CIUDADES.items() if d['lang'] == lang) + f'<option value="otra">{l["otra_ciudad"]}</option>'
    tipos = ''.join(f'<option value="{k}">{esc(t)}</option>' for k, t in TIPOS[lang])
    titulo, desc = titulo_ok(l['f_t']), l['f_desc']
    js = f'''<script>
document.getElementById('ev-form').addEventListener('submit', async function (e) {{
  e.preventDefault();
  var f = e.target, b = f.querySelector('button'), m = document.getElementById('ev-msg');
  var d = Object.fromEntries(new FormData(f).entries());
  b.disabled = true; m.textContent = '';
  try {{
    var r = await fetch('{WEBHOOK}', {{method: 'POST', headers: {{'Content-Type': 'application/json'}}, body: JSON.stringify(d)}});
    if (!r.ok) throw new Error(r.status);
    f.reset(); m.textContent = {json.dumps(l['ok'], ensure_ascii=False)};
  }} catch (x) {{ m.textContent = {json.dumps(l['err'], ensure_ascii=False)}; b.disabled = false; }}
}});
</script>'''
    cuerpo = f'''<main class="principal">
<div class="ancho">
<p class="miga"><a href="{BASE[lang]}">{l['eventos']}</a></p>
<h1>{l['f_h1']}</h1>
<p class="intro">{l['f_intro']}</p>
<form id="ev-form" class="formulario" autocomplete="off">
<label>{l['lb_nombre']}<input name="nombre" required maxlength="120"></label>
<label>{l['lb_url']}<input name="url" type="url" required maxlength="300" placeholder="https://"></label>
<label>{l['lb_ciudad']}<select name="ciudad" required>{ciudades}</select></label>
<label>{l['lb_tipo']}<select name="tipo">{tipos}</select></label>
<label>{l['lb_fecha']}<input name="fecha" required maxlength="120"></label>
<label>{l['lb_msg']}<textarea name="mensaje" rows="3" maxlength="500"></textarea></label>
<label>{l['lb_mail']}<input name="correo" type="email" maxlength="120"></label>
<label class="trampa" aria-hidden="true">Website<input name="web" tabindex="-1" autocomplete="off"></label>
<p class="botones"><button class="boton" type="submit" data-umami-event="enviar-evento-form">{l['enviar']}</button></p>
<p id="ev-msg" role="status"></p>
<p class="nota">{l['priv']} <a href="{PRIV[lang]}">{l['priv_link']}</a>.</p>
<noscript><p>{l['sin_js']}</p></noscript>
</form>
</div>
</main>
{js}
'''
    ld = migas([('Kinstride', INICIO[lang]), (l['eventos'], BASE[lang]), (l['f_h1'], ENVIAR[lang])])
    return ENVIAR[lang], cabeza(lang, titulo, desc, ENVIAR[lang], ld, umami=umami).replace('index, follow', 'noindex, follow') + GL.barra(lang, OTRA[lang]) + cuerpo + GL.pie(lang, srd)


SITIO = 'https://getkinstride.com'


def generar(raiz: Path, sitio: str, umami: str, srd: str) -> list[str]:
    global SITIO
    SITIO = sitio
    datos = json.loads((raiz / 'datos' / 'eventos.json').read_text()) if (raiz / 'datos' / 'eventos.json').exists() else {'eventos': []}
    evs = [e for e in datos['eventos'] if e['ciudad'] in CIUDADES]
    linajes = {lang: json.loads((raiz / 'datos' / f'linajes-{lang}.json').read_text()) for lang in ('en', 'es')}
    urls = []
    import shutil
    for viejo in (raiz / 'events', raiz / 'es' / 'eventos'):  # todo lo que hay aquí es generado: se rehace desde cero
        if viejo.exists():
            shutil.rmtree(viejo)

    def escribir(ruta, contenido):
        d = raiz / ruta.strip('/')
        d.mkdir(parents=True, exist_ok=True)
        (d / 'index.html').write_text(contenido)

    for lang in ('en', 'es'):
        propios = [e for e in evs if CIUDADES[e['ciudad']]['lang'] == lang]
        ruta, h = pagina_hub(lang, evs, umami, srd)
        escribir(ruta, h)
        urls.append(ruta)
        ruta, h = pagina_formulario(lang, umami, srd)
        escribir(ruta, h)  # noindex: no va al mapa del sitio
        for c, d in CIUDADES.items():
            if d['lang'] != lang:
                continue
            de_ciudad = [e for e in propios if e['ciudad'] == c]
            if len(de_ciudad) < MIN_CIUDAD:
                continue
            ruta, h = pagina_ciudad(c, de_ciudad, lang, umami, srd)
            escribir(ruta, h)
            urls.append(ruta)
            for e in de_ciudad:
                if tiene_pagina(e):
                    ruta, h = pagina_evento(e, de_ciudad, lang, umami, srd, linajes[lang])
                    escribir(ruta, h)
                    urls.append(ruta)
    return urls
