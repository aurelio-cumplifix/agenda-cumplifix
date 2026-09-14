# -*- coding: utf-8 -*-
"""Genera la Agenda de Cumplimiento CONDUSEF 2026 en PDF a partir del mismo dataset del sitio."""
import json, os, base64, datetime as dt
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
D = json.load(open(os.path.join(AQUI, "agenda-2026.json"), encoding="utf-8"))
LOGO = open(os.path.join(AQUI, "logo.b64"), encoding="utf-8").read()
MESES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto",
         "septiembre","octubre","noviembre","diciembre"]
DIAS = ["D","L","M","M","J","V","S"]
INH = set(D["inhabiles"])
ANIO = D["meta"]["anio"]
HOYTXT = "{} de {} de {}".format(dt.date.today().day, MESES[dt.date.today().month-1], dt.date.today().year)


def dia(s):
    a = [int(x) for x in s.split("-")]
    return dt.date(a[0], a[1], a[2])


def inhabil(d):
    return d.weekday() >= 5 or d.isoformat() in INH


def money(n):
    return "$" + format(round(n, 2), ",.2f")


def calendario(m, compacto=False):
    mes = m["mes"]
    primero = dt.date(ANIO, mes, 1)
    ndias = (dt.date(ANIO + (mes == 12), mes % 12 + 1, 1) - dt.timedelta(days=1)).day
    off = (primero.weekday() + 1) % 7
    out = ['<table class="cal' + (" mini" if compacto else "") + '">']
    if compacto:
        out.append('<caption>' + MESES[mes-1].upper() + '</caption>')
    out.append("<tr>" + "".join("<th>%s</th>" % x for x in DIAS) + "</tr><tr>")
    c = 0
    for _ in range(off):
        out.append("<td></td>"); c += 1
    for n in range(1, ndias + 1):
        d = dt.date(ANIO, mes, n); s = d.isoformat()
        # Un día concentra varios hitos: el REUS quincenal cae en el primer día
        # de la ventana de validación y el REUNE la abarca completa. El fondo
        # lleva la banda dominante; los hitos tapados se marcan con un punto.
        ev = []
        if m["validacion"]["inicio"] <= s <= m["validacion"]["fin"]: ev.append("val")
        if s in m["reus"]: ev.append("reus")
        if m["reune"] and m["reune"]["inicio"] <= s <= m["reune"]["fin"]: ev.append("reune")
        bg = ("inh" if inhabil(d)
              else "val" if "val" in ev
              else "reune" if "reune" in ev
              else "reus" if "reus" in ev else "")
        pts = [e for e in ev if e != bg and e != "val"]
        mk = ('<span class="mk">%s</span>'
              % "".join('<i class="k-%s"></i>' % p for p in pts)) if pts else ""
        out.append('<td class="%s">%d%s</td>' % (bg, n, mk)); c += 1
        if c % 7 == 0: out.append("</tr><tr>")
    while c % 7 != 0:
        out.append("<td></td>"); c += 1
    out.append("</tr></table>")
    return "".join(out)


