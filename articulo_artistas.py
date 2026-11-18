"""Artículo para ilustradores que buscan su primer proyecto publicado (en y es). Lo importa generar.py.
Las afirmaciones de consejo vienen de las guías enlazadas; lo de Kinstride, de la página de artistas."""

_PENGUIN = 'https://www.penguin.co.uk/about/company-articles/how-to-become-a-book-illustrator'
_CENTRAL = 'https://centralillustration.com/news/top-tips-for-emerging-creatives-to-landing-your-first-illustration-client'
_CBLOQ = 'https://www.creativebloq.com/advice/how-to-get-illustrations-published'

EN_RUTA, ES_RUTA = '/artists/first-published-illustration-project/', '/es/artistas/primer-proyecto-ilustracion-publicado/'

GALERIA = {'en': [('bestiario', 'The bestiary: every creature gets its own plate'), ('mapa', 'The map is the home screen'), ('personaje', 'Your stride, read in a radar')],
           'es': [('bestiario', 'El Bestiario: cada criatura tiene su lámina'), ('mapa', 'El mapa es la pantalla principal'), ('personaje', 'Tu paso, leído en un radar')]}
FAQ = {'en': [
 ('Can I get a first published credit without clients?', 'Yes. Career guides for newcomers point first to self-initiated work, and a collaboration on someone else’s project adds a published credit if the credit is real and written down.'),
 ('What should a credit look like?', 'Your name and a link to your Instagram, website or portfolio on each piece, plus a written statement of what you did, how many pieces and when.'),
 ('Is a credit-only offer worth it?', 'It can be, if it is stated plainly, the licence is non-exclusive and you may show the work in your portfolio. Ask what you are getting, in writing, before you start.'),
 ('How many illustrators does Kinstride accept?', 'We accept 2 new illustrators each month.'),
 ('Does Kinstride pay?', 'Yes: US$50 once your first 10 pieces are accepted. Pieces accepted later carry your credit and are not paid additionally.')],
 'es': [
 ('¿Puedo tener un primer crédito publicado sin clientes?', 'Sí. Las guías de carrera para quien empieza señalan primero el trabajo autoiniciado, y una colaboración en el proyecto de otra persona suma un crédito publicado si el crédito es real y está por escrito.'),
 ('¿Cómo debe verse un crédito?', 'Tu nombre y un enlace a tu Instagram, web o portafolio en cada pieza, más una constancia escrita de qué hiciste, cuántas piezas y cuándo.'),
 ('¿Vale la pena una oferta solo con crédito?', 'Puede valer, si se dice con claridad, la licencia no es exclusiva y puedes mostrar el trabajo en tu portafolio. Pregunta por escrito qué recibes antes de empezar.'),
 ('¿Cuántos ilustradores acepta Kinstride?', 'Aceptamos 2 ilustradores nuevos cada mes.'),
 ('¿Kinstride paga?', 'Sí: US$50 cuando se acepten tus primeras 10 piezas. Las piezas aceptadas después llevan tu crédito y no se pagan aparte.')]}
H = {'en': dict(toc='In this article', faq='Frequently asked questions', upd='Updated November 15, 2026', ids=['start', 'show', 'collab', 'checklist', 'example', 'after'], inicio='Kinstride', art='Artists'),
     'es': dict(toc='En este artículo', faq='Preguntas frecuentes', upd='Actualizado el 15 de noviembre de 2026', ids=['empieza', 'muestralo', 'colaboracion', 'revisar', 'ejemplo', 'despues'], inicio='Kinstride', art='Artistas')}

