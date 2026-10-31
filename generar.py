#!/usr/bin/env python3
"""Genera index.html (inglés) y es/index.html (español) desde un solo molde, para que las dos versiones digan lo mismo.

    python3 generar.py

Hojas de ejemplo y pantallas: ~/Projects/kinstride/scripts/tienda/hojas.mjs
"""
from pathlib import Path

RAIZ = Path(__file__).parent
PLAY = 'https://play.google.com/store/apps/details?id=co.com.monsalve.kinstride'
PRUEBA = 'https://play.google.com/apps/testing/co.com.monsalve.kinstride'
GRUPO = 'https://groups.google.com/g/lince-app-testers'
CORREO = 'lince.revision@gmail.com'
SRD = ('This work includes material from the System Reference Document 5.2 (“SRD 5.2”) by Wizards of the Coast LLC, available at '
       '<a href="https://www.dndbeyond.com/srd">https://www.dndbeyond.com/srd</a>. The SRD 5.2 is licensed under the Creative Commons Attribution 4.0 '
       'International License, available at <a href="https://creativecommons.org/licenses/by/4.0/legalcode">https://creativecommons.org/licenses/by/4.0/legalcode</a>.')
HOJAS = ['orrin', 'mira', 'bruna', 'kael', 'tamsin', 'nettle']

