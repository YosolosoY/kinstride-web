"""Test de linajes y una página por linaje, en inglés y español. Lo llama generar.py.

Reglas, nombres y metas salen de datos/linajes-*.json (exportado desde la app con scripts/tienda/linajes-sitio.ts):
aquí solo van los textos propios del sitio.
"""
import json
import re
from pathlib import Path

TIKTOK = 'https://www.tiktok.com/@kinstrideapp'
SLUG = {'en': {'mediano': 'halfling', 'enano': 'dwarf', 'humano': 'human', 'elfo': 'elf', 'orco': 'orc', 'arboreo': 'barkfolk', 'gnomo': 'gnome', 'goliat': 'goliath', 'ascuano': 'emberkin'},
        'es': {'mediano': 'mediano', 'enano': 'enano', 'humano': 'humano', 'elfo': 'elfo', 'orco': 'orco', 'arboreo': 'arboreo', 'gnomo': 'gnomo', 'goliat': 'goliat', 'ascuano': 'ascuano'}}
RUTA = {'en': {'inicio': '/', 'test': '/test/', 'linajes': '/lineages/'}, 'es': {'inicio': '/es/', 'test': '/es/test/', 'linajes': '/es/linajes/'}}
ORDEN = ['mediano', 'enano', 'humano', 'elfo', 'orco', 'arboreo', 'gnomo', 'goliat', 'ascuano']

# Cada respuesta es una estimación de las medidas de la app, en sus mismas unidades.
RESPUESTAS = [
    [{'velocidadMejor': 3.7}, {'velocidadMejor': 4.6}, {'velocidadMejor': 5.4}, {'velocidadMejor': 6.2}],
    [{'zancada': .38, 'cadencia': 135}, {'zancada': .40, 'cadencia': 108}, {'zancada': .445, 'cadencia': 115}, {'zancada': .49, 'cadencia': 112}, {'zancada': .56, 'cadencia': 105}],
    [{'duracion': 25}, {'duracion': 50}, {'duracion': 90}, {'duracion': 150}],
    [{'pausasPorHora': .3}, {'pausasPorHora': 1}, {'pausasPorHora': 2.5}, {'pausasPorHora': 4.5}],
    [{'desnivelPorKm': 2}, {'desnivelPorKm': 10}, {'desnivelPorKm': 18}, {'desnivelPorKm': 28}],
    [{'variacion': .03}, {'variacion': .055}, {'variacion': .11}, {'variacion': .22}],
    [{'trote': 0}, {'trote': .1}, {'trote': .4}, {'trote': .85}],
    [{'constancia': .25, 'salidas': 6}, {'constancia': .5, 'salidas': 12}, {'constancia': .8, 'salidas': 18}, {'constancia': .95, 'salidas': 24}],
]

