#!/usr/bin/env python3
"""Imágenes para compartir (1200×630) de cada linaje y del test, más compartir.jpg (1024×500). Correr si cambia un nombre o el diseño."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).parent
KS = Path.home() / 'Projects/kinstride'
F = KS / 'assets/fonts'
ORDEN = ['mediano', 'enano', 'humano', 'elfo', 'orco', 'arboreo', 'gnomo', 'goliat', 'ascuano']
TXT = {'en': ('WHICH LINEAGE DO YOU WALK LIKE?', 'Free walking test · getkinstride.com'), 'es': ('¿A QUÉ LINAJE TE PARECES AL CAMINAR?', 'Test gratis · getkinstride.com'),
       'pt': ('COM QUAL LINHAGEM VOCÊ CAMINHA?', 'Teste de caminhada grátis · getkinstride.com'),
       'fr': ('À QUELLE LIGNÉE RESSEMBLES-TU QUAND TU MARCHES ?', 'Test de marche gratuit · getkinstride.com'),
       'de': ('WELCHER ABSTAMMUNG ENTSPRICHT DEIN GANG?', 'Gratis-Wandertest · getkinstride.com'),
       'it': ('CON QUALE LIGNAGGIO CAMMINI?', 'Test di camminata gratuito · getkinstride.com')}
NUEVOS = ('pt', 'fr', 'de', 'it')
CARPETA_TEST = {'pt': 'teste', 'fr': 'test', 'de': 'test', 'it': 'test'}


def datos_idioma(lang):
    """Nombre y resumen de cada linaje: en/es de datos/linajes-*.json; el resto, del test ya traducido de la página."""
    if lang in ('en', 'es'):
        return json.loads((RAIZ / f'datos/linajes-{lang}.json').read_text())
    import re
    h = (RAIZ / lang / CARPETA_TEST[lang] / 'index.html').read_text()
    d = json.loads(re.search(r'<script[^>]*id="datos-test"[^>]*>(.*?)</script>', h, re.S).group(1))
    return {'razas': [{'id': k, 'nombre': v['nombre'], 'resumen': v['resumen']} for k, v in d['razas'].items()]}



def fondo():
    m = Image.open(RAIZ / 'img/mapa-1000.webp').convert('RGB').resize((1400, 715), Image.LANCZOS).crop((100, 40, 1300, 670))
    return Image.blend(m, Image.new('RGB', m.size, (20, 21, 24)), 0.82)


def parrafo(d, texto, fuente, x, y, ancho, color, interlinea):
    linea = ''
    for p in texto.split():
        prueba = f'{linea} {p}'.strip()
        if d.textlength(prueba, font=fuente) > ancho and linea:
            d.text((x, y), linea, font=fuente, fill=color)
            y += interlinea
            linea = p
        else:
            linea = prueba
    d.text((x, y), linea, font=fuente, fill=color)
    return y + interlinea


def carta(img, r, x, y, alto):
    f = Image.open(RAIZ / f'img/raza-{r}.webp').convert('RGB')
    f = f.resize((round(f.width * alto / f.height), alto), Image.LANCZOS)
    img.paste(f, (x, y))
    return f.width


# Actualizar compartir.jpg desde el gráfico destacado 4.0
gd = KS / 'store/grafico-destacado-en.png'
if gd.exists():
    Image.open(gd).convert('RGB').save(RAIZ / 'img/compartir.jpg', quality=86, optimize=True, progressive=True)

for lang in ('es',) + NUEVOS:  # el gráfico destacado de cada idioma (el de inglés ya es compartir.jpg)
    g = KS / f'store/grafico-destacado-{lang}.png'
    if g.exists():
        Image.open(g).convert('RGB').save(RAIZ / f'img/compartir-{lang}.jpg', quality=86, optimize=True, progressive=True)

for lang in ('en', 'es') + NUEVOS:
    datos = datos_idioma(lang)
    pregunta, pie = TXT[lang]
    titulo = ImageFont.truetype(F / 'SairaExtraCondensed_800ExtraBold.ttf', 108)
    medio = ImageFont.truetype(F / 'IMFellEnglish_400Regular_Italic.ttf', 46)
    chico = ImageFont.truetype(F / 'SchibstedGrotesk_700Bold.ttf', 30)
    marca = ImageFont.truetype(F / 'SairaExtraCondensed_800ExtraBold.ttf', 42)
    for r in datos['razas']:
        img = fondo()
        d = ImageDraw.Draw(img)
        w = carta(img, r['id'], 790, 55, 520)
        d.rectangle((788, 53, 791 + w, 576), outline=(242, 194, 48), width=3)
        d.text((70, 64), 'KINSTRIDE', font=marca, fill=(242, 194, 48))
        y = parrafo(d, r['nombre'].upper(), titulo, 70, 126, 680, (237, 237, 232), 108)
        y = parrafo(d, r['resumen'], medio, 70, y + 14, 680, (180, 182, 189), 56)
        lineas = []  # la pregunta no debe pisar la carta (x ≥ 790): se parte en renglones de hasta 680 px
        for pal in pregunta.split():
            if lineas and d.textlength(f'{lineas[-1]} {pal}', font=chico) <= 680: lineas[-1] += f' {pal}'
            else: lineas.append(pal)
        for i, ln in enumerate(lineas):
            d.text((70, 496 - 36 * (len(lineas) - 1) + 36 * i), ln, font=chico, fill=(242, 194, 48))
        d.text((70, 540), pie.split(' · ')[1], font=chico, fill=(237, 237, 232))
        img.save(RAIZ / f"img/og-{lang}-{r['id']}.jpg", quality=85, optimize=True, progressive=True)
    img = fondo()
    d = ImageDraw.Draw(img)
    d.text((70, 56), 'KINSTRIDE', font=marca, fill=(242, 194, 48))
    y = parrafo(d, pregunta, ImageFont.truetype(F / 'SairaExtraCondensed_800ExtraBold.ttf', 88), 70, 114, 1060, (237, 237, 232), 92)
    x = 70
    for r in ORDEN:
        cw = carta(img, r, x, 340, 150)
        d.rectangle((x - 1, 339, x + cw, 490), outline=(58, 60, 66), width=2)
        x += cw + 4
    d.text((70, 530), pie, font=chico, fill=(237, 237, 232))
    img.save(RAIZ / f'img/og-test-{lang}.jpg', quality=85, optimize=True, progressive=True)
print('Imágenes OG y compartir.jpg listas')