FUENTES = os.path.join(RAIZ, "assets", "fonts")
CSS = ("""
@font-face{font-family:'Inter';font-weight:400;src:url('file://""" + FUENTES + """/inter-latin-400-normal.woff2')}
@font-face{font-family:'Inter';font-weight:600;src:url('file://""" + FUENTES + """/inter-latin-600-normal.woff2')}
@font-face{font-family:'Inter';font-weight:700;src:url('file://""" + FUENTES + """/inter-latin-700-normal.woff2')}
@font-face{font-family:'Raleway';font-weight:700;src:url('file://""" + FUENTES + """/raleway-latin-700-normal.woff2')}
@font-face{font-family:'Raleway';font-weight:800;src:url('file://""" + FUENTES + """/raleway-latin-800-normal.woff2')}
""" + """
@page{size:A4 landscape;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:'Inter','DejaVu Sans',Arial,sans-serif;color:#0F172A;font-size:8.6pt;line-height:1.35;font-variant-numeric:tabular-nums}
h1,h2,h3,.hd .t b,.cover h1,.cover .lema,.cover .stats b{font-family:'Raleway','Inter',Arial,sans-serif;font-weight:800}
.page{page-break-after:always;height:210mm;padding:11mm 10mm 9mm;display:flex;flex-direction:column;overflow:hidden}
.page:last-child{page-break-after:auto}
h1,h2,h3{margin:0;letter-spacing:-.01em}
.hd{display:flex;align-items:center;gap:9px;border-bottom:2.2px solid #1C46DC;padding-bottom:6px;margin-bottom:9px}
.hd img{width:30px;height:30px;border-radius:50%}
.hd .t{flex:1}
.hd .t b{font-size:12.5pt;font-weight:800;letter-spacing:-.02em;color:#0B1F5B;display:block}
.hd .t span{font-size:7.2pt;letter-spacing:.16em;text-transform:uppercase;color:#5B6B84}
.hd .r{text-align:right;font-size:7.4pt;color:#5B6B84}
.hd .r b{display:block;font-size:11pt;color:#1C46DC;text-transform:capitalize}
.ft{margin-top:auto;display:flex;justify-content:space-between;gap:10px;
  font-size:6.6pt;color:#8494AC;border-top:1px solid #E2E8F0;padding-top:5px}
.body{flex:1}
table.ob{width:100%;border-collapse:collapse;font-size:7.5pt}
table.ob th{background:#0B1F5B;color:#fff;text-align:left;padding:5px 5px;font-size:6.5pt;
  letter-spacing:.05em;text-transform:uppercase;font-weight:700}
table.ob td{padding:4.5px 5px;border-bottom:.6px solid #E2E8F0;vertical-align:top}
table.ob tr:nth-child(even) td{background:#F8FAFC}
table.ob .c{text-align:center}.ob .r{text-align:right;white-space:nowrap}
.badge{display:inline-block;background:#EEF2FF;color:#1C46DC;border-radius:3px;padding:1px 4px;
  font-size:6.4pt;font-weight:800}
.box{width:11px;height:11px;border:1.1px solid #94A3B8;border-radius:2px;display:inline-block}
table.cal{border-collapse:separate;border-spacing:1.6px;font-size:7.2pt;table-layout:fixed;width:100%}
table.cal caption{font-size:7pt;font-weight:800;letter-spacing:.08em;color:#0B1F5B;text-align:left;padding-bottom:2px}
table.cal th{font-size:6.2pt;color:#8494AC;font-weight:700;padding:0}
table.cal td{position:relative;height:14px;text-align:center;border-radius:2.5px;background:#fff;
  border:.5px solid #EDF1F7;color:#334155;font-weight:600;padding-bottom:3px}
table.cal td .mk{position:absolute;left:0;right:0;bottom:1.5px;text-align:center;line-height:0}
table.cal td .mk i{display:inline-block;width:2.2px;height:2.2px;border-radius:50%;margin:0 .6px}
table.cal td .mk .k-reus{background:#C98A00}
table.cal td .mk .k-reune{background:#0E93B0}
table.cal td.inh{background:#EDF1F7;color:#94A3B8;border-color:#EDF1F7}
table.cal td.val{background:#FDE7F2;color:#9D1B5F;border-color:#F9C2DD}
table.cal td.reus{background:#FDF0DC;color:#8A5A00;border-color:#F3D9AC}
table.cal td.reune{background:#DCF4FA;color:#046C86;border-color:#AEE4F0}
table.cal.mini td{height:11.5px;font-size:6.4pt}
.leg{display:flex;gap:11px;flex-wrap:wrap;font-size:6.8pt;color:#5B6B84;margin-top:6px}
.leg i{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:3px;vertical-align:-1px}
.grid12{display:grid;grid-template-columns:repeat(6,1fr);gap:7px 9px}
.two{display:grid;grid-template-columns:132px 1fr;gap:11px;align-items:start}
.kv{font-size:7.2pt;color:#5B6B84;margin-top:7px}
.kv div{display:flex;justify-content:space-between;gap:6px;padding:2px 0;border-bottom:.5px dotted #DDE3EC}
.kv b{color:#0F172A}
.cover{background:linear-gradient(135deg,#081848,#0B1F5B 45%,#1C46DC);color:#fff;flex:1;
  margin:-11mm -10mm -9mm;padding:30mm 24mm 20mm;display:flex;flex-direction:column;justify-content:space-between}
.cover h1{font-size:31pt;line-height:1.06;max-width:15ch;margin:12px 0 10px}
.cover .sub{font-size:11pt;opacity:.88;max-width:52ch}
.cover .lema{font-size:12pt;font-weight:800;margin-top:5px}
.cover .lema span{display:block;font-size:8.4pt;font-weight:400;opacity:.82;margin-top:3px}
.cover img{width:60px;height:60px;border-radius:50%;background:#fff}
.cover .stats{display:flex;gap:26px;margin-top:20px}
.cover .stats b{display:block;font-size:19pt;font-weight:800}
.cover .stats span{font-size:7.6pt;opacity:.8}
.note{font-size:7pt;color:#5B6B84;line-height:1.5}
.note b{color:#0F172A}
h2.sec{font-size:12pt;color:#0B1F5B;margin-bottom:3px}
p.sub{font-size:7.6pt;color:#5B6B84;margin:0 0 8px}
.warn{background:#FEF3C7;border:.7px solid #FCD9A0;color:#7C4A03;border-radius:5px;padding:7px 9px;font-size:7pt;margin-top:7px}
.cols2{column-count:2;column-gap:11mm;font-size:7.2pt;color:#334155;line-height:1.55}
.cols2 h3{font-size:8.4pt;color:#0B1F5B;margin:0 0 4px;break-after:avoid}
.cols2 p{margin:0 0 9px}
""")