T = {
    'en': dict(
        marca='Kinstride home', pag_desc='{resumen}. How {art} walks, what Kinstride measures and a free lineage test.', nav_test='Walking test', nav_linajes='Lineages', otro='Español', tester='Become a tester', tester_url='/#tester',
        priv=('/privacy/', 'Privacy'), borrar=('/delete-data/', 'Delete your data'),
        test_titulo='Which Fantasy Lineage Do You Walk Like? Free Test | Kinstride',
        test_desc='Answer 8 questions about how you walk and find out if you walk like an Elf, a Dwarf, a Goliath or something rarer. Free, with no sign-up.',
        test_h1='Which lineage do you walk like?', test_intro='Eight questions about how you really walk. One minute, no sign-up, and the answer comes from the same rules the Kinstride app uses on real walks.',
        empezar='Start the test', sin_js='This test needs JavaScript. You can still read about the nine lineages.',
        faq_t='About this test',
        faq=[('How does it work?', 'Each answer estimates something Kinstride measures on a walk, like pace, stride or climb. Those estimates go through the rules of the app, and the lineage closest to you wins.'),
             ('Is it as accurate as the app?', 'No. The test trusts your memory. The app measures four weeks of real walks with GPS and your steps, so your lineage there may be different, and it can change when your walking changes.'),
             ('Do you save my answers?', 'No. Your answers stay in your browser. We only count how many people start the test and which lineage they got, with no name and no cookies.')],
        preguntas=[
            ('On an ordinary walk, your pace is…', ['Unhurried. People pass me', 'Relaxed, a normal stroll', 'Brisk, like I have somewhere to be', 'Fast. I pass almost everyone']),
            ('For your height, your steps are…', ['Tiny and very quick', 'Short and relaxed', 'About average', 'Long', 'Huge. Friends need extra steps to keep up']),
            ('A typical walk lasts…', ['Under 30 minutes', 'Around 50 minutes', 'An hour and a half', 'Two hours or more']),
            ('How often do you stop?', ['Almost never', 'Once in a while', 'A few times an hour', 'All the time. There is so much to see']),
            ('Hills on your walks?', ['Flat, please', 'A few slopes', 'I look for them', 'The steeper the better']),
            ('From start to finish, your rhythm…', ['Never changes', 'Barely changes', 'Depends on my mood', 'Comes in bursts: fast, slow, fast']),
            ('Do you run?', ['Never', 'A few steps now and then', 'I mix running and walking', 'I run most of the way']),
            ('How often do you go out?', ['One or two days a week', 'Three or four days a week', 'Most days', 'Every day']),
        ],
        pregunta='Question', atras='← Back', caminas='You walk like {}', ver='More about the {}', compartir='Share my result', copiado='Link copied', repetir='Take it again',
        raro='A rare lineage: in the app, Pro reveals it.', estimado='An estimate from your answers. The app reads your real walks, so it may tell you something else.',
        texto_compartir='I walk like {}. Which lineage do you walk like?',
        linajes_titulo='The 9 Fantasy Lineages of Kinstride, by Walking Style',
        linajes_desc='Halfling, Dwarf, Human, Elf, Orc, Barkfolk, Gnome, Goliath and Emberkin: how each one walks, and what the Kinstride walking RPG measures.',
        linajes_h1='Nine lineages, nine ways of walking', linajes_intro='You don’t pick your lineage in Kinstride. The app reads four weeks of your walks and tells you who you walk like. When your walking changes, your lineage changes too.',
        test_cta='Take the walking test', test_cta_p='Not sure which one is yours?', mide_t='What the app measures', mide_p='These are the marks that give full score, taken straight from the rules of the app. You get partial score on the way there.',
        col=('Measure', 'Full score at'), llave='the key', llave_p='Without the key measure there is no {}, whatever the rest says.',
        variantes_t='Variants', variantes_p='With Pro, where and how you walk can make you a variant:', otros_t='The other lineages', raro_pag='A rare lineage. Kinstride calculates it for everyone; Pro reveals it.', gratis_pag='One of the six lineages open to everyone.', intro_miga='Lineages',
        tester_p='Kinstride is in closed testing on Android. Test it for 14 days and see what your real walks say.',
    ),
    'es': dict(
        marca='Inicio de Kinstride', pag_desc='{resumen}. Cómo camina {art}, qué mide Kinstride y un test gratis de linajes.', nav_test='Test de caminar', nav_linajes='Linajes', otro='English', tester='Ser tester', tester_url='/es/#tester',
        priv=('/es/privacidad/', 'Privacidad'), borrar=('/es/borrar-datos/', 'Borrar tus datos'),
        test_titulo='Test: ¿a qué linaje te pareces al caminar? | Kinstride',
        test_desc='Responde 8 preguntas sobre cómo caminas y descubre si caminas como un Elfo, un Enano, un Goliat o algo más raro. Gratis y sin registro.',
        test_h1='¿A qué linaje te pareces al caminar?', test_intro='Ocho preguntas sobre cómo caminas de verdad. Un minuto, sin registro, y el resultado sale de las mismas reglas que la app de Kinstride usa con caminatas reales.',
        empezar='Empezar el test', sin_js='Este test necesita JavaScript. Igual puedes leer sobre los nueve linajes.',
        faq_t='Sobre este test',
        faq=[('¿Cómo funciona?', 'Cada respuesta estima algo que Kinstride mide en una caminata, como el ritmo, el paso o la subida. Esas estimaciones pasan por las reglas de la app, y gana el linaje más cercano a ti.'),
             ('¿Es tan preciso como la app?', 'No. El test confía en tu memoria. La app mide cuatro semanas de caminatas reales con GPS y tus pasos, así que allí tu linaje puede ser otro, y puede cambiar cuando cambie tu forma de caminar.'),
             ('¿Guardan mis respuestas?', 'No. Tus respuestas se quedan en tu navegador. Solo contamos cuántas personas empiezan el test y qué linaje obtuvieron, sin nombre y sin cookies.')],
        preguntas=[
            ('En una caminata normal, tu ritmo es…', ['Sin apuro. Me pasa todo el mundo', 'Tranquilo, de paseo', 'Ágil, como si fuera a alguna parte', 'Rápido. Paso a casi todos']),
            ('Para tu estatura, tus pasos son…', ['Cortitos y muy rápidos', 'Cortos y tranquilos', 'Normales', 'Largos', 'Enormes. A mi lado hay que dar pasos de más']),
            ('Una salida típica dura…', ['Menos de 30 minutos', 'Unos 50 minutos', 'Una hora y media', 'Dos horas o más']),
            ('¿Cada cuánto te detienes?', ['Casi nunca', 'De vez en cuando', 'Varias veces por hora', 'Todo el tiempo. Hay mucho que ver']),
            ('¿Subidas en tus caminatas?', ['Plano, por favor', 'Algunas cuestas', 'Las busco', 'Mientras más empinado, mejor']),
            ('De principio a fin, tu ritmo…', ['No cambia', 'Casi no cambia', 'Depende de mi ánimo', 'Va a rachas: rápido, lento, rápido']),
            ('¿Trotas?', ['Nunca', 'Unos pasos de vez en cuando', 'Mezclo trote y caminata', 'Troto casi todo el camino']),
            ('¿Cada cuánto sales?', ['Uno o dos días a la semana', 'Tres o cuatro días a la semana', 'Casi todos los días', 'Todos los días']),
        ],
        pregunta='Pregunta', atras='← Atrás', caminas='Caminas como {}', ver='Más sobre el {}', compartir='Compartir mi resultado', copiado='Enlace copiado', repetir='Repetir el test',
        raro='Un linaje raro: en la app lo revela Pro.', estimado='Es una estimación con tus respuestas. La app lee tus caminatas reales, así que puede decirte otra cosa.',
        texto_compartir='Camino como {}. ¿A qué linaje te pareces tú?',
        linajes_titulo='Los 9 linajes de fantasía de Kinstride, según cómo caminas',
        linajes_desc='Mediano, Enano, Humano, Elfo, Orco, Arbóreo, Gnomo, Goliat y Ascuano: cómo camina cada uno y qué mide Kinstride, el juego de rol para caminar.',
        linajes_h1='Nueve linajes, nueve formas de caminar', linajes_intro='En Kinstride no eliges tu linaje. La app lee cuatro semanas de tus caminatas y te dice a quién te pareces. Si cambia tu forma de caminar, tu linaje cambia contigo.',
        test_cta='Hacer el test', test_cta_p='¿No sabes cuál es el tuyo?', mide_t='Qué mide la app', mide_p='Estas son las marcas que dan el puntaje completo, tomadas directamente de las reglas de la app. Antes de llegar a ellas sumas una parte.',
        col=('Medida', 'Puntaje completo'), llave='la llave', llave_p='Sin la medida llave no hay {}, diga lo que diga el resto.',
        variantes_t='Variantes', variantes_p='Con Pro, dónde y cómo caminas puede volverte una variante:', otros_t='Los otros linajes', raro_pag='Un linaje raro. Kinstride lo calcula para todos; Pro lo revela.', gratis_pag='Uno de los seis linajes abiertos a todos.', intro_miga='Linajes',
        tester_p='Kinstride está en prueba cerrada en Android. Pruébala 14 días y mira qué dicen tus caminatas reales.',
    ),
}