ARTICULOS = {
 'art_en': dict(articulo=True, ruta=EN_RUTA, otra=ES_RUTA, lang='en',
  t='First Illustration Project: How to Build a Portfolio From Zero',
  d='Leaving art school with no portfolio? How to land your first illustration project, show it, and check any offer for credit, licence, pay and AI use.',
  h1='How to get your first published illustration project (with no portfolio yet)', otro='Versión en español',
  resumen='If you are leaving art school with no portfolio, your first published credit usually comes from self-started or collaborative projects, not from paid commissions. Here is how to pick them, how to show them, and what to check before saying yes to any offer, ours included.',
  secs=[
   ('Start with work you decide', f'<p>Career guides for illustrators with no commissions yet agree on one thing: begin with self-initiated work. <a href="{_PENGUIN}" rel="noopener">A Penguin guide to becoming a book illustrator</a> suggests self-started covers as a strong start for a newcomer, and quotes an illustrator who recommends including only pieces you are proud of and that reflect what you enjoy drawing.</p><p>A short, coherent series says more about you than many unrelated pieces. Choose a subject, a technique and a format, and keep them steady.</p>'),
   ('Show it where people look', f'<p>Put the series online in a simple portfolio, on Behance or on Instagram. <a href="{_CENTRAL}" rel="noopener">Central Illustration Agency</a> adds that a website and social media are not enough on their own: becoming part of the illustration community (associations, talks, awards) matters too. And keep making things: being able to show that you create constantly helps you be found.</p><p>Some outlets feature new talent by email submission; <a href="{_CBLOQ}" rel="noopener">Creative Bloq’s guide to getting illustrations published</a> lists examples. Check that any list you use is still current.</p>'),
   ('A project that is not yours: what counts', '<p>A published collaboration, such as a game, a book or a magazine, adds something your own series cannot: someone else’s product with your name on it. It only helps if the credit is real and you can prove it.</p>'),
   ('What to check before accepting any offer', '<ol><li><b>Credit:</b> your name and a link (Instagram, website or portfolio) on every piece, not only on a “thanks” page.</li><li><b>Proof:</b> a written statement of what you did, how many pieces and when.</li><li><b>Licence:</b> what the other side may do with the work, for how long, and whether it is exclusive.</li><li><b>Portfolio rights:</b> that you can show the work in your portfolio, social media and CV.</li><li><b>Compensation:</b> what, how much and when, in writing before you start. If the answer is “credit only”, that should be said plainly.</li><li><b>AI:</b> whether your art can be used to train AI or to imitate your style, and whether the other side uses AI on your files.</li><li><b>Scope:</b> number of pieces, format, deadlines and rounds of revision agreed up front.</li><li><b>Reality of the project:</b> is it published, or still in development? Many independent projects never reach release, so ask about its state.</li></ol>'),
   ('One example: Kinstride', '<p>Kinstride is an independent Android walking game. At the time of writing (November 2026) it is still in testing on Google Play, and its images were generated with AI; we want to replace them with the work of human illustrators. The offer: your name and link on each piece, in the app, on shared postcards and on this site; a signed letter with what you did, how many pieces and the date; a style guide and a list of 281 possible pieces (you do not have to do them all); a non-exclusive licence; no use of your art to train AI; and a fee of US$50 once your first 10 pieces are accepted (further accepted pieces carry your credit without additional payment). We accept 2 new illustrators each month.</p><p><a href="__ART__">See the full details for illustrators</a>.</p>'),
   ('After your first published piece', '<p>Ask for the written confirmation, add the piece to your portfolio with a link to where it is published, and tell people you are taking work: first commissions often come by word of mouth.</p>'),
 ]),
 'art_es': dict(articulo=True, ruta=ES_RUTA, otra=EN_RUTA, lang='es',
  t='Primer proyecto de ilustración: cómo armar tu portafolio desde cero',
  d='¿Saliendo de la carrera sin portafolio? Cómo conseguir tu primer proyecto de ilustración, mostrarlo y revisar crédito, licencia, pago y uso de IA.',
  h1='Cómo conseguir tu primer proyecto de ilustración publicado (sin portafolio todavía)', otro='English version',
  resumen='Si estás saliendo de la carrera y no tienes portafolio, tu primer crédito publicado suele salir de proyectos propios o colaborativos, no de encargos pagados. Aquí tienes cómo elegirlos, cómo mostrarlos y qué revisar antes de aceptar cualquier oferta, incluida la nuestra.',
  secs=[
   ('Empieza con trabajo que decides tú', f'<p>Las guías de carrera para ilustradores sin encargos coinciden en algo: empieza con trabajo autoiniciado. <a href="{_PENGUIN}" rel="noopener">Una guía de Penguin para ser ilustrador de libros</a> propone portadas propias como un buen comienzo para quien recién llega, y cita a una ilustradora que recomienda incluir solo piezas de las que te sientas orgulloso y que reflejen lo que disfrutas dibujando.</p><p>Una serie corta y coherente dice más de ti que muchas piezas sin relación. Elige un tema, una técnica y un formato, y mantenlos.</p>'),
   ('Muéstralo donde la gente mira', f'<p>Sube la serie a un portafolio sencillo, a Behance o a Instagram. <a href="{_CENTRAL}" rel="noopener">Central Illustration Agency</a> añade que un sitio web y redes sociales no bastan por sí solos: también importa formar parte de la comunidad de la ilustración (asociaciones, charlas, premios). Y sigue creando: poder mostrar que produces con constancia ayuda a que te encuentren.</p><p>Algunos medios muestran talento nuevo por envío de correo; <a href="{_CBLOQ}" rel="noopener">la guía de Creative Bloq para publicar ilustraciones</a> da ejemplos. Comprueba que cualquier lista que uses siga vigente.</p>'),
   ('Un proyecto que no es tuyo: qué cuenta', '<p>Una colaboración publicada, como un juego, un libro o una revista, aporta algo que tu propia serie no puede: el producto de otra persona con tu nombre. Solo sirve si el crédito es real y puedes demostrarlo.</p>'),
   ('Qué revisar antes de aceptar cualquier oferta', '<ol><li><b>Crédito:</b> tu nombre y un enlace (Instagram, web o portafolio) en cada pieza, no solo en una página de «agradecimientos».</li><li><b>Constancia:</b> un documento escrito con lo que hiciste, cuántas piezas y cuándo.</li><li><b>Licencia:</b> qué puede hacer la otra parte con la obra, por cuánto tiempo y si es exclusiva.</li><li><b>Derechos de portafolio:</b> que puedas mostrar la obra en tu portafolio, redes y CV.</li><li><b>Compensación:</b> qué, cuánto y cuándo, por escrito antes de empezar. Si la respuesta es «solo crédito», que lo digan con claridad.</li><li><b>IA:</b> si tu arte puede usarse para entrenar IA o imitar tu estilo, y si la otra parte usa IA con tus archivos.</li><li><b>Alcance:</b> número de piezas, formato, plazos y rondas de revisión acordados desde el principio.</li><li><b>Realidad del proyecto:</b> ¿está publicado o sigue en desarrollo? Muchos proyectos independientes nunca llegan a lanzarse, así que pregunta en qué estado está.</li></ol>'),
   ('Un ejemplo: Kinstride', '<p>Kinstride es un juego de caminar independiente para Android. Al momento de escribir esto (noviembre de 2026) sigue en pruebas en Google Play, y sus imágenes se generaron con IA; queremos reemplazarlas por obra de ilustradores humanos. Lo que ofrecemos: tu nombre y enlace en cada pieza, en la app, en las postales que se comparten y en este sitio; una carta firmada con lo que hiciste, cuántas piezas y la fecha; una guía de estilo y una lista de 281 piezas posibles (no tienes que hacerlas todas); licencia no exclusiva; que tu arte no se usa para entrenar IA; y un pago de US$50 cuando se acepten tus primeras 10 piezas (las piezas aceptadas adicionales llevan tu crédito, sin pago adicional). Aceptamos 2 ilustradores nuevos cada mes.</p><p><a href="__ART__">Mira todos los detalles para ilustradores</a>.</p>'),
   ('Después de tu primera pieza publicada', '<p>Pide la confirmación por escrito, agrega la pieza a tu portafolio con un enlace a donde está publicada y avisa que estás tomando trabajo: los primeros encargos suelen llegar de boca en boca.</p>'),
 ]),
}
import json as _json
import play
if play.LIVE:  # ya en producción: quitar «sigue en pruebas»
    for _k in ('art_en', 'art_es'):
        _a = ARTICULOS[_k]
        _a['secs'] = [(h, c.replace('At the time of writing (November 2026) it is still in testing on Google Play, and its images', 'It is available on Google Play, and its images').replace('Al momento de escribir esto (noviembre de 2026) sigue en pruebas en Google Play, y sus imágenes', 'Está disponible en Google Play y sus imágenes')) for h, c in _a['secs']]
