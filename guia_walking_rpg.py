"""Guía en inglés: mejores apps de caminar con juego de rol para Android. Solo inglés (no se traduce). Lo importa generar.py.
Borrador original: homeserver ~/sistema/borradores/kinstride/2026-11-18_best-walking-rpg-apps-android.md (fuentes verificadas allí).
Lo de Kinstride (hoja de personaje, linajes, artistas) sale del código de la app y de las páginas del sitio."""
import json as _json
import play

RUTA = '/guides/best-walking-rpg-apps-android/'
SITIO_ = 'https://getkinstride.com'
_MISTY = 'https://mistyway.app/blog/walking-rpg-apps'
_SQUID = 'https://laughingsquid.com/fantsy-hike-walk-tracking-app/'
_POCKET = 'https://www.pocketgamer.com/run-the-realm/out-now/'

_IDS = ['distinction', 'compared', 'notes', 'choose', 'fits', 'table', 'artists']
_FAQ = [
 ('Does Kinstride use GPS?', 'Kinstride counts your real kilometers to move you along the map. The way you walk (climbs, cadence, endurance and more) decides your lineage and your character’s abilities.'),
 ('Can I use my Kinstride character in a tabletop role-playing game?', 'The character sheet follows the usual layout: six abilities, armor, hit points and proficiency bonus, with the formulas from the SRD 5.2. Ask your game master whether the table accepts it. See “Use it at your table” above for what it does and does not include.'),
 ('Is Kinstride on Google Play?', (f'Yes. Kinstride is free on <a href="{play.url("guia-faq")}">Google Play</a>, with no ads and no distance limit.' if play.LIVE else 'Not yet at the time of writing (November 18, 2026). The app is waiting for Google Play’s production review, so there is no download link here.')),
 ('Who draws the art in Kinstride?', 'Illustration students and artists, credited by name on each piece. We accept 2 new illustrators each month and pay US$50 once the first 10 pieces are accepted. See the artists page.'),
]

_TABLA = ('<div class="tabla"><table><thead><tr><th>App</th><th>Android?</th><th>Tracking</th><th>Cost (per source)</th><th>Style</th></tr></thead><tbody>'
 '<tr><td>MistyWay</td><td>Yes (also iOS)</td><td>Steps, no GPS</td><td>Free, no ads</td><td>Quests, biomes, hero levels</td></tr>'
 '<tr><td>Orna</td><td>Yes (also iOS)</td><td>GPS</td><td>Free, no ads</td><td>Monsters and dungeons on real streets, multiplayer raid bosses</td></tr>'
 '<tr><td>WalkScape</td><td>Yes, closed beta only</td><td>Steps, works offline</td><td>Free, no ads</td><td>Skill training (mining, woodcutting, combat) by walking</td></tr>'
 '<tr><td>The Walk</td><td>Yes (also iOS)</td><td>Steps, works offline</td><td>First 5 episodes free, then purchase or subscription</td><td>Linear thriller story, 65 episodes</td></tr>'
 '<tr><td>Zombies, Run!</td><td>Yes (also iOS)</td><td>GPS</td><td>Freemium, $6.99/month</td><td>Running-focused story missions</td></tr>'
 '<tr><td>Run the Realm</td><td>Yes, re-released on Google Play</td><td>Not stated in our source</td><td>Not stated</td><td>Fantasy story; jogging, running, cycling and walking count</td></tr>'
 '<tr><td>Fantasy Hike</td><td>Not confirmed (appears iOS-only)</td><td>Steps</td><td>Not stated</td><td>Fixed-route journey across a themed map</td></tr>'
 '</tbody></table></div>')

_LINAJES = ' · '.join(f'<a href="/lineages/{s}/">{n}</a>' for s, n in
    [('halfling', 'Halfling'), ('dwarf', 'Dwarf'), ('human', 'Human'), ('elf', 'Elf'), ('orc', 'Orc'), ('barkfolk', 'Barkfolk'), ('gnome', 'Gnome'), ('goliath', 'Goliath'), ('emberkin', 'Emberkin')])