C = {
    'mediano': {'en': dict(art='a Halfling', titulo='Walk Like a Halfling: Short, Lively Steps', uno='Halflings are in no hurry, and the road is better for it. Their stride is short for their height, their walks rarely pass the hour, and there is always a reason to stop: a bakery, a dog, a view, a bench that looks underused.', dos='Short steps come first. Without them there is no Halfling, however many stops you make. Daytime strolls and frequent pauses then say how Halfling you really are.'),
                'es': dict(art='un Mediano', titulo='Camina como un Mediano: pasos cortos y vivos', uno='Los medianos no tienen prisa, y el camino lo agradece. Su paso es corto para su estatura, sus salidas rara vez pasan de la hora y siempre hay un motivo para parar: una panadería, un perro, una vista, una banca que parece desaprovechada.', dos='Lo primero es el paso corto. Sin él no hay Mediano, por muchas paradas que hagas. Los paseos de día y las pausas frecuentes dicen después qué tan Mediano eres.')},
    'enano': {'en': dict(art='a Dwarf', titulo='Walk Like a Dwarf: Steady Up Every Climb', uno='Dwarves do not mind the hill. They prefer it. Their walks climb, their pace barely changes from the bottom to the top, and they stay out long after others have turned back.', dos='Climbing comes first. Without real ascent there is no Dwarf. An even pace and long outings then add to it.'),
              'es': dict(art='un Enano', titulo='Camina como un Enano: firme en cada subida', uno='A los enanos no les molesta la subida: la prefieren. Sus salidas trepan, su ritmo casi no cambia de abajo hacia arriba y siguen afuera cuando otros ya dieron la vuelta.', dos='Lo primero es subir. Sin desnivel de verdad no hay Enano. El ritmo parejo y las salidas largas suman después.')},
    'humano': {'en': dict(art='a Human', titulo='Walk Like a Human: The Hardest Lineage to Earn', uno='Humans refuse to be just one thing. A hard climb one day, a fast walk the next, a long outing on Saturday, a run when nobody expected it.', dos='This is the hardest lineage in Kinstride. It asks for four different feats within four weeks, plenty of outings and steady habits. Nobody starts as a Human: you have to walk your way there.'),
               'es': dict(art='un Humano', titulo='Camina como un Humano: el linaje más difícil', uno='Los humanos se niegan a ser una sola cosa. Una subida dura un día, una caminata rápida al siguiente, una salida larga el sábado y un trote cuando nadie lo esperaba.', dos='Es el linaje más difícil de Kinstride. Pide cuatro hazañas distintas en cuatro semanas, muchas salidas y costumbres firmes. Nadie empieza como Humano: hay que llegar caminando.')},
    'elfo': {'en': dict(art='an Elf', titulo='Walk Like an Elf: Quick, Light and Even', uno='Elves seem to cover ground without trying. Their pace is quick, it hardly changes from one stretch to the next, and they come back to the road almost every day.', dos='Speed comes first. Without a quick walking pace there is no Elf. An even rhythm and steady days then say how Elf you really are.'),
             'es': dict(art='un Elfo', titulo='Camina como un Elfo: rápido, liviano y parejo', uno='Los elfos parecen avanzar sin esfuerzo. Su ritmo es rápido, casi no cambia de un tramo a otro y vuelven al camino casi todos los días.', dos='Lo primero es la velocidad. Sin un ritmo rápido al caminar no hay Elfo. El ritmo parejo y la constancia dicen después qué tan Elfo eres.')},
    'orco': {'en': dict(art='an Orc', titulo='Move Like an Orc: All In, Running', uno='Orcs do not stroll. They run most of the way, and they run hard from the first minute to the last.', dos='Running comes first: without it there is no Orc. Overall speed and a sustained effort then show how strong that run really is.'),
             'es': dict(art='un Orco', titulo='Muévete como un Orco: a fondo, trotando', uno='Los orcos no pasean. Trotan casi todo el camino, y fuerte, del primer minuto al último.', dos='Lo primero es trotar: sin eso no hay Orco. La velocidad total y el esfuerzo sostenido muestran después qué tan fuerte es ese trote.')},
    'arboreo': {'en': dict(art='Barkfolk', titulo='Walk Like Barkfolk: Slow, for Hours', uno='Barkfolk are slow to start and slower to stop. Their walking pace is unhurried, their outings last for hours, and they rarely pause, because nothing about the road makes them tired.', dos='An unhurried pace comes first. Without it there are no Barkfolk. Long outings with very few stops then deepen the roots.'),
                'es': dict(art='un Arbóreo', titulo='Camina como un Arbóreo: lento, por horas', uno='Los arbóreos tardan en arrancar y tardan más en detenerse. Caminan sin apuro, sus salidas duran horas y casi no paran, porque el camino no los cansa.', dos='Lo primero es el ritmo sin apuro. Sin él no hay Arbóreo. Las salidas largas con muy pocas paradas hunden después las raíces.')},
    'gnomo': {'en': dict(art='a Gnome', titulo='Walk Like a Gnome: Tiny, Rapid Steps', uno='Gnomes take more steps than anyone else on the road. Their stride is very short for their height and their cadence is very high, as if their feet had something urgent to tell the ground.', dos='Kinstride reads only two things here: how short your stride is and how many steps you take per minute.'),
              'es': dict(art='un Gnomo', titulo='Camina como un Gnomo: pasitos rapidísimos', uno='Los gnomos dan más pasos que nadie en el camino. Su paso es muy corto para su estatura y su cadencia es muy alta, como si los pies tuvieran algo urgente que decirle al suelo.', dos='Kinstride mira solo dos cosas: qué tan corto es tu paso y cuántos pasos das por minuto.')},
    'goliat': {'en': dict(art='a Goliath', titulo='Walk Like a Goliath: Giant Strides', uno='Goliaths cover in one step what others need two for. Height is not the point: Kinstride compares your stride with your own height, so anyone with a long reach can be one.', dos='Only one measure counts here, and it is the length of your stride for your height.'),
               'es': dict(art='un Goliat', titulo='Camina como un Goliat: zancadas gigantes', uno='Los goliats avanzan en un paso lo que otros en dos. No se trata de ser alto: Kinstride compara tu paso con tu propia estatura, así que cualquiera con una zancada larga puede serlo.', dos='Aquí cuenta una sola medida: el largo de tu paso para tu estatura.')},
    'ascuano': {'en': dict(art='Emberkin', titulo='Move Like Emberkin: Bursts of Fire', uno='Emberkin burn in bursts. They run, walk, run again, and no two stretches look the same. Calm is simply the moment before the next spark.', dos='Kinstride looks for a share of running in the middle of your walks and a pace that keeps changing.'),
                'es': dict(art='un Ascuano', titulo='Muévete como un Ascuano: arranques de fuego', uno='Los ascuanos arden a rachas. Trotan, caminan, vuelven a trotar, y no hay dos tramos iguales. La calma es solo el momento antes de la siguiente chispa.', dos='Kinstride busca una parte de trote en medio de tus caminatas y un ritmo que cambia todo el tiempo.')},
}


