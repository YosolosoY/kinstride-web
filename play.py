"""Interruptor de «Kinstride ya está en Google Play». Mientras la ficha dé 404, LIVE = False (botones de prueba cerrada).
El día en que la ficha abra: cambiar el valor por defecto a '1' (o correr con PLAY_LIVE=1), regenerar y publicar (ver README, sección «Salida a producción»)."""
import os
from urllib.parse import quote

LIVE = os.environ.get('PLAY_LIVE', '0') == '1'
BASE = 'https://play.google.com/store/apps/details?id=co.com.monsalve.kinstride'


def url(donde: str) -> str:
    """Enlace de Play con UTM por lugar (el parámetro referrer lo recoge Play Console)."""
    return BASE + '&referrer=' + quote(f'utm_source=getkinstride&utm_medium=site&utm_campaign={donde}', safe='')
