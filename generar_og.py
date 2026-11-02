#!/usr/bin/env python3
"""Imágenes para compartir (1200×630) de cada linaje y del test. Correr si cambia un nombre o un dibujo."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).parent
F = Path.home() / 'Projects/kinstride/assets/fonts'
ORDEN = ['mediano', 'enano', 'humano', 'elfo', 'orco', 'arboreo', 'gnomo', 'goliat', 'ascuano']
TXT = {'en': ('Which lineage do you walk like?', 'Free walking test · getkinstride.com'), 'es': ('¿A qué linaje te pareces al caminar?', 'Test gratis · getkinstride.com')}


def fondo():
    m = Image.open(RAIZ / 'img/mapa-1000.webp').convert('RGB').resize((1400, 715), Image.LANCZOS).crop((100, 40, 1300, 670))
    return Image.blend(m, Image.new('RGB', m.size, (20, 26, 36)), 0.72)


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


for lang in ('en', 'es'):
    datos = json.loads((RAIZ / f'datos/linajes-{lang}.json').read_text())
    pregunta, pie = TXT[lang]
    titulo = ImageFont.truetype(F / 'IMFellEnglish_400Regular.ttf', 92)
    medio = ImageFont.truetype(F / 'IMFellEnglish_400Regular.ttf', 46)
    chico = ImageFont.truetype(F / 'AlegreyaSans_700Bold.ttf', 34)
    for r in datos['razas']:
        img = fondo()
        d = ImageDraw.Draw(img)
        w = carta(img, r['id'], 790, 55, 520)
        d.rectangle((788, 53, 791 + w, 576), outline=(180, 154, 108), width=2)
        d.text((70, 70), 'KINSTRIDE', font=chico, fill=(233, 162, 59))
        y = parrafo(d, r['nombre'], titulo, 70, 130, 680, (247, 238, 216), 104)
        y = parrafo(d, r['resumen'], medio, 70, y + 12, 680, (230, 220, 199), 58)
        d.text((70, 500), pregunta, font=chico, fill=(233, 162, 59))
        d.text((70, 542), pie.split(' · ')[1], font=chico, fill=(230, 220, 199))
        img.save(RAIZ / f"img/og-{lang}-{r['id']}.jpg", quality=84, optimize=True, progressive=True)
    img = fondo()
    d = ImageDraw.Draw(img)
    d.text((70, 60), 'KINSTRIDE', font=chico, fill=(233, 162, 59))
    y = parrafo(d, pregunta, ImageFont.truetype(F / 'IMFellEnglish_400Regular.ttf', 78), 70, 118, 1060, (247, 238, 216), 90)
    x = 70
    for r in ORDEN:
        x += carta(img, r, x, 345, 150) + 4
    d.text((70, 530), pie, font=chico, fill=(230, 220, 199))
    img.save(RAIZ / f'img/og-test-{lang}.jpg', quality=84, optimize=True, progressive=True)