def encabezado(titulo, derecha_top, derecha):
    return ('<div class="hd"><img src="%s"><div class="t"><b>CumpliFix S.C. · Agenda de Cumplimiento CONDUSEF %d</b>'
            '<span>%s</span></div><div class="r">%s<b>%s</b></div></div>'
            % (LOGO, ANIO, titulo, derecha_top, derecha))


def pie(n):
    return ('<div class="ft"><span>CumpliFix S.C. · Cumple tus metas, nosotros tu cumplimiento</span>'
            '<span>info@cumplifix.com · 55-7146-2367 · agenda.cumplifix.com</span>'
            '<span>%s</span></div>' % n)


P = []

# --- Portada
tot_obl = sum(len(m["obligaciones"]) for m in D["meses"])
tot_umas = sum(o["umas"] for m in D["meses"] for o in m["obligaciones"])
P.append('<div class="page"><div class="cover"><div><img src="%s">'
         '<h1>Agenda de Cumplimiento CONDUSEF %d</h1>'
         '<div class="sub">Calendario anual de obligaciones ante la Comisión Nacional para la Protección '
         'y Defensa de los Usuarios de Servicios Financieros. Días inhábiles, periodos de validación, '
         'fechas límite por registro y sanción aplicable.</div>'
         '<div class="stats"><div><b>%d</b><span>obligaciones en el año</span></div>'
         '<div><b>%d</b><span>registros CONDUSEF</span></div>'
         '<div><b>%s</b><span>UMAs de exposición mínima</span></div></div></div>'
         '<div><div class="lema">CumpliFix S.C.<span>Cumple tus metas, nosotros tu cumplimiento</span></div>'
         '<div style="font-size:7.4pt;opacity:.75;margin-top:10px">info@cumplifix.com · 55-7146-2367 · '
         'www.cumplifix.com · Actualizada al %s</div></div></div></div>'
         % (LOGO, ANIO, tot_obl, len(D["sistemas"]), format(tot_umas, ","), HOYTXT))

# --- Calendario anual
P.append('<div class="page">' + encabezado("Calendario anual", "Ejercicio", str(ANIO)) +
         '<h2 class="sec">Días inhábiles y periodos de cumplimiento ' + str(ANIO) + '</h2>'
         '<p class="sub">Conforme al artículo 12 de la Disposición en Materia de Registros ante la CONDUSEF: '
         'los primeros 5 días hábiles de cada mes para la información del mes inmediato anterior, y los primeros '
         '10 días hábiles de enero, abril, julio y octubre para el informe trimestral del REUNE.</p>'
         '<div class="body"><div class="grid12">' + "".join(calendario(m, True) for m in D["meses"]) + '</div>'
         '<div class="leg"><span><i style="background:#FDE7F2;border:1px solid #F9C2DD"></i>Periodo de validación</span>'
         '<span><i style="background:#FDF0DC;border:1px solid #F3D9AC"></i>Reporte quincenal REUS</span>'
         '<span><i style="background:#DCF4FA;border:1px solid #AEE4F0"></i>Informe trimestral REUNE</span>'
         '<span><i style="background:#EDF1F7"></i>Día inhábil (sábados, domingos y acuerdo CONDUSEF)</span>'
         '<span style="color:#8494AC"><i style="background:#C98A00;width:3px;height:3px;border-radius:50%"></i>'
         '<i style="background:#0E93B0;width:3px;height:3px;border-radius:50%"></i>'
         'El punto marca un hito que coincide con otro el mismo día</span></div>'
         '<div class="warn"><b>Pendiente de validación:</b> los días inhábiles marcados provienen de la agenda '
         'CumpliFix S.C. y deben contrastarse con el acuerdo anual publicado por la Comisión Nacional.</div></div>'
         + pie("Página 2") + '</div>')

