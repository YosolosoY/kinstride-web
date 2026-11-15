#!/usr/bin/env python3
"""Páginas del sitio en portugués (pt), francés (fr), alemán (de) e italiano (it), a partir de las páginas en
inglés que deja `generar.py`. También pone a TODAS las páginas el selector de idiomas y los hreflang de los 6 idiomas.

Orden de trabajo (dependencias: `pip install beautifulsoup4`):
    python3 generar.py                  # las páginas en inglés y español de siempre
    python3 idiomas_sitio.py faltan     # lista lo que no está traducido → datos/i18n-sitio/faltan-<idioma>.json
    # traducir con la API (en el homeserver, donde está la llave): python3 traducir_sitio_api.py <idioma>
    python3 idiomas_sitio.py importar   # mete datos/i18n-sitio/nuevas-<idioma>.json en la caché
    python3 idiomas_sitio.py construir  # escribe pt/, fr/, de/, it/, los hreflang y el sitemap

La caché (datos/i18n-sitio/<idioma>.json: {huella: [inglés, traducción]}) va en el repo: reconstruir NO usa la API.
Cada unidad es el HTML interior de un bloque (p, li, h2, td…), un atributo (alt, aria-label, content) o un texto
de los datos JSON de las páginas. Las direcciones internas se reescriben a las de cada idioma.
"""
import hashlib, json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

RAIZ = Path(__file__).parent
SITIO = 'https://getkinstride.com'
NUEVOS = ['pt', 'fr', 'de', 'it']
TODOS = ['en', 'es'] + NUEVOS
NOMBRE = {'en': 'English', 'es': 'Español', 'pt': 'Português', 'fr': 'Français', 'de': 'Deutsch', 'it': 'Italiano'}
OG_LOCALE = {'en': 'en_US', 'es': 'es_419', 'pt': 'pt_BR', 'fr': 'fr_FR', 'de': 'de_DE', 'it': 'it_IT'}
CACHE = RAIZ / 'datos' / 'i18n-sitio'

# ---- direcciones: inglés → cada idioma ------------------------------------------------------------------------
LINAJES = ['halfling', 'dwarf', 'human', 'elf', 'orc', 'barkfolk', 'gnome', 'goliath', 'emberkin']
SLUG = {
    'es': ['mediano', 'enano', 'humano', 'elfo', 'orco', 'arboreo', 'gnomo', 'goliat', 'ascuano'],
    'pt': ['halfling', 'anao', 'humano', 'elfo', 'orc', 'arboreo', 'gnomo', 'golias', 'brasiano'],
    'fr': ['halfelin', 'nain', 'humain', 'elfe', 'orc', 'ecorcien', 'gnome', 'goliath', 'braisien'],
    'de': ['halbling', 'zwerg', 'mensch', 'elf', 'ork', 'rindenvolk', 'gnom', 'goliath', 'glutvolk'],
    'it': ['halfling', 'nano', 'umano', 'elfo', 'orco', 'arboreo', 'gnomo', 'golia', 'braciano'],
}
PAG = {  # privacy, delete-data, artists, test, lineages
    'es': ['privacidad', 'borrar-datos', 'artistas', 'test', 'linajes'],
    'pt': ['privacidade', 'apagar-dados', 'artistas', 'teste', 'linhagens'],
    'fr': ['confidentialite', 'supprimer-donnees', 'artistes', 'test', 'lignees'],
    'de': ['datenschutz', 'daten-loeschen', 'kuenstler', 'test', 'abstammungen'],
    'it': ['privacy', 'elimina-dati', 'artisti', 'test', 'lignaggi'],
}
EN_PAG = ['privacy', 'delete-data', 'artists', 'test', 'lineages']

