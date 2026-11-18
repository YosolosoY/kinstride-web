# getkinstride.com

Sitio de Kinstride (GitHub Pages). La portada en inglés (`index.html`) y en español (`es/index.html`) salen de
`generar.py`: cambiar los textos ahí y correr `python3 generar.py`. Capturas en `img/` (desde
~/Projects/kinstride/store/originales-*). Privacidad y borrado de datos se editan a mano en sus carpetas.

El test (`test.js`) y las páginas de linaje salen de `generar_linajes.py` y de `datos/linajes-*.json`, exportados desde la app con `scripts/tienda/linajes-sitio.ts`: si cambian las reglas, volver a exportar y correr `generar.py`. Las imágenes para compartir salen de `generar_og.py`.

## Idiomas (4.2.0): pt, fr, de, it

El sitio sale en 6 idiomas: inglés y español como siempre (`generar.py`) y portugués, francés, alemán e italiano en `/pt/`, `/fr/`, `/de/`, `/it/`, hechos por `idiomas_sitio.py` a partir de las páginas en inglés (necesita `pip install beautifulsoup4`):

```
python3 generar.py                  # inglés y español (y linajes)
python3 idiomas_sitio.py faltan     # qué textos nuevos hay sin traducir → datos/i18n-sitio/faltan-<idioma>.json
# en el homeserver (allí está la llave de la API; copiar el script, datos/glosario-i18n.json y los faltan-*.json):
python3 traducir_sitio_api.py pt fr de it       # lotes de Sonnet 5.5 → nuevas-<idioma>.json
python3 idiomas_sitio.py importar   # valida que las etiquetas HTML no cambiaron y mete los textos en la caché
python3 idiomas_sitio.py construir  # escribe pt/ fr/ de/ it/, el selector de idiomas, los hreflang y el sitemap
```

La caché de traducciones (`datos/i18n-sitio/<idioma>.json`, por huella del texto en inglés) está en el repo: reconstruir no gasta API; si cambia un texto en inglés, solo ese se vuelve a traducir. Dejan de traducirse a propósito: la licencia del SRD 5.2 y la declaración de Health Connect (van en inglés). El glosario (`datos/glosario-i18n.json`) es copia del de la app (`kinstride/archivo/trabajo/idiomas/glosario-final.json`). Las imágenes para compartir (`og:image`) siguen siendo las de inglés. La app abre la política de privacidad de su idioma: `/pt/privacidade/`, `/fr/confidentialite/`, `/de/datenschutz/`, `/it/privacy/`.

### Imágenes por idioma y SEO (4.2.0)

- Imágenes para compartir: `python3 generar_og.py` genera `img/compartir-{es,pt,fr,de,it}.jpg` (del gráfico destacado de Play), `og-{idioma}-<linaje>.jpg` y `og-test-{idioma}.jpg`; los textos de pt/fr/de/it salen del test ya traducido. `idiomas_sitio.py construir` las apunta en cada página (`ajustar_og`) y pone `og:image:alt` en el idioma de la página.
- Capturas de la app por idioma: `node scripts/tienda/hojas.mjs <idioma> <carpeta>` (en el repo de la app, con `npx expo start --web --port 8091`) y convertirlas a `img/<idioma>-*.webp` (480 y 240 px; hojas 720 y 360). Si falta `img/<idioma>-X.webp`, la página usa la de inglés.
- Auditoría SEO: revisar título (≤65), descripción (70–165), canonical, `lang`, un solo h1, hreflang recíproco con `x-default`, og/twitter, JSON-LD válido, alt, ancho/alto de imágenes, enlaces y sitemap. `lastmod` del sitemap = fecha en que se genera.
- El dato estructurado `MobileApplication` no lleva `aggregateRating` ni `review` a propósito: Google los exige para el resultado enriquecido y no se inventan; agregarlos cuando haya reseñas reales.

## Guía en inglés (2026-11-18): `/guides/best-walking-rpg-apps-android/`

Texto en `guia_walking_rpg.py` (solo inglés, no se traduce; generar.py la importa). Su enlace en el pie de las páginas EN lo añade `python3 enlace_guia.py` DESPUÉS de `idiomas_sitio.py construir` (no va en los generadores: cambiaría el texto del pie y pt/fr/de/it quedarían sin traducir en esa línea). `actualizar_eventos.sh` ya lo llama.

## Eventos (2026-11-17): `/events/` (EE. UU., en) y `/es/eventos/` (Santiago, es)

Calendario de eventos de fantasía, juegos y anime por ciudad, con fechas comprobadas en la página del organizador y un ángulo de linajes. Un solo idioma por ciudad: NO se traduce a pt/fr/de/it (`idiomas_sitio.py` solo toma su lista fija `EN_PAG`).

```
./actualizar_eventos.sh     # trae el radar del homeserver → consolida → genera → idiomas → restaura privacidad → audita. NO publica.
python3 auditar_eventos.py  # solo la auditoría (título ≤65, descripción 70–165, canonical, h1, enlaces, idioma, sitemap…)
```
- Datos: `datos/eventos_manual.json` (verificados a mano, manda sobre el radar campo a campo) + `datos/eventos-crudo/` (radar) + `datos/eventos-descripciones.json` → `datos/eventos.json` (lo escribe `consolidar_eventos.py`; el estado más fuerte gana: confirmada > sin_2027 > solo_terceros).
- Radar (homeserver `~/sistema/`): `radar_eventos.py` (miércoles 03:00, 8 ciudades × 3 trabajos), `enriquecer_eventos.py` (miércoles 05:30, descripción factual desde la web oficial), `vigila_eventos.py` (lunes 09:00, avisa por Telegram cuando una web oficial publica 2027), `pistas_facebook.py` (Apify; necesita `~/.config/apify/token`). Todo usa `claude -p` con la suscripción, nunca la API.
- Formulario de organizadores: n8n `KinstrideEvento01x` (POST `https://n8n.monsalve.com.co/webhook/kinstride-evento`) → `/srv/automatizacion/eventos/envios.jsonl` + aviso por Telegram. Página `/events/submit/` y `/es/eventos/enviar/` (noindex).
- Reglas: página propia solo para «confirmada» y «sin_2027» con web oficial y última edición; ciudad con página solo con ≥3 eventos (`MIN_CIUDAD`); el ángulo de linaje se rotula como opinión nuestra; cada página dice fecha de verificación y no-afiliación.
- TRAMPAS: `generar.py` sin `idiomas_sitio.py construir` deja las páginas sin hreflang de 6 idiomas; `construir` pisa privacidad pt/fr/de/it (el script las restaura con `git checkout`); `python3 -I generar.py` falla (no ve los módulos hermanos); `.venv/` (bs4, playwright) está excluido de git.
- Tras publicar: `ssh homeserver 'python3 ~/sistema/medicion_cambios.py --registrar getkinstride.com /events/ "…"'` (y `/es/eventos/`) para medir a 28 días.
