#!/usr/bin/env python3
"""Lista de organizadores/tiendas por ciudad (de datos/eventos.json) con mensajes listos para invitarlos a enviar sus eventos.

    python3 contactos_eventos.py   → ~/Projects/kinstride/archivo/trabajo/eventos-piloto/contactos.md

El envío es de Mateo (contacto personal); aquí solo se arma la lista y el texto. Nada se envía desde aquí.
"""
import json
from pathlib import Path

R = Path(__file__).parent
SALIDA = Path.home() / 'Projects/kinstride/archivo/trabajo/eventos-piloto/contactos.md'
datos = json.loads((R / 'datos' / 'eventos.json').read_text())['eventos']
NOMBRE = {'santiago': 'Santiago', 'los-angeles': 'Los Angeles', 'san-diego': 'San Diego', 'chicago': 'Chicago', 'new-york': 'New York City', 'atlanta': 'Atlanta', 'houston': 'Houston', 'denver': 'Denver'}
URL = {'en': 'https://getkinstride.com/events/submit/', 'es': 'https://getkinstride.com/es/eventos/enviar/'}
MSG = {
    'es': """Hola, soy [tu nombre], de Kinstride (una app de caminar con linajes de fantasía). Armamos un calendario gratuito de eventos de juegos, rol, cartas, anime y fantasía en Santiago, con la fecha comprobada en la página del organizador y un enlace directo a ustedes. Ya tenemos «{ev}» en seguimiento. Si quieren que figuren sus próximos eventos, pueden enviarlos aquí (1 minuto): {url}. No cuesta nada y no pedimos nada a cambio. ¡Gracias!""",
    'en': """Hi, I'm [your name] from Kinstride (a walking app built around fantasy lineages). We run a free calendar of tabletop, card-game, anime and fantasy events in {city}, with every date checked on the organizer's own page and a direct link back to you. We're already tracking "{ev}". If you'd like your upcoming events listed, you can send them here (1 minute): {url}. It's free and we don't ask for anything in return. Thanks!""",
}
salida = ['# Organizadores y tiendas por ciudad (para invitarlos a enviar eventos)\n',
          'Generado desde `datos/eventos.json`. El envío lo hace Mateo (mensaje personal, no masivo). Cada fila: evento o tienda, su página, estado en el sitio.\n']
for c, nombre in NOMBRE.items():
    evs = [e for e in datos if e['ciudad'] == c]
    if not evs:
        continue
    lang = 'es' if c == 'santiago' else 'en'
    salida.append(f'\n## {nombre} ({len(evs)} eventos)\n')
    salida.append('| Evento / organizador | Página | Estado |\n|---|---|---|')
    for e in sorted(evs, key=lambda x: x['nombre']):
        url = e.get('url_oficial') or (e.get('fuentes') or [''])[0]
        org = f" — {e['organizador']}" if e.get('organizador') else ''
        salida.append(f"| {e['nombre']}{org} | {url} | {e['estado']} |")
    ej = next((e['nombre'] for e in evs if e['estado'] == 'confirmada'), evs[0]['nombre'])
    salida.append(f"\n**Mensaje ({lang}):**\n\n> " + MSG[lang].format(ev=ej, url=URL[lang], city=nombre))
SALIDA.write_text('\n'.join(salida) + '\n')
print(f'{SALIDA} · {len(datos)} eventos')