def ruta(lang: str, en: str) -> str:
    """La dirección de una página en inglés ('/privacy/', '/lineages/dwarf/'…) en el idioma pedido."""
    if lang == 'en': return en
    pref = '/' + lang
    if en == '/': return pref + '/'
    partes = [p for p in en.split('/') if p]
    if partes[0] in EN_PAG:
        base = PAG[lang][EN_PAG.index(partes[0])]
        if len(partes) == 1: return f'{pref}/{base}/'
        if partes[0] == 'lineages' and partes[1] in LINAJES: return f'{pref}/{base}/{SLUG[lang][LINAJES.index(partes[1])]}/'
    return en  # /discord/ y demás: una sola dirección

def paginas_en() -> list[str]:
    """Direcciones de las páginas en inglés que se traducen."""
    return ['/', '/privacy/', '/delete-data/', '/artists/', '/test/', '/lineages/'] + [f'/lineages/{s}/' for s in LINAJES]

def archivo(url: str) -> Path:
    return RAIZ / url.strip('/') / 'index.html' if url != '/' else RAIZ / 'index.html'

# ---- unidades traducibles ------------------------------------------------------------------------------------------
INLINE = {'a', 'b', 'strong', 'i', 'em', 'span', 'code', 'small', 'sup', 'sub', 'br', 'img', 'mark', 'abbr', 'u', 's', 'kbd', 'time', 'cite', 'wbr'}
SALTAR = {'script', 'style', 'svg', 'noscript_', 'pre', 'code'}
ATRIBUTOS = ('alt', 'aria-label', 'title', 'placeholder')
CLAVES_LD = {'name', 'description', 'text', 'headline', 'alternateName'}