def meta_limpia(m: dict, lang: str) -> str:
    """'100 % or more' no dice nada: el máximo se muestra solo."""
    txt = m['meta'] if lang == 'es' or m['meta'] == m['metaImperial'] else f"{m['meta']} ({m['metaImperial']})"
    return re.sub(r'^(100 %|4 of 4|4 de 4)( or more| o más)$', r'\1', txt)


def url_linaje(lang: str, id_: str) -> str:
    return f"{RUTA[lang]['linajes']}{SLUG[lang][id_]}/"


def cabeza(lang, sitio, umami, titulo, desc, url, otra, og, extra=''):
    es, en = (url, otra) if lang == 'es' else (otra, url)
    loc = 'es_419' if lang == 'es' else 'en_US'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Kinstride">
<meta property="og:locale" content="{loc}">
<meta property="og:image" content="{sitio}{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{sitio}{url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{sitio}{url}">
<link rel="icon" href="/favicon.png" sizes="32x32">
<link rel="icon" href="/img/icono-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="/img/icono-180.png">
<meta name="theme-color" content="#1B1C1F">
<link rel="alternate" hreflang="en" href="{sitio}{en}">
<link rel="alternate" hreflang="es" href="{sitio}{es}">
<link rel="alternate" hreflang="x-default" href="{sitio}{en}">
<link rel="preload" href="/fuentes/saira-extra-condensed-normal-900.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fuentes/saira-extra-condensed-normal-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fuentes/schibsted-grotesk-normal-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/estilo.css">
{umami}{extra}
</head>
<body class="sub">
'''


def barra(lang, otra):
    t = T[lang]
    return f'''<header class="barra"><nav class="barra-dentro"><a class="marca" href="{RUTA[lang]['inicio']}" aria-label="{t['marca']}">KINSTRIDE</a><span><a href="{RUTA[lang]['test']}">{t['nav_test']}</a><a href="{RUTA[lang]['linajes']}">{t['nav_linajes']}</a><a href="{otra}">{t['otro']}</a></span></nav></header>