SECS = [
 ('The one distinction that matters: GPS or steps',
  '<p><b>GPS-based apps</b> place the game on your real streets. Monsters and dungeons show up near you. This makes the world feel real, but it needs location access and, in practice, more screen time or location services running.</p>'
  '<p><b>Step-based apps</b> read your phone’s pedometer or a health platform. The game world is separate from where you are, so it works on a treadmill, indoors, or on a route you have walked a hundred times.</p>'
  '<p>Neither is better. It depends on whether you want your neighborhood to be the map or you want to escape it.</p>'),
 ('The apps, compared',
  f'<p>One caveat first: most of the detail below comes from <a href="{_MISTY}" rel="noopener">a comparison on MistyWay’s own blog</a> (updated November 17, 2026). The author discloses that MistyWay is “our app” and ranks it first, and its battery-use figures for GPS games are unsourced estimates. We used it for factual descriptions only, not for its rankings.</p>'
  + _TABLA + '<p><small>Prices and availability change. Check each store listing before you rely on this table.</small></p>'),
 ('Notes on each',
  '<h3>Orna: your streets are the map</h3><p>Orna is the pick if you want a GPS game with classes, crafting and raid bosses. According to the MistyWay comparison, it is free with no ads. The trade-off is that you play it on your real surroundings, so it suits walks outdoors.</p>'
  '<h3>WalkScape: skills by steps</h3><p>Per the same source, WalkScape is step-based, works offline, and is Android-only and still in closed beta. That limits who can try it right now.</p>'
  '<h3>The Walk: a finite story</h3><p>The Walk is a story with a beginning and an end: a courier carrying a detonator to Edinburgh over 65 episodes, according to the comparison. The first five episodes are free and the rest need a purchase or subscription. If you like a plot more than a stat sheet, this is a different kind of motivation.</p>'
  '<h3>Zombies, Run!: for runners</h3><p>It is built around running, with GPS tracking and story missions. The comparison lists it at $6.99/month. A separate figure of $7.99 appeared in our research, so we are not sure which is current. Check the store.</p>'
  f'<h3>Run the Realm</h3><p><a href="{_POCKET}" rel="noopener">PocketGamer’s coverage</a> of its Google Play re-release (January 2025) says jogging, running, cycling and walking all advance a fantasy story, with a mage, knight or thief class. It says nothing about tracking or pricing, so we cannot tell you either. The reviewer notes the AI-generated art can look muddy up close.</p>'
  f'<h3>Fantasy Hike</h3><p><a href="{_SQUID}" rel="noopener">Laughing Squid covered it</a> in January 2024: your steps move a halfling avatar across a Lord of the Rings-themed map to Mount Fire. The article mentions Apple Health and Apple Watch, which suggests an iOS app, but it does not say so outright. We could not confirm Android support or pricing. That “walk to a faraway place” idea is popular, though.</p>'),
 ('How to choose',
  '<ul><li><b>You walk mostly outdoors and like a live map:</b> a GPS game such as Orna.</li>'
  '<li><b>You walk on a treadmill, at the gym or on repeated routes:</b> a step-based game.</li>'
  '<li><b>You want a story with an ending:</b> The Walk.</li>'
  '<li><b>You run more than you walk:</b> Zombies, Run!</li>'
  '<li><b>You want a character you can also play at a table:</b> see Kinstride below.</li>'
  '<li><b>You hate subscriptions:</b> read the store listing’s pricing section first. “Free” can still mean in-app purchases.</li></ul>'
  '<p>One more tip: test for a week before committing. Many people drop gamified apps after the novelty fades, and a week shows you whether the loop keeps pulling you out the door or only counts steps in the background.</p>'),
 ('Where Kinstride fits',
  '<p>Kinstride is an Android app we are building, and we make it, so weigh this section accordingly. Your real kilometers move you across a fantasy map, and <b>the way you walk decides your character</b>: your climbs, cadence, endurance and routine pick one of nine lineages and a class. '
  'Steps-to-map is the same basic idea as several apps above, so we do not claim it is new. We have not proven it keeps people walking longer, and we have no retention data to show you.</p>'
  f'<p>Meet the lineages: {_LINAJES}. The <a href="/lineages/">lineages page</a> describes each one, and the <a href="/test/">test</a> shows which fits how you walk.</p>'
  + (f'<p>Kinstride is free on <a href="{play.url("guia-texto")}">Google Play</a>, with no ads and no distance limit.</p>' if play.LIVE else '<p>At the time of writing (November 18, 2026) Kinstride is not yet on the Google Play store: it is waiting for the production review, so there is no download link here.</p>')),
 ('Use it at your table',
  '<p>We designed the character so it can sit at a role-playing table. Your character sheet has the layout a tabletop player expects: <b>six abilities</b> (Strength, Dexterity, Constitution, Intelligence, Wisdom and Charisma, each from 8 to 20), a modifier for each, armor class, hit points by class and level, and a proficiency bonus. '
  'The numbers are not rolled: they come from how you walk. Climbing hills raises Strength, a steady cadence raises Dexterity, long outings raise Constitution, camps found raise Intelligence, consistency raises Wisdom, and walking with company raises Charisma.</p>'
  '<p>What this means in practice: bring your character to a game that uses the fifth-edition rules, show your game master the sheet, and ask whether the table accepts it. '
  'What it does not include yet: skills, saving throws, a backstory or spells, and the sheet is shared as an image rather than a file you can edit. Your abilities also recalculate as your walking changes, so a campaign would need you to agree with your game master on a fixed set of numbers.</p>'
  '<p>The rules and names come from the SRD 5.2 (see the license notice at the end of this page). Kinstride is independent and has no affiliation with any tabletop publisher.</p>'),
 ('The art is drawn by artists, with their name on it',
  '<p>Kinstride’s illustrations are being replaced, piece by piece, by work from illustration students and artists. Each piece carries the artist’s name and a link to their Instagram or portfolio, and the artist owns the work and may show it in their portfolio, social media and CV. '
  'We accept 2 new illustrators each month and pay US$50 once the first 10 pieces are accepted. If you draw, <a href="/artists/">read the artists page</a>; if you are leaving art school with no portfolio, '
  '<a href="/artists/first-published-illustration-project/">this guide to your first published illustration project</a> explains what to check in any offer, ours included.</p>'),
]


