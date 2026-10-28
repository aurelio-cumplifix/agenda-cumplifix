# -*- coding: utf-8 -*-
"""Ensambla el sitio: inyecta datos y assets en las plantillas y escribe la raíz del repo."""
import json, os, datetime as dt

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
MESES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto",
         "septiembre","octubre","noviembre","diciembre"]


def leer(nombre):
    with open(os.path.join(AQUI, nombre), encoding="utf-8") as f:
        return f.read()


def escribir(nombre, texto):
    ruta = os.path.join(RAIZ, nombre)
    os.makedirs(os.path.dirname(ruta), exist_ok=True) if os.path.dirname(ruta) != RAIZ else None
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    return len(texto)


datos = leer("agenda-2026.json")
logo = leer("logo.b64")
favicon = leer("favicon.b64")
hoy = dt.date.today()
fecha = "{} de {} de {}".format(hoy.day, MESES[hoy.month - 1], hoy.year)

plantilla = leer("plantilla.html")
LINK_2027 = ('<a class="link2027" href="pronostico-2027.html"><b>NUEVO</b>'
             'Ver posible calendario 2027 →</a>')
n1 = escribir("index.html", plantilla
              .replace("<!--BARRA_PRONOSTICO-->", "").replace("<!--SECCION_PRONOSTICO-->", "")
              .replace("<!--LINK_OTRO_ANIO-->", LINK_2027)
              .replace("__DATA__", datos).replace("__LOGO__", logo).replace("__FAVICON__", favicon))