def huella(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()[:10]

def tiene_texto(e) -> bool:
    return any(isinstance(c, NavigableString) and not isinstance(c, Comment) and c.strip() for c in e.children)

def hijos_bloque(e) -> bool:
    return any(getattr(d, 'name', None) and d.name not in INLINE for d in e.descendants)

def unidades(soup: BeautifulSoup):
    """[(huella, texto_inglés, aplicar(traducción))] de una página."""
    out = []
    def agregar(txt, fn):
        txt = txt.strip()
        if txt and re.search(r'[A-Za-z]{2,}', re.sub(r'<[^>]+>', '', txt)): out.append((huella(txt), txt, fn))
    # <title> y metas
    if soup.title and soup.title.string: agregar(soup.title.string, lambda t, e=soup.title: e.string.replace_with(t))
    for m in soup.find_all('meta'):
        if m.get('content') and (m.get('name') in ('description',) or m.get('property') in ('og:title', 'og:description') or m.get('name') in ('twitter:title', 'twitter:description')):
            agregar(m['content'], lambda t, e=m: e.__setitem__('content', t))
    # cuerpo
    raiz = soup.body or soup
    def en_unidad(e):  # ¿ya va dentro de una unidad de texto?
        p = e.parent
        while p is not None and getattr(p, 'name', None) not in (None, '[document]'):
            if p.name not in INLINE and tiene_texto(p) and not hijos_bloque(p): return True
            p = p.parent
        return False
    for e in raiz.find_all(True):
        if e.name in SALTAR or any(a.name in SALTAR for a in e.parents): continue
        if 'idiomas' in (e.get('class') or []) or any('idiomas' in (a.get('class') or []) for a in e.parents): continue  # el selector de idiomas no se traduce
        dentro = en_unidad(e)  # lo de dentro de un texto ya viaja en su HTML
        for at in ATRIBUTOS:
            if not dentro and e.get(at) and re.search(r'[A-Za-z]{2,}', e[at]): agregar(e[at], lambda t, e=e, at=at: e.__setitem__(at, t))
        if tiene_texto(e):
            if e.name in INLINE and en_unidad(e): continue
            if hijos_bloque(e):
                for c in list(e.children):  # texto suelto junto a otros bloques: cada trozo es una unidad
                    if isinstance(c, NavigableString) and not isinstance(c, Comment) and c.strip():
                        agregar(str(c), lambda t, c=c: c.replace_with(NavigableString(t)))
                continue
            agregar(e.decode_contents(), lambda t, e=e: (e.clear(), [e.append(n) for n in list(BeautifulSoup(t, 'html.parser').contents)]))
    # datos JSON dentro de la página
    for s in soup.find_all('script'):
        tipo, cont = s.get('type'), (s.string or '')
        if tipo == 'application/ld+json' and cont.strip():
            d = json.loads(cont)
            def rec_ld(x):
                if isinstance(x, dict):
                    for k, v in list(x.items()):
                        if isinstance(v, str) and k in CLAVES_LD and not v.startswith(('http', '/')) and v != 'Kinstride':
                            agregar(v, lambda t, x=x, k=k: x.__setitem__(k, t))
                        else: rec_ld(v)
                elif isinstance(x, list):
                    for v in x: rec_ld(v)
            rec_ld(d)
            out.append(('', '', lambda _t, s=s, d=d: s.string.replace_with(json.dumps(d, ensure_ascii=False))))  # vuelve a escribir el JSON ya modificado
        if s.get('id') == 'datos-test' and cont.strip():
            d = json.loads(cont)
            for r in d['razas'].values():
                for k in ('nombre', 'resumen', 'conArticulo'): agregar(r[k], lambda t, r=r, k=k: r.__setitem__(k, t))
            for q in d['preguntas']:
                agregar(q['q'], lambda t, q=q: q.__setitem__('q', t))
                for a in q['a']: agregar(a[0], lambda t, a=a: a.__setitem__(0, t))
            for k, v in d['t'].items(): agregar(v, lambda t, d=d, k=k: d['t'].__setitem__(k, t))
            out.append(('', '', lambda _t, s=s, d=d: s.string.replace_with(json.dumps(d, ensure_ascii=False))))
    return out

def parsear(pag: str) -> BeautifulSoup:
    return BeautifulSoup(archivo(pag).read_text(), 'html.parser')

def cache(lang: str) -> dict:
    p = CACHE / f'{lang}.json'
    return json.loads(p.read_text()) if p.exists() else {}

# ---- ordenes ---------------------------------------------------------------------------------------------------------
def cmd_faltan():
    CACHE.mkdir(parents=True, exist_ok=True)
    todas = {}
    for pag in paginas_en():
        for h, txt, _ in unidades(parsear(pag)):
            if h: todas[h] = txt
    print(f'{len(todas)} textos únicos en {len(paginas_en())} páginas ({sum(len(t) for t in todas.values())} caracteres)')
    # textos legales que se dejan en inglés tal cual (licencia CC-BY del SRD y la declaración de Health Connect que exige Google)
    fijos = {h for h, t in todas.items() if t.startswith(('This work includes material from the System Reference Document', 'The use of information received from Health Connect'))}
    for lang in NUEVOS:
        c = cache(lang)
        for h in fijos: c.setdefault(h, [todas[h], todas[h]])
        (CACHE / f'{lang}.json').write_text(json.dumps(c, ensure_ascii=False, indent=1))
        f = {h: t for h, t in todas.items() if h not in c}
        (CACHE / f'faltan-{lang}.json').write_text(json.dumps(f, ensure_ascii=False, indent=1))
        print(f'  {lang}: faltan {len(f)}')

def estructura(html: str):
    """Etiquetas y atributos de un trozo de HTML (para comprobar que la traducción no los tocó)."""
    return [(t.name, tuple(sorted((k, str(v)) for k, v in t.attrs.items()))) for t in BeautifulSoup(html, 'html.parser').find_all(True)]

def cmd_importar():
    for lang in NUEVOS:
        p = CACHE / f'nuevas-{lang}.json'
        if not p.exists(): continue
        c, nuevas, mal = cache(lang), json.loads(p.read_text()), 0
        faltan = json.loads((CACHE / f'faltan-{lang}.json').read_text())
        for h, tr in nuevas.items():
            en = faltan.get(h)
            if en is None: continue
            if estructura(en) != estructura(tr): mal += 1; print(f'  ✗ {lang} {h}: etiquetas distintas · {en[:60]}'); continue
            c[h] = [en, tr]
        (CACHE / f'{lang}.json').write_text(json.dumps(c, ensure_ascii=False, indent=1))
        print(f'{lang}: caché {len(c)} textos · rechazados por etiquetas: {mal}')

def reescribir_enlaces(html: str, lang: str) -> str:
    def f(m):
        url = m.group(2)
        base, ancla = (url.split('#', 1) + [''])[:2] if '#' in url else (url, '')
        nuevo = ruta(lang, base) if base.startswith('/') else base
        return f'{m.group(1)}{nuevo}{"#" + ancla if ancla else ""}"'
    return re.sub(r'(href=")(/[^"]*?)"', f, html)

def selector(url_en: str) -> str:
    items = ' · '.join(f'<a href="{ruta(l, url_en)}" hreflang="{l}" lang="{l}">{NOMBRE[l]}</a>' for l in TODOS)
    return f'<p class="idiomas">{items}</p>'

def hreflang(url_en: str) -> str:
    ls = ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITIO}{ruta(l, url_en)}">\n' for l in TODOS)
    return ls + f'<link rel="alternate" hreflang="x-default" href="{SITIO}{url_en}">\n'