# --- Páginas mensuales
for i, m in enumerate(D["meses"]):
    mes = m["mes"]
    filas = []
    for n, o in enumerate(m["obligaciones"], 1):
        filas.append(
            '<tr><td class="c"><span class="box"></span></td><td class="c">%d</td>'
            '<td><span class="badge">%s</span></td>'
            '<td><b>%s</b><br><span style="color:#5B6B84">%s · %s</span></td>'
            '<td>%s</td><td>%s</td><td>%s</td>'
            '<td class="r"><b style="color:#BE123C">%s</b><br>'
            '<span style="color:#5B6B84;font-size:6.6pt">desde %d UMAs</span></td>'
            '<td style="border-bottom:.6px solid #E2E8F0;min-width:56px"></td></tr>'
            % (n, o["sistema"], o["obligacion"], o["art"], o["sancionador"],
               o["periodicidad"], o["periodo"], o["limite"], money(o["sancion"]), o["umas"]))
    umas = sum(o["umas"] for o in m["obligaciones"])
    piso = sum(o["sancion"] for o in m["obligaciones"])
    kv = [("Periodo de validación", "%s al %s" % (dia(m["validacion"]["inicio"]).day, dia(m["validacion"]["fin"]).day)),
          ("Reporte quincenal REUS", "%d y %d" % (dia(m["reus"][0]).day, dia(m["reus"][1]).day)),
          ("Informe trimestral REUNE", "%d al %d" % (dia(m["reune"]["inicio"]).day, dia(m["reune"]["fin"]).day)) if m["reune"] else ("Informe trimestral REUNE", "No aplica"),
          ("Obligaciones", str(len(m["obligaciones"]))),
          ("UMA aplicable", money(m["uma"])),
          ("Exposición mínima", money(piso))]
    P.append('<div class="page">' + encabezado("Agenda mensual", "Mes", MESES[mes-1] + " " + str(ANIO)) +
             '<div class="body"><div class="two"><div>' + calendario(m) +
             '<div class="leg" style="font-size:6.2pt"><span><i style="background:#FDE7F2"></i>Validación</span>'
             '<span><i style="background:#FDF0DC"></i>REUS</span>'
             '<span><i style="background:#DCF4FA"></i>REUNE</span>'
             '<span><i style="background:#EDF1F7"></i>Inhábil</span></div>'
             '<div class="kv">' + "".join('<div><span>%s</span><b>%s</b></div>' % k for k in kv) + '</div></div>'
             '<div><table class="ob"><tr><th style="width:20px">✓</th><th style="width:18px">#</th>'
             '<th style="width:52px">Registro</th><th>Obligación y fundamento</th>'
             '<th style="width:52px">Period.</th><th style="width:15%">Periodo que se reporta</th>'
             '<th style="width:16%">Fecha límite</th><th style="width:78px" class="r">Sanción mín.</th>'
             '<th style="width:56px">Acuse / folio</th></tr>' + "".join(filas) + '</table>'
             '<div style="display:flex;justify-content:space-between;font-size:7pt;color:#5B6B84;margin-top:5px">'
             '<span>Marca cada obligación y anota el folio del acuse. Este documento es evidencia de control interno.</span>'
             '<span>Total: <b style="color:#0F172A">%d obligaciones · desde %s UMAs</b></span></div></div></div>'
             % (len(m["obligaciones"]), format(umas, ",")) + '</div>' + pie("Página %d" % (i + 3)) + '</div>')