'''


def pie(lang, srd):
    t = T[lang]
    return f'''<footer class="ancho">
<p class="pie"><a href="{RUTA[lang]['test']}">{t['nav_test']}</a> · <a href="{RUTA[lang]['linajes']}">{t['nav_linajes']}</a> · <a href="{TIKTOK}" rel="me">TikTok</a> · <a href="/discord/">Discord</a> · <a href="{t['priv'][0]}">{t['priv'][1]}</a> · <a href="{t['borrar'][0]}">{t['borrar'][1]}</a></p>
<p class="pie legal">{srd}</p>
</footer>
</body>
</html>
'''


def tarjetas(lang, datos, saltar=None, carga='lazy'):
    r = {x['id']: x for x in datos['razas']}
    return ''.join(f'''<a class="linaje" href="{url_linaje(lang, i)}"><img src="/img/raza-{i}.webp" alt="" width="360" height="480" loading="{carga}"><b>{r[i]['nombre']}</b></a>''' for i in ORDEN if i != saltar)


def pagina_test(lang, raiz, sitio, umami, srd):
    t, datos = T[lang], json.loads((raiz / 'datos' / f'linajes-{lang}.json').read_text())
    otro = 'es' if lang == 'en' else 'en'
    razas = {r['id']: {'nombre': r['nombre'], 'resumen': r['resumen'], 'pro': r['pro'], 'conArticulo': C[r['id']][lang]['art'], 'url': url_linaje(lang, r['id']), 'img': f"/img/raza-{r['id']}.webp"} for r in datos['razas']}
    preguntas = [{'q': q, 'a': [[o, RESPUESTAS[i][j]] for j, o in enumerate(ops)]} for i, (q, ops) in enumerate(t['preguntas'])]
    textos = {k: t[k] for k in ('pregunta', 'atras', 'caminas', 'ver', 'compartir', 'copiado', 'repetir', 'raro', 'estimado')} | {'textoCompartir': t['texto_compartir']}
    j = json.dumps({'reglas': datos['reglas'], 'razas': razas, 'preguntas': preguntas, 't': textos}, ensure_ascii=False, separators=(',', ':'))
    faq = ''.join(f'<h3>{q}</h3><p>{a}</p>' for q, a in t['faq'])
    u, o = RUTA[lang]['test'], RUTA[otro]['test']
    faq_ld = '<script type="application/ld+json">' + json.dumps({
        '@context': 'https://schema.org', '@type': 'FAQPage',
        'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]
    }, ensure_ascii=False) + '</script>' + miga(sitio, [('Kinstride', RUTA[lang]['inicio']), (t['nav_test'], u)])
    html = cabeza(lang, sitio, umami, t['test_titulo'], t['test_desc'], u, o, f'/img/og-test-{lang}.jpg', faq_ld) + barra(lang, o) + f'''<main class="ancho">
