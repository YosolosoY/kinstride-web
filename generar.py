#!/usr/bin/env python3
"""Genera index.html (inglés) y es/index.html (español) desde un solo molde, para que las dos versiones digan lo mismo.

    python3 generar.py
"""
from pathlib import Path

RAIZ = Path(__file__).parent
PLAY = 'https://play.google.com/store/apps/details?id=co.com.monsalve.kinstride'
PRUEBA = 'https://play.google.com/apps/testing/co.com.monsalve.kinstride'
GRUPO = 'https://groups.google.com/g/lince-app-testers'
CORREO = 'lince.revision@gmail.com'

T = {
    'en': dict(
        lang='en', titulo='Kinstride: walking adventure', otro='/es/', otro_nombre='Español',
        priv='/privacy/', borrar='/delete-data/', priv_t='Privacy', borrar_t='Delete your data',
        desc='Your real steps travel a hand-drawn fantasy map, and the way you walk reveals your lineage. Free, no ads, for Android.',
        h1='Every step takes you farther',
        bajada='Your real kilometres travel across the Farwander, a hand-drawn world of legendary roads. And the way you walk reveals your lineage: dwarf, elf, halfling…',
        play='Get it on Google Play', ser_tester='Become a tester',
        aviso='Kinstride is in closed testing. While it lasts, Google Play only shows it to testers: see how to join below.',
        capturas=[('mapa', 'The map moves as you walk'), ('personaje', 'Your stride reveals your lineage'), ('parada', '657 camps with their own story'),
                  ('camino', 'Every camp on the road ahead'), ('logros', '22 achievements'), ('semana', 'Daily goal, streak and week'), ('resumen', 'Expeditions with GPS')],
        secciones=[
            ('A journey the size of a legend', [
                'The Long Road is 2,865 km, from the quiet farms of Hearthvale to the Cinder Peak, and then the Road Home.',
                '657 camps along the way, each with its own illustrated story, and 10 great landmarks.',
                'Beyond the next landmark, the map stays hidden in fog until you get there.']),
            ('Walk as you always do', [
                'Your daily steps from Health Connect move you forward on their own.',
                'Walks, runs and hikes from your watch (Samsung Health, Google Fit, Garmin and more) count too.',
                'Or start an expedition: GPS measures your pace, stride, climbs and rests. Your exact route never leaves your phone.']),
            ('Your stride reveals your lineage', [
                'Steady and loves the climbs? Dwarf. Quick and light? Elf. Short steps with plenty of stops? Halfling.',
                'Nine lineages, read from your last 4 weeks: walk differently and your lineage changes.',
                'Level up from 1 to 20, from Doorstep Wanderer to The Unwearied.']),
            ('Keep going', [
                'A daily goal in steps or distance, with a streak.',
                'A weekly summary compared with last week.',
                '22 achievements: your first campfire, a half marathon, a week on the road and more.',
                'Walk as a Company with friends or family: your kilometres move you together along the same road.']),
        ],
        precio_t='Free and complete',
        precio='No ads and no distance limit. <b>Kinstride Pro</b> (US$9.99 a year, or US$24.99 once for life) adds the three rare lineages (Gnome, Goliath and Emberkin), larger companies, special postcards and everything that comes next.',
        tester_t='Become a tester',
        tester_intro='Before Kinstride opens to everyone, Google asks for people to test it for 14 days. You need an Android phone and the Gmail account you use on Play Store.',
        pasos=[
            f'Join the test group with that Gmail account: <a href="{GRUPO}">groups.google.com/g/lince-app-testers</a> → <b>Join group</b>.',
            f'On your Android phone, open <a href="{PRUEBA}">the Kinstride test on Google Play</a> → <b>Become a tester</b>.',
            f'Install Kinstride from <a href="{PLAY}">Google Play</a> and <b>keep it installed for 14 days</b>. Walk as usual; one expedition helps a lot.',
            f'Tell us what you think, or anything that fails: <b>{CORREO}</b>',
        ],
        tester_nota='If step 2 says the app is not available, wait a few minutes after joining the group and try again.',
    ),
    'es': dict(
        lang='es', titulo='Kinstride: aventura a pie', otro='/', otro_nombre='English',
        priv='/es/privacidad/', borrar='/es/borrar-datos/', priv_t='Privacidad', borrar_t='Borrar tus datos',
        desc='Tus pasos reales recorren un mapa de fantasía dibujado a mano, y tu forma de caminar revela tu linaje. Gratis, sin anuncios, para Android.',
        h1='Cada paso te lleva más lejos',
        bajada='Tus kilómetros de verdad avanzan por Las Tierras Lejanas, un mundo dibujado a mano lleno de caminos legendarios. Y tu forma de caminar revela tu linaje: enano, elfo, mediano…',
        play='Disponible en Google Play', ser_tester='Ser tester',
        aviso='Kinstride está en prueba cerrada. Mientras dure, Google Play solo la muestra a los testers: abajo te contamos cómo sumarte.',
        capturas=[('mapa', 'El mapa avanza mientras caminas'), ('personaje', 'Tu paso revela tu linaje'), ('parada', '657 paradas con su historia'),
                  ('camino', 'Cada parada del camino que viene'), ('logros', '22 logros'), ('semana', 'Meta diaria, racha y semana'), ('resumen', 'Expediciones con GPS')],
        secciones=[
            ('Un viaje del tamaño de una leyenda', [
                'El Gran Viaje mide 2.865 km, desde las granjas tranquilas de Valleapacible hasta el Pico de Ceniza, y luego El Regreso.',
                '657 paradas en el camino, cada una con su historia ilustrada, y 10 grandes lugares.',
                'Más allá del próximo lugar, el mapa sigue cubierto de niebla hasta que llegas.']),
            ('Camina como siempre', [
                'Tus pasos de cada día, desde Health Connect, te hacen avanzar solos.',
                'Las caminatas, carreras y salidas de senderismo de tu reloj (Samsung Health, Google Fit, Garmin y más) también cuentan.',
                'O sal de expedición: el GPS mide tu ritmo, tu paso, las subidas y los descansos. Tu ruta exacta nunca sale de tu teléfono.']),
            ('Tu forma de caminar revela tu linaje', [
                '¿Firme y te gustan las subidas? Enano. ¿Rápido y liviano? Elfo. ¿Pasos cortos y muchas paradas? Mediano.',
                'Nueve linajes, según tus últimas 4 semanas: si cambias tu forma de caminar, cambia tu linaje.',
                'Sube del nivel 1 al 20, de Andariego del Umbral a El Incansable.']),
            ('Sigue adelante', [
                'Meta diaria en pasos o distancia, con racha.',
                'Resumen de la semana comparado con la anterior.',
                '22 logros: tu primera fogata, una media maratón, una semana en el camino y más.',
                'Camina en Compañía con amigos o familia: sus kilómetros avanzan juntos por el mismo camino.']),
        ],
        precio_t='Gratis y completa',
        precio='Sin anuncios y sin límite de distancia. <b>Kinstride Pro</b> (US$9,99 al año, o US$24,99 una sola vez para siempre) suma los tres linajes raros (Gnomo, Goliat y Ascuano), compañías más grandes, postales especiales y todo lo que viene.',
        tester_t='Ser tester',
        tester_intro='Antes de abrir Kinstride para todos, Google pide que algunas personas la prueben durante 14 días. Necesitas un teléfono Android y la cuenta de Gmail que usas en Play Store.',
        pasos=[
            f'Únete al grupo de prueba con esa cuenta de Gmail: <a href="{GRUPO}">groups.google.com/g/lince-app-testers</a> → <b>Unirse al grupo</b>.',
            f'En tu teléfono Android, abre <a href="{PRUEBA}">la prueba de Kinstride en Google Play</a> → <b>Convertirse en tester</b>.',
            f'Instala Kinstride desde <a href="{PLAY}">Google Play</a> y <b>déjala instalada 14 días</b>. Camina como siempre; una expedición ayuda mucho.',
            f'Cuéntanos qué te parece, o cualquier cosa que falle: <b>{CORREO}</b>',
        ],
        tester_nota='Si el paso 2 dice que la app no está disponible, espera unos minutos después de unirte al grupo y vuelve a intentarlo.',
    ),
}


