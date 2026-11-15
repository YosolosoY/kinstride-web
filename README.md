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
