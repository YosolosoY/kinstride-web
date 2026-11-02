/* Test de linajes: estima tus medidas con 8 respuestas y las pasa por las mismas reglas de la app.
   Las respuestas no salen del navegador. Solo se cuenta el linaje resultante. */
(function (raiz) {
  const sube = (x, a, b) => (x == null || !Number.isFinite(x) ? 0 : Math.max(0, Math.min(1, (x - a) / (b - a))));
  const entre = (x, a, b, m) => (x == null ? 0 : x < a ? sube(x, a - m, a) : x > b ? sube(x, b + m, b) : 1);
  const puntaje = (f, v) => ('entre' in f ? entre(v[f.k], ...f.entre) : sube(v[f.k], f.a, f.b));
  const prom = (xs) => xs.reduce((s, x) => s + x, 0) / xs.length;
  const afinidad = (r, v) => {
    const fs = r.factores.map((f) => puntaje(f, v));
    return r.llave ? puntaje(r.llave, v) * prom([1, ...fs]) : prom(fs);
  };

  /** Las respuestas en las medidas que usa la app (`valoresRaza`). */
  function medidas(res) {
    const m = { deDia: 0.7, hazanas: 0, ...Object.assign({}, ...res) };
    // Trotando se va a unos 9 km/h: la velocidad de las salidas mezcla los dos ritmos.
    m.velocidadTotal = m.velocidadMejor * (1 - m.trote) + 9 * m.trote;
    m.hazanas = [m.desnivelPorKm >= 20, m.velocidadMejor >= 6, m.duracion >= 75, m.trote >= 0.25].filter(Boolean).length;
    return m;
  }

  /** Porcentajes como en la app: afinidad al cuadrado, de mayor a menor. */
  function calcular(reglas, res) {
    const v = medidas(res);
    const af = Object.fromEntries(Object.entries(reglas).map(([id, r]) => [id, afinidad(r, v)]));
    if (Object.values(af).every((x) => x === 0)) af[v.velocidadMejor >= 4.85 ? 'elfo' : 'arboreo'] = 0.1;
    const peso = Object.entries(af).map(([id, x]) => [id, x * x]);
    const suma = peso.reduce((s, p) => s + p[1], 0);
    return peso.sort((a, b) => b[1] - a[1]).map(([id, w]) => ({ id, pct: Math.round((w / suma) * 100) }));
  }

  raiz.calcularLinaje = calcular;
  if (typeof document === 'undefined') return;

  const d = JSON.parse(document.getElementById('datos-test').textContent);
  const caja = document.getElementById('test');
  const res = [];
  const evento = (n, x) => window.umami && window.umami.track(n, x);
  const boton = (texto, clase, fn) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = clase;
    b.textContent = texto;
    b.addEventListener('click', fn);
    return b;
  };

  function pregunta(i) {
    caja.textContent = '';
    const p = d.preguntas[i];
    const avance = document.createElement('p');
    avance.className = 'test-avance';
    avance.textContent = `${d.t.pregunta} ${i + 1} / ${d.preguntas.length}`;
    const barra = document.createElement('div');
    barra.className = 'test-barra';
    barra.style.setProperty('--avance', `${(i / d.preguntas.length) * 100}%`);
    const h = document.createElement('h2');
    h.tabIndex = -1;
    h.textContent = p.q;
    const ops = document.createElement('div');
    ops.className = 'test-opciones';
    p.a.forEach(([texto, v]) => ops.append(boton(texto, 'test-opcion', () => {
      res[i] = v;
      if (i + 1 < d.preguntas.length) pregunta(i + 1);
      else resultado();
    })));
    caja.append(avance, barra, h, ops);
    if (i) {
      caja.append(boton(d.t.atras, 'test-atras', () => pregunta(i - 1)));
      h.focus();
    }
  }

  function resultado() {
    const r = calcular(d.reglas, res);
    const g = d.razas[r[0].id];
    evento('test-resultado', { linaje: r[0].id });
    caja.textContent = '';
    const fig = document.createElement('img');
    fig.src = g.img;
    fig.alt = g.nombre;
    fig.width = 360;
    fig.height = 480;
    const div = document.createElement('div');
    const h = document.createElement('h2');
    h.tabIndex = -1;
    h.textContent = d.t.caminas.replace('{}', g.conArticulo);
    const res1 = document.createElement('p');
    res1.className = 'test-resumen';
    res1.textContent = g.resumen;
    const ul = document.createElement('ul');
    ul.className = 'test-ranking';
    r.slice(0, 3).filter((x) => x.pct > 0).forEach((x) => {
      const li = document.createElement('li');
      li.style.setProperty('--pct', `${x.pct}%`);
      li.textContent = `${d.razas[x.id].nombre}: ${x.pct} %`;
      ul.append(li);
    });
    const nota = document.createElement('p');
    nota.className = 'nota';
    nota.textContent = g.pro ? `${d.t.raro} ${d.t.estimado}` : d.t.estimado;
    const acc = document.createElement('p');
    acc.className = 'botones';
    const ver = document.createElement('a');
    ver.className = 'boton';
    ver.href = g.url;
    ver.textContent = d.t.ver.replace('{}', g.nombre);
    acc.append(ver, boton(d.t.compartir, 'boton secundario', async (e) => {
      const url = new URL(g.url, location.href).href;
      const texto = d.t.textoCompartir.replace('{}', g.conArticulo);
      evento('test-compartir', { linaje: r[0].id });
      if (navigator.share) {
        try { await navigator.share({ text: texto, url }); } catch { /* cerrado por la persona */ }
      } else {
        await navigator.clipboard.writeText(`${texto} ${url}`);
        e.target.textContent = d.t.copiado;
      }
    }));
    const otra = boton(d.t.repetir, 'test-atras', () => { res.length = 0; pregunta(0); });
    div.append(h, res1, ul, nota, acc, otra);
    const f = document.createElement('div');
    f.className = 'test-resultado';
    f.append(fig, div);
    caja.append(f);
    h.focus();
  }

  document.getElementById('test-empezar').addEventListener('click', () => {
    evento('test-empezar');
    pregunta(0);
  });
})(typeof window === 'undefined' ? globalThis : window);