def pagina(t: dict) -> str:
    l = t['lang']
    capturas = '\n'.join(
        f'<figure><img src="/img/{l}-{n}.webp" alt="{txt}" width="480" height="839" loading="lazy"><figcaption>{txt}</figcaption></figure>'
        for n, txt in t['capturas'])
    secciones = '\n'.join(
        f'<section><h2>{h}</h2><ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul></section>' for h, items in t['secciones'])
    pasos = ''.join(f'<li>{p}</li>' for p in t['pasos'])
    url = 'https://kinstride.monsalve.com.co' + ('/es/' if l == 'es' else '/')
    return f'''<!doctype html>
<html lang="{l}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['titulo']}</title>
<meta name="description" content="{t['desc']}">
<meta property="og:title" content="{t['titulo']}">
<meta property="og:description" content="{t['desc']}">
<meta property="og:image" content="https://kinstride.monsalve.com.co/img/compartir.png">
<meta property="og:url" content="{url}">
<link rel="icon" href="/favicon.png">
<link rel="alternate" hreflang="en" href="https://kinstride.monsalve.com.co/">
<link rel="alternate" hreflang="es" href="https://kinstride.monsalve.com.co/es/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&family=IM+Fell+English+SC&family=Alegreya+Sans:wght@500;700&display=swap">
<link rel="stylesheet" href="/estilo.css">
</head>
<body>
<main class="ancho">
<header class="cabeza">
<img class="icono" src="/img/icono.png" alt="" width="80" height="80">
<span class="marca">KINSTRIDE</span>
<h1>{t['h1']}</h1>
<p class="bajada">{t['bajada']}</p>
<p class="botones"><a class="boton" href="{PLAY}">{t['play']}</a> <a class="boton secundario" href="#tester">{t['ser_tester']}</a></p>
<p class="aviso">{t['aviso']}</p>
</header>
<div class="galeria">
{capturas}
</div>
{secciones}
<section><h2>{t['precio_t']}</h2><p>{t['precio']}</p></section>
<section id="tester" class="resumen tester"><h2>{t['tester_t']}</h2><p>{t['tester_intro']}</p><ol>{pasos}</ol><p class="nota">{t['tester_nota']}</p></section>
<p class="pie"><a href="{t['priv']}">{t['priv_t']}</a> · <a href="{t['borrar']}">{t['borrar_t']}</a> · <a href="{t['otro']}">{t['otro_nombre']}</a></p>
</main>
</body>
</html>
'''


(RAIZ / 'index.html').write_text(pagina(T['en']))
(RAIZ / 'es' / 'index.html').write_text(pagina(T['es']))
print('index.html y es/index.html listos')