SITIO_ = 'https://getkinstride.com'
for _k, _a in ARTICULOS.items():
    _l = _a['lang']; _h = H[_l]
    _a['secs'] = [(h, c.replace('__ART__', '/artists/' if _a['lang'] == 'en' else '/es/artistas/')) for h, c in _a['secs']]
    _ids = _h['ids']
    _gal = '<div class="galeria">' + ''.join(f'<figure><img src="/img/{_l}-{n}.webp" srcset="/img/{_l}-{n}-240.webp 240w, /img/{_l}-{n}.webp 480w" sizes="min(230px, 62vw)" alt="Kinstride app screen: {txt}" width="480" height="839" loading="lazy"><figcaption>{txt}</figcaption></figure>' for n, txt in GALERIA[_l]) + '</div>'
    _toc = f'<nav aria-label="{_h["toc"]}"><p><b>{_h["toc"]}</b></p><ol>' + ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, (t, _) in zip(_ids + ['faq'], _a['secs'] + [(_h['faq'], '')])) + '</ol></nav>'
    _cuerpo = f'<p><small>{_h["upd"]}</small></p>' + _toc
    for i, (t, c) in zip(_ids, _a['secs']):
        _cuerpo += f'<h2 id="{i}">{t}</h2>{c}'
        if i in ('example', 'ejemplo'): _cuerpo += _gal
    _cuerpo += f'<h2 id="faq">{_h["faq"]}</h2>' + ''.join(f'<h3>{q}</h3><p>{a}</p>' for q, a in FAQ[_l])
    _a['cuerpo'] = _cuerpo
    _url = SITIO_ + _a['ruta']
    _a['head_extra'] = '<script type="application/ld+json">' + _json.dumps([
        {'@context': 'https://schema.org', '@type': 'Article', 'headline': _a['h1'], 'description': _a['d'], 'inLanguage': _l, 'datePublished': '2026-11-15', 'dateModified': '2026-11-15',
         'author': {'@type': 'Organization', 'name': 'Kinstride', 'url': SITIO_ + '/'}, 'publisher': {'@type': 'Organization', 'name': 'Kinstride', 'url': SITIO_ + '/'},
         'image': SITIO_ + '/img/compartir.jpg', 'mainEntityOfPage': _url},
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Kinstride', 'item': SITIO_ + ('/' if _l == 'en' else '/es/')},
            {'@type': 'ListItem', 'position': 2, 'name': _h['art'], 'item': SITIO_ + ('/artists/' if _l == 'en' else '/es/artistas/')},
            {'@type': 'ListItem', 'position': 3, 'name': _a['h1'], 'item': _url}]}], ensure_ascii=False) + '</script>'

ENLACES = {  # sección que se añade al final de las páginas de artistas
 'en': ('Not sure where to start?', f'<p><a href="{EN_RUTA}">How to get your first published illustration project</a>: what to check in any offer, ours included.</p>'),
 'es': ('¿No sabes por dónde empezar?', f'<p><a href="{ES_RUTA}">Cómo conseguir tu primer proyecto de ilustración publicado</a>: qué revisar en cualquier oferta, incluida la nuestra.</p>'),
}