<section class="test-portada"><h1>{t['test_h1']}</h1><p class="intro">{t['test_intro']}</p>
<div id="test" class="test" aria-live="polite"><button type="button" id="test-empezar" class="boton">{t['empezar']}</button><div class="test-linajes">{tarjetas(lang, datos, carga='eager')}</div></div>
<noscript><p><a href="{RUTA[lang]['linajes']}">{t['sin_js']}</a></p></noscript></section>
<section class="amplia"><h2>{t['faq_t']}</h2>{faq}</section>
</main>
<script type="application/json" id="datos-test">{j}</script>
<script src="/test.js" defer></script>
''' + pie(lang, srd)
    p = raiz / u.strip('/') / 'index.html'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)


def miga(sitio, items):
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': sitio + u} for i, (n, u) in enumerate(items)]}, ensure_ascii=False) + '</script>'


def cta(lang):
    t = T[lang]
    return f'''<section class="resumen tester"><p>{t['test_cta_p']} <a href="{RUTA[lang]['test']}">{t['test_cta']}</a>.</p><p>{t['tester_p']}</p><p class="botones"><a class="boton" href="{t['tester_url']}" data-umami-event="ser-tester">{t['tester']}</a></p></section>
'''


def pagina_linajes(lang, raiz, sitio, umami, srd):
    t, datos = T[lang], json.loads((raiz / 'datos' / f'linajes-{lang}.json').read_text())
    otro = 'es' if lang == 'en' else 'en'
    datos_otro = {r['id']: r for r in datos['razas']}
    u, o = RUTA[lang]['linajes'], RUTA[otro]['linajes']
    lista = ''.join(f'''<article class="linaje-fila"><a href="{url_linaje(lang, i)}"><img src="/img/raza-{i}.webp" alt="{datos_otro[i]['nombre']}" width="360" height="480" loading="lazy"></a><div><h2><a href="{url_linaje(lang, i)}">{datos_otro[i]['nombre']}</a></h2><p>{datos_otro[i]['resumen']}.</p></div></article>''' for i in ORDEN)
    lista_ld = '<script type="application/ld+json">' + json.dumps({
        '@context': 'https://schema.org', '@type': 'ItemList', 'name': t['linajes_h1'],
        'itemListElement': [{'@type': 'ListItem', 'position': idx + 1, 'name': datos_otro[i]['nombre'], 'url': sitio + url_linaje(lang, i)} for idx, i in enumerate(ORDEN)]
    }, ensure_ascii=False) + '</script>' + miga(sitio, [('Kinstride', RUTA[lang]['inicio']), (t['intro_miga'], u)])
    html = cabeza(lang, sitio, umami, t['linajes_titulo'], t['linajes_desc'], u, o, f'/img/og-test-{lang}.jpg', lista_ld) + barra(lang, o) + f'''<main class="ancho">