# ---------------------------------------------------------------------------
# Pronóstico 2027: misma agenda con los días inhábiles estimados por
# CUMPLIFIX, S.C. Vive en su propia página para no tocar la agenda oficial.
# Cuando la CONDUSEF publique su acuerdo, se actualiza gen_data.py.
# ---------------------------------------------------------------------------
def pagina_pronostico():
    d27 = json.loads(leer("agenda-2027.json"))
    DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    def larga(iso):
        f = dt.date.fromisoformat(iso)
        return "{} {} de {}".format(DIAS[f.weekday()], f.day, MESES[f.month - 1])
    ene = d27["meses"][0]
    BASE = {"ley": ("Ley", "base-ley"), "patron": ("Patrón CONDUSEF", "base-patron"),
            "estimado": ("Estimado", "base-estimado")}
    # Agrupa los periodos vacacionales en una sola fila
    filas, vistos = [], set()
    for x in d27["meta"]["inhabiles_detalle"]:
        if x["base"] == "estimado":
            if x["motivo"] in vistos:
                continue
            vistos.add(x["motivo"])
            grupo = [y["fecha"] for y in d27["meta"]["inhabiles_detalle"] if y["motivo"] == x["motivo"]]
            fecha = "Del {} al {}".format(larga(grupo[0]), larga(grupo[-1]))
        else:
            fecha = larga(x["fecha"])
        et, cl = BASE[x["base"]]
        filas.append('<li><div>{}<br><span>{}</span></div><em class="base {}">{}</em></li>'.format(
            fecha[0].upper() + fecha[1:], x["motivo"], cl, et))
    seccion = """
  <section class="card pron" id="pronostico">
    <div class="eyebrow">Pronóstico CUMPLIFIX, S.C. · no oficial</div>
    <h2>Así podría quedar 2027</h2>
    <p class="lead2">La CONDUSEF da a conocer cada diciembre los días en que cerrará sus puertas
      (DOF del 21 de diciembre de 2022, 26 de diciembre de 2024 y 23 de diciembre de 2025). El acuerdo
      de 2027 todavía no se publica. Mientras tanto, construimos este calendario con lo que ya marca la
      ley y con lo que la CONDUSEF ha repetido en sus acuerdos de 2023, 2025 y 2026.</p>
    <div class="pron-claves">
      <div class="pron-clave"><div class="k">Primer día hábil</div>
        <div class="v">{p1}</div><div class="u">El 1 de enero cae en viernes</div></div>
      <div class="pron-clave"><div class="k">Primera validación</div>
        <div class="v">{v1} al {v2} de enero</div><div class="u">Información de diciembre de 2026</div></div>
      <div class="pron-clave"><div class="k">Informe trimestral REUNE</div>
        <div class="v">{r1} al {r2} de enero</div><div class="u">Primeros 10 días hábiles</div></div>
    </div>
    <div class="pron-grid">
      <div>
        <h3>Días inhábiles que proyectamos</h3>
        <ul class="pron-lista">{filas}</ul>
      </div>
      <div>
        <h3>Cómo lo ha hecho la CONDUSEF</h3>
        <table>
          <tr><th>Año</th><th>Verano</th><th>Fin de año</th></tr>
          <tr><td>2023</td><td>24 al 28 jul</td><td>18 al 29 dic</td></tr>
          <tr><td>2025</td><td>18 al 31 jul</td><td>18 al 31 dic</td></tr>
          <tr><td>2026</td><td>20 al 31 jul</td><td>17 al 31 dic</td></tr>
          <tr><td><b>2027</b></td><td><b>19 al 30 jul</b></td><td><b>17 al 31 dic</b></td></tr>
        </table>
        <p class="nota"><b>Ley:</b> artículo 28 de la Ley Federal de Procedimiento Administrativo
          y calendario oficial. <b>Patrón CONDUSEF:</b> lo ha incluido cada vez que cae entre semana
          (Jueves y Viernes Santo; 2 de noviembre en 2023 y 2026). <b>Estimado:</b> los periodos
          vacacionales cambian cada año; las fechas exactas las fija el acuerdo.</p>
        <p class="nota"><b>Lo que podría moverse:</b> los dos periodos vacacionales y el inicio de
          enero. Algunas dependencias ya declararon inhábiles los primeros días de enero de 2027;
          si la CONDUSEF hiciera lo mismo, la primera ventana se recorrería. Las multas usan la UMA
          de 2026 porque la de 2027 se publica en enero.</p>
      </div>
    </div>
  </section>
""".format(p1=larga(ene["validacion"]["inicio"]).capitalize(),
           v1=int(ene["validacion"]["inicio"][-2:]), v2=int(ene["validacion"]["fin"][-2:]),
           r1=int(ene["reune"]["inicio"][-2:]), r2=int(ene["reune"]["fin"][-2:]),
           filas="".join(filas))
    barra = ('<div class="pronbar"><b>Pronóstico, no es el calendario oficial.</b> '
             'Lo actualizaremos cuando la CONDUSEF publique su acuerdo de días inhábiles de 2027. '
             '<a href="./">Ir a la agenda oficial 2026</a></div>')
    t = plantilla
    CAMBIOS = [
        ("<title>Agenda regulatoria CONDUSEF 2026 · CUMPLIFIX, S.C.</title>",
         "<title>Posible calendario CONDUSEF 2027 · CUMPLIFIX, S.C.</title>"),
        ('content="Agenda gratuita de cumplimiento CONDUSEF 2026: ventanas de validación, fechas límite por registro, sanción mínima por obligación y semáforo anual, con vista por sector financiero."',
         'content="Pronóstico de CUMPLIFIX, S.C. de los días inhábiles y las ventanas de validación ante la CONDUSEF en 2027, mientras se publica el acuerdo oficial."'),
        ('<meta property="og:url" content="https://agenda.cumplifix.com/">',
         '<meta property="og:url" content="https://agenda.cumplifix.com/pronostico-2027.html">'),
        ('<meta property="og:title" content="Agenda regulatoria CONDUSEF 2026 · CUMPLIFIX, S.C.">',
         '<meta property="og:title" content="Posible calendario CONDUSEF 2027 · CUMPLIFIX, S.C.">'),
        ('<link rel="canonical" href="https://agenda.cumplifix.com/">',
         '<link rel="canonical" href="https://agenda.cumplifix.com/pronostico-2027.html">'),
        ('<span class="pill">Agenda gratuita · 2026</span>', '<span class="pill">Pronóstico · 2027</span>'),
        ("<h1>Agenda regulatoria CONDUSEF 2026</h1>", "<h1>Posible calendario CONDUSEF 2027</h1>"),
        ("""Cada día que entres te dice exactamente cuánto falta para la próxima ventana,
        qué obligaciones vencen y qué rango de multa prevé la ley. Sin registro, sin costo.""",
         """Nos adelantamos al acuerdo oficial: estas serían las ventanas de validación de 2027
        con los días inhábiles que proyectamos. Úsalo para planear, no para computar plazos."""),
        ('<a class="btn btn-onblue" href="#descarga">Descargar agenda PDF</a>',
         '<a class="btn btn-onblue" href="#pronostico">Cómo lo calculamos</a>'),
        ("<!--LINK_OTRO_ANIO-->", '<a class="link2027" href="./">← Volver a la agenda oficial 2026</a>'),
        ("<!--BARRA_PRONOSTICO-->", barra),
        ("<!--SECCION_PRONOSTICO-->", seccion),
        ("Semáforo de cumplimiento 2026", "Semáforo de cumplimiento 2027"),
        ("<h2>Agenda de Cumplimiento CONDUSEF 2026</h2>", "<h2>La agenda PDF de 2027, en cuanto haya acuerdo</h2>"),
        ("""<p>Calendario anual con días inhábiles, periodos de validación, fechas límite por obligación
         y la sanción aplicable. Formato imprimible para el expediente de la UNE.</p>""",
         """<p>Publicaremos la agenda imprimible de 2027 cuando la CONDUSEF dé a conocer sus días
         inhábiles. Mientras tanto, la de 2026 sigue vigente.</p>"""),
        ('<a class="btn btn-light" id="btnPdf" href="#" download>Descargar la agenda (PDF)</a>',
         '<a class="btn btn-light" id="btnPdf" href="./">Ver la agenda oficial 2026</a>'),
        ('document.getElementById("btnPdf").href=CONFIG.pdf;', ''),
        ("""Los importes se calculan con un valor diario de la UMA de <b>$113.14</b> para enero de 2026 y
        <b>$117.31</b> a partir de febrero de 2026, ya que la UMA se actualiza el 1 de febrero.""",
         """Los importes se calculan con el valor diario de la UMA de 2026, <b>$117.31</b>, porque el
        de 2027 se publica en enero y entra en vigor el 1 de febrero."""),
        ("""<span class="okbox">Validado contra fuente: los días inhábiles coinciden íntegramente con el
        <b>Acuerdo publicado en el DOF el 23 de diciembre de 2025</b>, por el que la CONDUSEF da a
        conocer los días de 2026 en que cerrará sus puertas y suspenderá operaciones. También se
        contrastó el texto literal de los artículos 136, 143, 158, 160 y 161.</span>""",
         """<span class="okbox" style="background:#FFF4DB;color:#7C4A03">Pronóstico: los días inhábiles
        de 2027 son una estimación de CUMPLIFIX, S.C. y no sustituyen el acuerdo que publicará la
        CONDUSEF en el Diario Oficial de la Federación.</span>"""),
        ('"X-WR-CALNAME:Agenda CONDUSEF "+anio+"', '"X-WR-CALNAME:Pronóstico CONDUSEF "+anio+"'),
        ('"*Agenda Regulatoria CONDUSEF "+anio+"', '"*Posible calendario CONDUSEF "+anio+" (pronóstico)'),
        ("__DATA__", json.dumps(d27, ensure_ascii=False, separators=(",", ":"))),
    ]
    for a, b in CAMBIOS:
        assert t.count(a) == 1, "No se encontró en la plantilla: " + a[:70]
        t = t.replace(a, b)
    return t.replace("__LOGO__", logo).replace("__FAVICON__", favicon)