def _cuerpo():
    toc = '<nav aria-label="In this article"><p><b>In this article</b></p><ol>' + ''.join(
        f'<li><a href="#{i}">{t}</a></li>' for i, (t, _) in zip(_IDS + ['faq'], SECS + [('Frequently asked questions', '')])) + '</ol></nav>'
    out = '<p><small>Updated November 18, 2026</small></p>' + toc
    for i, (t, c) in zip(_IDS, SECS):
        out += f'<h2 id="{i}">{t}</h2>{c}'
        if i == 'table':
            out += ('<div class="galeria"><figure><img src="/img/en-personaje.webp" srcset="/img/en-personaje-240.webp 240w, /img/en-personaje.webp 480w" sizes="min(230px, 62vw)" '
                    'alt="Kinstride app screen: your stride, read in a radar" width="480" height="839" loading="lazy"><figcaption>Your stride, read in a radar</figcaption></figure></div>')
    out += '<h2 id="faq">Frequently asked questions</h2>' + ''.join(f'<h3>{q}</h3><p>{a}</p>' for q, a in _FAQ)
    out += '<p><em>If an app above has changed or we got something wrong, tell us on <a href="/discord/">our Discord</a> and we will correct it.</em></p>'
    return out


TITULO = 'Best Walking RPG Apps for Android (2026 Comparison)'
DESC = 'Which walking RPG apps work on Android? A plain comparison of GPS and step-based apps, what each costs, and what we could and could not verify.'
H1 = 'Best walking RPG apps for Android: GPS vs step-based (2026)'
RESUMEN = ('Walking RPG apps either use GPS to put the game on your streets or count steps in a separate world. Here are seven compared, with what we could and could not verify, and where Kinstride, the app we make, fits: '
           'a character decided by how you walk, with a sheet you can bring to a role-playing table.')

ENTRADA = dict(articulo=True, ruta=RUTA, otra=None, lang='en', t=TITULO, d=DESC, h1=H1, otro='', resumen=RESUMEN, secs=SECS, cuerpo=_cuerpo(), head_extra='<script type="application/ld+json">' + _json.dumps([
    {'@context': 'https://schema.org', '@type': 'Article', 'headline': H1, 'description': DESC, 'inLanguage': 'en', 'datePublished': '2026-11-18', 'dateModified': '2026-11-18',
     'author': {'@type': 'Organization', 'name': 'Kinstride', 'url': SITIO_ + '/'}, 'publisher': {'@type': 'Organization', 'name': 'Kinstride', 'url': SITIO_ + '/'},
     'image': SITIO_ + '/img/compartir.jpg', 'mainEntityOfPage': SITIO_ + RUTA},
    {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Kinstride', 'item': SITIO_ + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': H1, 'item': SITIO_ + RUTA}]}], ensure_ascii=False) + '</script>')