# --- Notas
P.append('<div class="page">' + encabezado("Fuentes, supuestos y trazabilidad", "Documento", "Notas") +
         '<h2 class="sec">Cómo se construyó esta agenda</h2>'
         '<p class="sub">Trazabilidad de cada dato para que puedas defenderla ante una revisión.</p>'
         '<div class="body"><div class="cols2">'
         '<h3>Norma aplicable</h3><p>Disposición en Materia de Registros ante la CONDUSEF, aprobada por acuerdo '
         'CONDUSEF/JG/2EXT2022/03 y publicada en el Diario Oficial de la Federación el 14 de octubre de 2022, '
         'con reforma publicada en el DOF el 28 de septiembre de 2023.</p>'
         '<h3>Regla de plazos — artículo 12</h3><p>Dentro de los primeros 5 días hábiles de cada mes debe '
         'presentarse la información del mes inmediato anterior a través del PUR, en la sección que corresponda: '
         'SIPRES (fracciones I y II), REUNE (III), RESBA (IV), RECO (V), REDECO (VI), IFIT (VII) y REUS (VIII). '
         'El informe trimestral del REUNE se presenta dentro de los primeros 10 días hábiles de enero, abril, '
         'julio y octubre, por el trimestre inmediato anterior.</p>'
         '<h3>Días hábiles — artículo 11</h3><p>Son hábiles todos los días del año con excepción de sábados y '
         'domingos, así como aquellos establecidos en el acuerdo que cada año publica la Comisión Nacional.</p>'
         '<h3>Valor de la UMA</h3><p>Los importes se calculan con un valor diario de $113.14 para enero de 2026 '
         'y de $117.31 a partir de febrero de 2026, ya que la UMA se actualiza el 1 de febrero de cada año. '
         'Verifica el valor vigente publicado por el INEGI en el DOF antes de usar estas cifras en un escrito formal.</p>'
         '<h3>Sobre las sanciones</h3><p>Las cantidades señaladas son el <b>piso del rango legal</b>, no una multa '
         'fija. La Ley de Protección y Defensa al Usuario de Servicios Financieros (artículo 94) y la Ley para la '
         'Transparencia y Ordenamiento de los Servicios Financieros (artículo 41) establecen rangos —de 200 a 2,000 '
         'UMAs o más, según la fracción aplicable— y la individualización de la sanción corresponde a la autoridad, '
         'que además puede duplicarla en caso de reincidencia.</p>'
         '<h3>Pendientes de validación</h3><p>Acuerdo anual de días inhábiles 2026; texto literal de los artículos '
         '66, 71, 115, 130, 134 fracción XIII, 143, 158, 160 y 161; y la fracción sancionadora concreta que '
         'corresponde a cada obligación. La asignación de obligaciones por tipo de institución es un criterio '
         'orientativo de CumpliFix S.C. y debe validarse caso por caso conforme al objeto social, la autorización y '
         'los productos de cada entidad.</p>'
         '<h3>Aviso</h3><p>Este documento es información de carácter general con fines preventivos. No sustituye '
         'la consulta directa de las disposiciones vigentes ni la asesoría profesional sobre el caso concreto. '
         'CumpliFix S.C. no asume responsabilidad por decisiones tomadas exclusivamente con base en este contenido.</p>'
         '<h3>Versión siempre actualizada</h3><p>Consulta el estado del día, el semáforo anual de cumplimiento y '
         'la agenda personalizada por sector en <b>agenda.cumplifix.com</b>. Ahí puedes exportar el calendario a '
         'tu agenda electrónica y descargar la lista de verificación mensual.</p>'
         '</div></div>' + pie("Página %d" % (len(D["meses"]) + 3)) + '</div>')

HTML = "<!DOCTYPE html><html lang='es-MX'><head><meta charset='utf-8'><style>%s</style></head><body>%s</body></html>" % (CSS, "".join(P))

tmp = os.path.join(AQUI, "_agenda.html")
open(tmp, "w", encoding="utf-8").write(HTML)
salida = os.path.join(RAIZ, "assets", "agenda-cumplifix-condusef-2026.pdf")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto("file://" + tmp)
    pg.wait_for_timeout(700)
    pg.pdf(path=salida, format="A4", landscape=True, print_background=True,
           margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
    b.close()
os.remove(tmp)
print("PDF generado:", salida, round(os.path.getsize(salida) / 1024, 1), "KB")