n27 = escribir("pronostico-2027.html", pagina_pronostico())
# El aviso de privacidad vive en cumplifix.com (apartado XI); aviso-de-privacidad.html solo redirige.
# Si se activa analyticsToken, hay que describir la medición en ese apartado antes de publicar.
# El aviso de privacidad debe describir lo que el sitio realmente hace. El texto del
# apartado de medición se genera a partir del token configurado en la plantilla, para
# que nunca pueda afirmar algo distinto de lo que está publicado.
import re as _re
_tok = _re.search(r'analyticsToken:\s*"([^"]*)"', leer("plantilla.html"))
_tok = _tok.group(1) if _tok else ""
MEDICION = ("" if not _tok else
    " Para conocer el volumen de visitas se utiliza <b>Cloudflare Web Analytics</b>, una "
    "herramienta de medición que <b>no emplea cookies ni identificadores almacenados en su "
    "equipo</b> y que no permite seguirlo entre sitios ni construir un perfil suyo. Recaba "
    "únicamente información técnica agregada —página consultada, sitio de procedencia, tipo "
    "de navegador y dispositivo, y país—, sin recabar su dirección IP de forma que quede "
    "asociada a usted. Por no requerir el almacenamiento de información en su equipo, esta "
    "medición no está sujeta a consentimiento previo.")

n2 = escribir("aviso-de-privacidad.html", leer("aviso.html")
              .replace("__LOGO__", logo).replace("__FAVICON__", favicon)
              .replace("__FECHA__", fecha).replace("__MEDICION__", MEDICION))

escribir("404.html", leer("404.src.html").replace("__LOGO__", logo).replace("__FAVICON__", favicon))

# Archivos de despliegue para GitHub Pages
escribir("CNAME", "agenda.cumplifix.com\n")
escribir(".nojekyll", "")
escribir("robots.txt",
         "User-agent: *\nAllow: /\n\nSitemap: https://agenda.cumplifix.com/sitemap.xml\n")
escribir("sitemap.xml",
         '<?xml version="1.0" encoding="UTF-8"?>\n'
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
         '  <url><loc>https://agenda.cumplifix.com/</loc>'
         '<lastmod>{0}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>\n'
         '  <url><loc>https://agenda.cumplifix.com/pronostico-2027.html</loc>'
         '<lastmod>{0}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'
         '</urlset>\n'.format(hoy.isoformat()))

d = json.loads(datos)
print("index.html                 {:>7,} bytes".format(n1))
print("pronostico-2027.html       {:>7,} bytes".format(n27))
print("aviso-de-privacidad.html   {:>7,} bytes".format(n2))
print("CNAME · .nojekyll · robots.txt · sitemap.xml  escritos")
print("dataset: {} meses · {} obligaciones · {} sectores · {} sistemas".format(
    len(d["meses"]), sum(len(m["obligaciones"]) for m in d["meses"]),
    len(d["sectores"]), len(d["sistemas"])))
