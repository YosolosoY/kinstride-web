#!/usr/bin/env python3
"""Convierte las capturas de la app en cada idioma (de `scripts/tienda/hojas.mjs` y de store/originales-<idioma>) a las
imágenes del sitio: img/<idioma>-<nombre>.webp (480 px) y -240.webp; las hojas de personaje a 720 y 360 px.
Uso:  python3 capturas_idioma.py <carpeta con una subcarpeta por idioma (salida de hojas.mjs)>
Las pantallas camino, logros y viajero salen de las capturas de la ficha de Play (store/originales-<idioma>)."""
import sys
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).parent
KS = Path.home() / 'Projects/kinstride'
ORIGEN = Path(sys.argv[1])
HOJAS = ['mira', 'orrin', 'tamsin', 'bruna', 'kael', 'nettle']
# nombre en el sitio ← archivo que deja hojas.mjs
PANTALLAS = {'mapa': 'mapa', 'personaje': 'personaje', 'revelacion': 'revelacion', 'rutas': 'rutas', 'presentacion': 'presentacion',
             'plan': 'plan', 'historia': 'historia', 'bestiario': 'bestiario', 'caceria': 'caceria', 'parada': 'parada-monstruo', 'dragon': 'dragon'}
DE_PLAY = {'camino': 'camino', 'logros': 'logros', 'viajero': 'viajero'}  # store/originales-<idioma>/<archivo>.png


def guardar(img: Image.Image, destino: str, ancho: int):
    alto = round(img.height * ancho / img.width)
    img.convert('RGB').resize((ancho, alto), Image.LANCZOS).save(RAIZ / 'img' / destino, 'WEBP', quality=80, method=6)


for lang in sorted(p.name for p in ORIGEN.iterdir() if p.is_dir()):
    n = 0
    for h in HOJAS:
        f = ORIGEN / lang / f'hoja-{h}.png'
        if f.exists():
            im = Image.open(f); guardar(im, f'{lang}-hoja-{h}.webp', 720); guardar(im, f'{lang}-hoja-{h}-360.webp', 360); n += 1
    for sitio, arch in PANTALLAS.items():
        f = ORIGEN / lang / f'{arch}.png'
        if f.exists():
            im = Image.open(f); guardar(im, f'{lang}-{sitio}.webp', 480); guardar(im, f'{lang}-{sitio}-240.webp', 240); n += 1
    for sitio, arch in DE_PLAY.items():
        f = KS / f'store/originales-{lang}/{arch}.png'
        if f.exists():
            im = Image.open(f); guardar(im, f'{lang}-{sitio}.webp', 480); guardar(im, f'{lang}-{sitio}-240.webp', 240); n += 1
    print(lang, n, 'imágenes')