T = {
    'en': dict(
        lang='en', titulo='Kinstride: walking adventure', otro='/es/', otro_nombre='Español',
        priv='/privacy/', borrar='/delete-data/', priv_t='Privacy', borrar_t='Delete your data',
        desc='Your real walks cross a hand-drawn fantasy map, and the way you walk decides who your character becomes. Free, no ads, for Android.',
        h1='Walk. Discover who you become.',
        bajada='Your real steps carry you across a hand-drawn fantasy world, and the way you walk shapes your character: lineage, class, abilities and all.',
        play='Get it on Google Play', ser_tester='Become a tester',
        aviso='In closed testing: for now Google Play only shows it to testers.',
        como_t='How it works',
        como=[('You walk', 'Daily steps count on their own. Walks from your watch count too. Or start an expedition and GPS measures your pace, stride, climbs and rests.'),
              ('The world opens', 'Every step moves your marker across the Farwander. The fog lifts, and every few steps there is a camp with its own illustrated story.'),
              ('You become someone', 'After three expeditions your lineage is revealed. Your habits earn a class. Walk differently and your character changes with you.')],
        pantallas_t='A map, not a dashboard',
        capturas=[('presentacion', 'A short welcome tells you what to expect'), ('mapa', 'The map is your home screen'), ('personaje', 'Your stride, read in a radar'),
                  ('revelacion', 'The reveal after three expeditions'), ('parada', 'Camps with their own story'), ('rutas', 'Choose your road'), ('camino', 'Every camp ahead'), ('logros', '25 achievements')],
        razas_t='Nine lineages. You don’t pick one.',
        razas_p='Kinstride reads the last four weeks of how you walk: pace, stride for your height, climbs, rests, running. Then it tells you who you walk like. And it tells you what to change if you want to become something else.',
        razas=[('mediano', 'Halfling', 'Short, lively steps'), ('enano', 'Dwarf', 'Real climbs'), ('humano', 'Human', 'A bit of everything'),
               ('elfo', 'Elf', 'Quick and even'), ('orco', 'Orc', 'All in, running'), ('arboreo', 'Treefolk', 'Slow, for hours'),
               ('gnomo', 'Gnome', 'Tiny, rapid steps'), ('goliat', 'Goliath', 'Giant strides'), ('ascuano', 'Emberkin', 'Bursts of fire')],
        clases='Twelve classes come from your habits: Ranger, Paladin, Monk, Barbarian, Rogue, Druid, Bard, Fighter, Wizard, Sorcerer, Warlock and Cleric. With 108 portraits, one for each lineage and class.',
        hojas_t='A character sheet you earned',
        hojas_p='Every walker gets a real sheet: your name, level, six abilities built from your walks, and the items you carry. Share it as an image, or take it to your table: it’s compatible with fifth edition.',
        habilidades=[('Strength', 'climbs'), ('Dexterity', 'cadence'), ('Constitution', 'endurance'), ('Intelligence', 'camps found'), ('Wisdom', 'consistency'), ('Charisma', 'walks with others')],
        hojas_n='Example sheets with made-up characters.',
        mundo_t='A journey the size of a legend',
        cifras=[('2,865 km', 'The Long Road, then the way home'), ('657', 'camps, each with a story'), ('103', 'magic items to find'), ('25', 'achievements')],
        mundo_p='Bike rides count as a pony or a horse, a narrator can read each camp aloud, and one rest day a week never breaks your streak.',
        grupo_t='Walk as a Company',
        grupo_p='Up to 9 friends, one marker. Everyone’s steps push the group toward the next place, and you can open each other’s character sheets.',
        pro_t='Free and complete. Pro if you want more.',
        col=('', 'Free', 'Pro'),
        filas=[('Distance, map and camps', 'No limit, no ads', 'No limit, no ads'), ('Lineages', '6', '9, with every variant'), ('Classes', '8', '12, with magic'),
               ('Character sheet', 'Yes', 'With portrait and sharing'), ('Equipment slots', '1', '4'), ('Routes', 'The Long Road and the way home', 'Also separate routes'),
               ('Create a Company', 'Up to 3', 'Up to 9'), ('Postcards', 'With small logo', 'Without logo')],
        pro_n='Pro costs US$9.99 a year, or US$24.99 once for life. Whatever comes next is included.',
        viene_t='On the road ahead',
        viene=['The Hunt: 217 km against the clock', 'The Dragon Road: the other great journey', 'Your stride month by month', 'Training plans to become another lineage'],
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
        desc='Tus caminatas reales cruzan un mapa de fantasía dibujado a mano, y tu forma de caminar decide en quién se convierte tu personaje. Gratis, sin anuncios, para Android.',
        h1='Camina. Descubre en quién te conviertes.',
        bajada='Tus pasos reales te llevan por un mundo de fantasía dibujado a mano, y tu forma de caminar va formando a tu personaje: linaje, clase y habilidades.',
        play='Disponible en Google Play', ser_tester='Ser tester',
        aviso='En prueba cerrada: por ahora Google Play solo la muestra a los testers.',
        como_t='Cómo funciona',
        como=[('Caminas', 'Tus pasos del día cuentan solos, y las caminatas de tu reloj también. O inicia una expedición y el GPS mide tu ritmo, tu paso, las subidas y los descansos.'),
              ('El mundo se abre', 'Cada paso mueve tu marcador por Las Tierras Lejanas. La niebla se levanta y, cada poco, aparece una parada con su propia historia ilustrada.'),
              ('Te conviertes en alguien', 'Tras tres expediciones se revela tu linaje. Tus costumbres te ganan una clase. Si caminas distinto, tu personaje cambia contigo.')],
        pantallas_t='Un mapa, no un tablero de números',
        capturas=[('presentacion', 'Una bienvenida corta te dice qué esperar'), ('mapa', 'El mapa es tu pantalla principal'), ('personaje', 'Tu paso, leído en un radar'),
                  ('revelacion', 'La revelación tras tres expediciones'), ('parada', 'Paradas con su historia'), ('rutas', 'Elige tu camino'), ('camino', 'Cada parada que viene'), ('logros', '25 logros')],
        razas_t='Nueve linajes. Tú no eliges.',
        razas_p='Kinstride lee cómo caminaste las últimas cuatro semanas: ritmo, largo del paso para tu estatura, subidas, descansos y trote. Luego te dice a quién te pareces. Y también qué cambiar si quieres ser otra cosa.',
        razas=[('mediano', 'Mediano', 'Pasos cortos y vivos'), ('enano', 'Enano', 'Subidas de verdad'), ('humano', 'Humano', 'Un poco de todo'),
               ('elfo', 'Elfo', 'Rápido y parejo'), ('orco', 'Orco', 'A fondo, trotando'), ('arboreo', 'Arbóreo', 'Lento, por horas'),
               ('gnomo', 'Gnomo', 'Pasitos rapidísimos'), ('goliat', 'Goliat', 'Zancadas gigantes'), ('ascuano', 'Ascuano', 'Arranques de fuego')],
        clases='Doce clases salen de tus costumbres: Explorador, Paladín, Monje, Bárbaro, Pícaro, Druida, Bardo, Guerrero, Mago, Hechicero, Brujo y Clérigo. Son 108 retratos, uno por cada linaje y clase.',
        hojas_t='Una hoja de personaje que te ganaste',
        hojas_p='Cada caminante tiene una hoja de verdad: tu nombre, tu nivel, seis habilidades que salen de tus caminatas y los objetos que llevas. Compártela como imagen o llévala a tu mesa: es compatible con quinta edición.',
        habilidades=[('Fuerza', 'subidas'), ('Destreza', 'cadencia'), ('Constitución', 'resistencia'), ('Inteligencia', 'paradas halladas'), ('Sabiduría', 'constancia'), ('Carisma', 'salidas en grupo')],
        hojas_n='Hojas de ejemplo con personajes inventados.',
        mundo_t='Un viaje del tamaño de una leyenda',
        cifras=[('2.865 km', 'El Gran Viaje, y luego el regreso'), ('657', 'paradas, cada una con su historia'), ('103', 'objetos mágicos por encontrar'), ('25', 'logros')],
        mundo_p='La bicicleta cuenta como pony o caballo, un narrador puede leer cada parada en voz alta, y un día de descanso a la semana nunca corta tu racha.',
        grupo_t='Camina en Compañía',
        grupo_p='Hasta 9 amigos, un solo marcador. Los pasos de todos empujan al grupo hacia el próximo lugar, y pueden abrir la hoja de personaje de cada uno.',
        pro_t='Gratis y completa. Pro si quieres más.',
        col=('', 'Gratis', 'Pro'),
        filas=[('Distancia, mapa y paradas', 'Sin límite, sin anuncios', 'Sin límite, sin anuncios'), ('Linajes', '6', '9, con todas las variantes'), ('Clases', '8', '12, con magia'),
               ('Hoja de personaje', 'Sí', 'Con retrato y para compartir'), ('Casillas de equipo', '1', '4'), ('Rutas', 'El Gran Viaje y el regreso', 'También rutas aparte'),
               ('Crear una Compañía', 'Hasta 3', 'Hasta 9'), ('Postales', 'Con logo pequeño', 'Sin logo')],
        pro_n='Pro cuesta US$9,99 al año, o US$24,99 una sola vez para siempre. Lo que venga después está incluido.',
        viene_t='Lo que viene en el camino',
        viene=['La Cacería: 217 km contra el reloj', 'El Camino del Dragón: el otro gran viaje', 'Tu paso mes a mes', 'Planes de entrenamiento para llegar a otro linaje'],
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
    url = 'https://kinstride.monsalve.com.co' + ('/es/' if l == 'es' else '/')
    img_hoja = lambda n, extra='': f'<img src="/img/{l}-hoja-{n}.webp" alt="" width="720" height="1272" {extra}>'
    capturas = '\n'.join(
        f'<figure><img src="/img/{l}-{n}.webp" alt="{txt}" width="480" height="839" loading="lazy"><figcaption>{txt}</figcaption></figure>'
        for n, txt in t['capturas'])
    como = ''.join(f'<li><h3>{h}</h3><p>{p}</p></li>' for h, p in t['como'])
    razas = ''.join(
        f'<figure><img src="/img/raza-{r}.webp" alt="{n}" width="360" height="480" loading="lazy"><figcaption><b>{n}</b>{d}</figcaption></figure>' for r, n, d in t['razas'])
    habilidades = ''.join(f'<li><b>{a}</b> {m}</li>' for a, m in t['habilidades'])
    hojas = ''.join(f'<figure>{img_hoja(n, "loading=lazy")}</figure>' for n in HOJAS)
    cifras = ''.join(f'<div><b>{n}</b><span>{d}</span></div>' for n, d in t['cifras'])
    filas = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in t['filas'])
    viene = ''.join(f'<li>{x}</li>' for x in t['viene'])
    pasos = ''.join(f'<li>{p}</li>' for p in t['pasos'])
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
<body class="portada">
<header class="heroe">
<div class="heroe-dentro">
<div class="heroe-texto">
<img class="icono" src="/img/icono.png" alt="" width="80" height="80">
<span class="marca">KINSTRIDE</span>
<h1>{t['h1']}</h1>
<p class="bajada">{t['bajada']}</p>
<p class="botones"><a class="boton" href="{PLAY}">{t['play']}</a> <a class="boton secundario" href="#tester">{t['ser_tester']}</a></p>
<p class="aviso">{t['aviso']}</p>
</div>
<div class="abanico" aria-hidden="true">{img_hoja('kael')}{img_hoja('orrin')}{img_hoja('mira')}</div>
</div>
</header>
<main class="ancho">
<section class="como"><h2>{t['como_t']}</h2><ol class="camino">{como}</ol></section>
<section class="amplia"><h2>{t['pantallas_t']}</h2></section>
<div class="galeria">
{capturas}
</div>
<section class="amplia"><h2>{t['razas_t']}</h2><p class="intro">{t['razas_p']}</p><div class="razas">{razas}</div><p class="intro">{t['clases']}</p></section>
<section class="amplia hojas-sec"><h2>{t['hojas_t']}</h2><p class="intro">{t['hojas_p']}</p><ul class="habilidades">{habilidades}</ul></section>
<div class="hojas">{hojas}</div>
<p class="nota centro">{t['hojas_n']}</p>
</main>
<section class="banda"><div class="banda-dentro"><h2>{t['mundo_t']}</h2><div class="cifras">{cifras}</div><p>{t['mundo_p']}</p></div></section>
<main class="ancho">
<section class="amplia"><h2>{t['grupo_t']}</h2><p class="intro">{t['grupo_p']}</p></section>
<section class="amplia"><h2>{t['pro_t']}</h2><div class="tabla"><table><thead><tr><th>{t['col'][0]}</th><th>{t['col'][1]}</th><th>{t['col'][2]}</th></tr></thead><tbody>{filas}</tbody></table></div><p class="nota">{t['pro_n']}</p></section>
<section class="amplia"><h2>{t['viene_t']}</h2><ul class="viene">{viene}</ul></section>
<section id="tester" class="resumen tester"><h2>{t['tester_t']}</h2><p>{t['tester_intro']}</p><ol>{pasos}</ol><p class="nota">{t['tester_nota']}</p></section>
<p class="pie"><a href="{t['priv']}">{t['priv_t']}</a> · <a href="{t['borrar']}">{t['borrar_t']}</a> · <a href="{t['otro']}">{t['otro_nombre']}</a></p>
<p class="pie legal">{SRD}</p>
</main>
</body>
</html>
'''


(RAIZ / 'index.html').write_text(pagina(T['en']))
(RAIZ / 'es' / 'index.html').write_text(pagina(T['es']))
print('index.html y es/index.html listos')