<h1>{t['linajes_h1']}</h1><p class="intro">{t['linajes_intro']}</p>
<div class="linajes-lista">{lista}</div>
{cta(lang)}</main>
''' + pie(lang, srd)
    p = raiz / u.strip('/') / 'index.html'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)
    for r in datos['razas']:
        i, c = r['id'], C[r['id']][lang]
        u, o = url_linaje(lang, i), url_linaje(otro, i)
        filas = ''.join(f'''<tr><th scope="row">{m['medida']}{f" <em>({t['llave']})</em>" if m['llave'] else ''}</th><td>{meta_limpia(m, lang)}</td></tr>''' for m in r['metas'])
        nota = t['llave_p'].format(r['nombre']) if any(m['llave'] for m in r['metas']) else ''
        var = ''
        if r['variantes']:
            var = f'''<section class="amplia"><h2>{t['variantes_t']}</h2><p>{t['variantes_p']}</p><ul>''' + ''.join(f"<li><b>{v['nombre']}.</b> {v['porque']}</li>" for v in r['variantes']) + '</ul></section>'
        miga_j = miga(sitio, [('Kinstride', RUTA[lang]['inicio']), (t['intro_miga'], RUTA[lang]['linajes']), (r['nombre'], u)])
        html = cabeza(lang, sitio, umami, f"{c['titulo']} | Kinstride", t['pag_desc'].format(resumen=r['resumen'], art=c['art']), u, o, f"/img/og-{lang}-{i}.jpg", miga_j) + barra(lang, o) + f'''<main class="ancho">
<article class="linaje-pag"><img src="/img/raza-{i}.webp" alt="{r['nombre']}: {r['resumen']}" width="360" height="480"><div><p class="miga"><a href="{RUTA[lang]['linajes']}">{t['intro_miga']}</a></p><h1>{c['titulo']}</h1><p class="bajada">{r['resumen']}.</p><p>{c['uno']}</p><p>{c['dos']}</p><p class="nota">{t['raro_pag'] if r['pro'] else t['gratis_pag']}</p></div></article>
<section class="amplia"><h2>{t['mide_t']}</h2><p>{t['mide_p']}</p><div class="tabla"><table><thead><tr><th>{t['col'][0]}</th><th>{t['col'][1]}</th></tr></thead><tbody>{filas}</tbody></table></div><p class="nota">{nota}</p></section>
{var}
{cta(lang)}<section class="amplia"><h2>{t['otros_t']}</h2><div class="linajes-mini">{tarjetas(lang, datos, i)}</div></section>
</main>
''' + pie(lang, srd)
        p = raiz / u.strip('/') / 'index.html'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(html)


def generar(raiz: Path, sitio: str, umami: str, srd: str) -> list[str]:
    for lang in ('en', 'es'):
        pagina_test(lang, raiz, sitio, umami, srd)
        pagina_linajes(lang, raiz, sitio, umami, srd)
    return [RUTA[l]['test'] for l in ('en', 'es')] + [RUTA[l]['linajes'] for l in ('en', 'es')] + [url_linaje(l, i) for l in ('en', 'es') for i in ORDEN]