def poner_idiomas(html: str, url_en: str, es_en_es: bool = False) -> str:
    html = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', html)
    html = html.replace('</head>', hreflang(url_en) + '</head>', 1) if '<link rel="canonical"' in html else html
    html = re.sub(r'<p class="idiomas">.*?</p>\n?', '', html, flags=re.S)
    if '<p class="pie">' in html: html = re.sub(r'(<p class="pie">.*?</p>)', lambda m: m.group(1) + '\n' + selector(url_en), html, count=1, flags=re.S)
    elif '</main>' in html: html = html.replace('</main>', selector(url_en) + '\n</main>', 1)
    return html

ALT_COMPARTIR = {
    'en': 'Kinstride logo over an illustrated fantasy map', 'es': 'Logo de Kinstride sobre un mapa de fantasía ilustrado',
    'pt': 'Logotipo do Kinstride sobre um mapa de fantasia ilustrado', 'fr': 'Logo de Kinstride sur une carte fantasy illustrée',
    'de': 'Kinstride-Logo auf einer illustrierten Fantasy-Karte', 'it': 'Logo di Kinstride su una mappa fantasy illustrata',
}

def _meta(html: str, prop: str):
    """(texto de la etiqueta, contenido) de <meta property="prop">, con los atributos en cualquier orden."""
    m = re.search(r'<meta\b[^>]*\bproperty="' + re.escape(prop) + r'"[^>]*>', html)
    if not m: return None, None
    c = re.search(r'content="([^"]*)"', m.group(0))
    return m.group(0), (c.group(1) if c else None)

MILES = {'pt': '.', 'de': '.', 'it': '.', 'fr': ' '}

def numeros_locales(html: str, lang: str) -> str:
    """Las cifras sueltas del inglés («<b>1,081</b>», que no son texto traducible) con el separador de miles del idioma."""
    if lang not in MILES: return html
    return re.sub(r'(<b>)(\d{1,3}(?:,\d{3})+)(</b>)', lambda m: m.group(1) + m.group(2).replace(',', MILES[lang]) + m.group(3), html)

def ajustar_og(html: str, lang: str) -> str:
    """Imagen para compartir en el idioma de la página y su texto alternativo (og:image:alt) en todas las páginas con og:image."""
    if lang != 'en':
        html = html.replace('/img/compartir.jpg', f'/img/compartir-{lang}.jpg')
    if lang in NUEVOS:  # capturas de la app en el idioma de la página (si existen; si no, quedan las de inglés)
        html = re.sub(r'/img/en-([a-z0-9-]+\.webp)', lambda m: f'/img/{lang}-{m.group(1)}' if (RAIZ / 'img' / f'{lang}-{m.group(1)}').exists() else m.group(0), html)
        html = re.sub(r'/img/og-en-', f'/img/og-{lang}-', html)
        html = html.replace('/img/og-test-en.jpg', f'/img/og-test-{lang}.jpg')
    img_tag, img = _meta(html, 'og:image')
    if not img: return html
    comp = img.rsplit('/', 1)[-1].startswith('compartir')
    _, titulo = _meta(html, 'og:title')
    alt = ALT_COMPARTIR[lang] if comp else (titulo or 'Kinstride')
    viejo, _ = _meta(html, 'og:image:alt')
    nueva = f'<meta content="{alt}" property="og:image:alt"/>' if 'content="' in img_tag and img_tag.index('content="') < img_tag.index('property=') else f'<meta property="og:image:alt" content="{alt}">'
    if viejo: return html.replace(viejo, nueva, 1)
    ancla, _ = _meta(html, 'og:image:height')
    ancla = ancla or img_tag
    return html.replace(ancla, ancla + '\n' + nueva, 1)

def cmd_construir():
    pares = {}  # dirección en inglés → dirección en español existente
    for pag in paginas_en(): pares[pag] = ruta('es', pag)
    escritas = []
    for lang in NUEVOS:
        c = cache(lang); sin = 0
        for pag in paginas_en():
            soup = parsear(pag)
            us = unidades(soup)
            for h, txt, aplicar in us:
                if not h: continue
                if h in c: aplicar(c[h][1])
                else: sin += 1
            for h, txt, aplicar in us:  # los datos JSON se vuelven a escribir ya con las traducciones puestas
                if not h: aplicar(None)
            # cabecera y enlaces, sobre el árbol (bs4 reescribe el orden de los atributos, por eso no se usan expresiones regulares)
            soup.find('html')['lang'] = lang
            for l in soup.find_all('link'):
                rels = l.get('rel') or []
                if 'canonical' in rels: l['href'] = f'{SITIO}{ruta(lang, pag)}'
                if 'alternate' in rels and l.get('hreflang'): l.decompose()
            for l in TODOS:
                soup.head.append(soup.new_tag('link', rel='alternate', hreflang=l, href=f'{SITIO}{ruta(l, pag)}'))
            soup.head.append(soup.new_tag('link', rel='alternate', hreflang='x-default', href=f'{SITIO}{pag}'))
            for m in soup.find_all('meta'):
                if m.get('property') == 'og:url': m['content'] = f'{SITIO}{ruta(lang, pag)}'
                if m.get('property') == 'og:locale': m['content'] = OG_LOCALE[lang]
            for t in soup.find_all(href=True):
                u = t['href']
                if u.startswith('/') and not u.startswith('//'):
                    base, _, ancla = u.partition('#'); t['href'] = ruta(lang, base) + ('#' + ancla if ancla else '')
            sel = BeautifulSoup(selector(pag), 'html.parser')
            pie = soup.find('p', class_='pie') or soup.find('main')
            (pie.insert_after if pie.name == 'p' else pie.append)(sel)
            html = numeros_locales(ajustar_og(str(soup), lang), lang)
            destino = archivo(ruta(lang, pag)); destino.parent.mkdir(parents=True, exist_ok=True); destino.write_text(html)
            escritas.append(ruta(lang, pag))
        print(f'{lang}: {len(paginas_en())} páginas · textos sin traducir (se ven en inglés): {sin}')
    # hreflang y selector también en las páginas en inglés y español
    for pag in paginas_en():
        for lang in ('en', 'es'):
            p = archivo(ruta(lang, pag))
            if p.exists(): p.write_text(ajustar_og(poner_idiomas(p.read_text(), pag), lang))
    # mapa del sitio con todo
    sm = RAIZ / 'sitemap.xml'
    urls = [f'{SITIO}{ruta(l, p)}' for p in paginas_en() for l in TODOS]
    extra = re.findall(r'<loc>([^<]+)</loc>', sm.read_text())
    for u in extra:
        if u not in urls: urls.append(u)
    sm.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{u}</loc><lastmod>{__import__('datetime').date.today().isoformat()}</lastmod></url>\n' for u in urls) + '</urlset>\n')
    print(f'sitemap: {len(urls)} direcciones')

if __name__ == '__main__':
    {'faltan': cmd_faltan, 'importar': cmd_importar, 'construir': cmd_construir}[sys.argv[1] if len(sys.argv) > 1 else 'faltan']()
