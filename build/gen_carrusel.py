# -*- coding: utf-8 -*-
"""Genera el carrusel de lanzamiento de la Agenda CumpliFix.

Produce las láminas en tres proporciones desde una sola definición de contenido:
  LinkedIn   1080x1350
  Instagram  1080x1080
  WhatsApp   1080x1350 (lámina única de difusión)

Se dibuja con HTML y se captura con Chromium para tener control exacto de la
tipografía y del color de marca, en vez de depender de plantillas genéricas.
"""
import os, json, base64, asyncio
from playwright.async_api import async_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(RAIZ, "build")
SALIDA = os.path.join(RAIZ, "lanzamiento")
FUENTES = os.path.join(RAIZ, "assets", "fonts")
os.makedirs(SALIDA, exist_ok=True)

LOGO = open(os.path.join(BUILD, "logo.b64"), encoding="utf-8").read().strip()
DATA = json.load(open(os.path.join(BUILD, "agenda-2026.json"), encoding="utf-8"))


def f64(nombre):
    with open(os.path.join(FUENTES, nombre), "rb") as fh:
        return base64.b64encode(fh.read()).decode()


CSS_FUENTES = """
@font-face{font-family:'Inter';font-weight:400;src:url(data:font/woff2;base64,%s) format('woff2')}
@font-face{font-family:'Inter';font-weight:600;src:url(data:font/woff2;base64,%s) format('woff2')}
@font-face{font-family:'Inter';font-weight:700;src:url(data:font/woff2;base64,%s) format('woff2')}
@font-face{font-family:'Raleway';font-weight:700;src:url(data:font/woff2;base64,%s) format('woff2')}
@font-face{font-family:'Raleway';font-weight:800;src:url(data:font/woff2;base64,%s) format('woff2')}
""" % (f64("inter-latin-400-normal.woff2"), f64("inter-latin-600-normal.woff2"),
       f64("inter-latin-700-normal.woff2"), f64("raleway-latin-700-normal.woff2"),
       f64("raleway-latin-800-normal.woff2"))

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:%(W)spx;height:%(H)spx;overflow:hidden;
  font-family:'Inter',system-ui,sans-serif;color:#0F172A;
  font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
.l{width:%(W)spx;height:%(H)spx;position:relative;display:flex;flex-direction:column;
  padding:%(P)spx;background:#FBFCFE}
.l.oscura{background:linear-gradient(145deg,#071540 0%%,#0B1F5B 42%%,#1C46DC 100%%);color:#fff}
.l.oscura .sub,.l.oscura p{color:#BFD0F5}
h1,h2,.n{font-family:'Raleway',sans-serif;font-weight:800;letter-spacing:-.02em;line-height:1.04}
.eyebrow{font-size:%(EY)spx;font-weight:800;letter-spacing:.14em;text-transform:uppercase;
  color:#1C46DC;margin-bottom:%(G1)spx}
.l.oscura .eyebrow{color:#6FA8FF}
h1{font-size:%(H1)spx}
h2{font-size:%(H2)spx}
p{font-size:%(TX)spx;line-height:1.5;color:#475569;margin-top:%(G1)spx}
.sp{flex:1}
.marca{display:flex;align-items:center;gap:%(G2)spx}
.marca img{width:%(LG)spx;height:%(LG)spx;border-radius:50%%;background:#fff;
  padding:2px;box-shadow:0 0 0 2px rgba(255,255,255,.9)}
.l:not(.oscura) .marca img{box-shadow:0 0 0 1px #DCE3F2}
.marca .t{font-family:'Raleway',sans-serif;font-weight:800;font-size:%(MC)spx;letter-spacing:.02em}
.marca .t i{color:#4FA8FF;font-style:normal}
.pie{display:flex;align-items:flex-end;justify-content:space-between;gap:16px}
.url{font-family:'Raleway',sans-serif;font-weight:800;font-size:%(UR)spx;color:#1C46DC}
.l.oscura .url{color:#8FC2FF}
.num{font-size:%(NU)spx;font-weight:700;color:#94A3B8;letter-spacing:.1em}
.l.oscura .num{color:#7C97D8}
.lema{font-size:%(LE)spx;color:#64748B;font-weight:600}
.l.oscura .lema{color:#AFC6F0}

.cifras{display:flex;gap:%(G3)spx;margin-top:%(G3)spx}
.cifra .v{font-family:'Raleway',sans-serif;font-weight:800;font-size:%(CF)spx;line-height:1;
  letter-spacing:-.03em}
.cifra .k{font-size:%(CK)spx;color:#64748B;margin-top:%(G1)spx;font-weight:600;line-height:1.3}
.l.oscura .cifra .k{color:#BFD0F5}

.lista{margin-top:%(G3)spx;display:flex;flex-direction:column;gap:%(G2)spx}
.item{display:flex;gap:%(G2)spx;align-items:flex-start}
.item .b{width:%(BU)spx;height:%(BU)spx;border-radius:%(BR)spx;flex:none;margin-top:3px;
  background:#EEF2FF;color:#1C46DC;display:grid;place-items:center;
  font-weight:800;font-size:%(BF)spx}
.l.oscura .item .b{background:rgba(255,255,255,.14);color:#fff}
.item .x{font-size:%(IT)spx;line-height:1.4;font-weight:600}
.item .x small{display:block;font-weight:400;color:#64748B;font-size:%(IS)spx;margin-top:2px}
.l.oscura .item .x small{color:#BFD0F5}

.chip{display:inline-block;align-self:flex-start;width:fit-content;
  background:#EEF2FF;color:#1C46DC;border-radius:999px;
  padding:%(CP)s;font-size:%(CS)spx;font-weight:800;letter-spacing:.06em;text-transform:uppercase}
.l.oscura .chip{background:rgba(255,255,255,.16);color:#fff}
.regs{display:flex;flex-wrap:wrap;gap:%(G1)spx;margin-top:%(G3)spx}
.reg{border-radius:%(RR)spx;padding:%(RP)s;font-weight:800;font-size:%(RS)spx;
  letter-spacing:.04em;color:#fff}
.marco{border:2px solid #E2E8F0;border-radius:%(MR)spx;padding:%(MP)spx;margin-top:%(G3)spx;
  background:#fff}
.l.oscura .marco{border-color:rgba(255,255,255,.22);background:rgba(255,255,255,.07)}
.marco .h{font-size:%(MH)spx;font-weight:800;letter-spacing:.1em;text-transform:uppercase;
  color:#94A3B8;margin-bottom:%(G1)spx}
.l.oscura .marco .h{color:#9FB8EC}
.marco .c{font-family:'Raleway',sans-serif;font-weight:800;font-size:%(MF)spx;line-height:1.1}
"""

COLORES = {"REUNE": "#0891B2", "REDECO": "#C21F73", "REUS": "#B45309", "SIPRES": "#1C46DC",
           "RECO": "#15803D", "IFIT": "#6D28D9", "RESBA": "#BE123C"}


def laminas(total):
    """Contenido de cada lámina. `total` sirve para numerar el pie."""
    regs = "".join(
        '<span class="reg" style="background:%s">%s</span>' % (COLORES[k], k)
        for k in ["SIPRES", "REUNE", "REUS", "REDECO", "RECO", "IFIT", "RESBA"])
    return [
        # 1 · Portada
        dict(oscura=True, cuerpo="""
          <div class="eyebrow">Versión 1.0 · Gratuita</div>
          <h1>Agenda<br>Regulatoria<br>CONDUSEF<br>2026</h1>
          <p>La primera agenda pública que te dice, cada día,<br>
             qué le debes a la CONDUSEF.</p>
          <div class="sp"></div>
          <span class="chip">Sin costo · Sin registro</span>"""),
        # 2 · El problema
        dict(cuerpo="""
          <div class="eyebrow">El problema de siempre</div>
          <h2>¿Sabes hoy,<br>sin abrir nada,<br>qué tienes que<br>reportar?</h2>
          <p>La ventana de validación cambia de fecha cada mes.
             El REUS es quincenal. El REUNE es trimestral. Y los días
             inhábiles mueven todo.</p>
          <div class="sp"></div>
          <div class="marco">
            <div class="h">Lo que suele pasar</div>
            <div class="c">Te enteras el día que<br>ya cerró la ventana.</div>
          </div>"""),
        # 3 · La dimensión
        dict(cuerpo="""
          <div class="eyebrow">La dimensión real</div>
          <h2>160 obligaciones<br>al año. Siete<br>registros distintos.</h2>
          <div class="regs">%s</div>
          <p>Cada uno con su periodo que se reporta, su fecha límite
             y su sanción aplicable.</p>
          <div class="sp"></div>
          <div class="cifras">
            <div class="cifra"><div class="v">160</div><div class="k">obligaciones<br>en el año</div></div>
            <div class="cifra"><div class="v">7</div><div class="k">registros<br>CONDUSEF</div></div>
            <div class="cifra"><div class="v">12</div><div class="k">ventanas de<br>validación</div></div>
          </div>""" % regs),
        # 4 · La solución
        dict(cuerpo="""
          <div class="eyebrow">Lo que hicimos</div>
          <h2>Un solo lugar<br>que se actualiza<br>solo.</h2>
          <div class="lista">
            <div class="item"><div class="b">1</div><div class="x">Qué te toca hoy
              <small>Estado del día y cuenta regresiva a la próxima ventana</small></div></div>
            <div class="item"><div class="b">2</div><div class="x">Cuándo vence
              <small>Calendario con días inhábiles y periodos de validación</small></div></div>
            <div class="item"><div class="b">3</div><div class="x">Cuánto cuesta no hacerlo
              <small>Sanción mínima por obligación, en UMAs y en pesos</small></div></div>
            <div class="item"><div class="b">4</div><div class="x">Qué llevas del año
              <small>Semáforo de enero a hoy, con la exposición acumulada</small></div></div>
          </div>"""),
        # 5 · Por sector
        dict(cuerpo="""
          <div class="eyebrow">Lo más pedido</div>
          <h2>Solo lo que<br>a ti te aplica.</h2>
          <p>No es lo mismo una SOFOM E.N.R. que una IFPE. El RECO no le
             aplica a un banco. El RESBA solo a seguros.</p>
          <div class="lista">
            <div class="item"><div class="b">✓</div><div class="x">Nueve tipos de institución
              <small>Banca, SOFOM E.R. y E.N.R., Seguros, SOFIPO y SOCAP,
                     Uniones de Crédito, IFPE, IFC y Casas de Bolsa</small></div></div>
            <div class="item"><div class="b">✓</div><div class="x">Con fundamento, no a ojo
              <small>Conforme al art. 3 de la Disposición en Materia de Registros
                     ante la CONDUSEF, DOF 14-10-2022</small></div></div>
          </div>"""),
        # 6 · Utilidades
        dict(cuerpo="""
          <div class="eyebrow">Además</div>
          <h2>Se lleva<br>a tu operación.</h2>
          <div class="lista">
            <div class="item"><div class="b">↓</div><div class="x">Agenda completa en PDF
              <small>15 páginas, una por mes, lista para el expediente</small></div></div>
            <div class="item"><div class="b">↓</div><div class="x">El año entero a tu calendario
              <small>Archivo .ics para Outlook, Google Calendar o Apple</small></div></div>
            <div class="item"><div class="b">↓</div><div class="x">Lista de verificación mensual
              <small>CSV con casillas de avance que se guardan en tu navegador</small></div></div>
          </div>
          <p>Todo sin cuenta, sin costo y sin dejar tus datos.</p>"""),
        # 7 · Cierre
        dict(oscura=True, cuerpo="""
          <div class="eyebrow">Ya está en línea</div>
          <h1>agenda.<br>cumplifix<br>.com</h1>
          <p>Ábrela hoy. Te dice en un vistazo si vas al corriente
             o si ya se te cerró algo.</p>
          <div class="sp"></div>
          <div class="marco">
            <div class="h">Versión 1.0</div>
            <div class="c">Esto apenas empieza.<br>Va a seguir creciendo.</div>
          </div>"""),
    ]


ESC = {
    "linkedin":  dict(W=1080, H=1350, P=88, H1=104, H2=82, TX=30, EY=20, CF=86, CK=21,
                      IT=30, IS=21, LG=62, MC=34, UR=27, NU=19, LE=20, BU=44, BR=13, BF=21,
                      G1=13, G2=19, G3=40, CP="14px 26px", CS=19, RR=11, RP="10px 17px", RS=20,
                      MR=20, MP=32, MH=17, MF=38),
    "instagram": dict(W=1080, H=1080, P=76, H1=90, H2=70, TX=27, EY=18, CF=74, CK=19,
                      IT=27, IS=19, LG=54, MC=30, UR=25, NU=17, LE=18, BU=40, BR=12, BF=19,
                      G1=11, G2=16, G3=30, CP="12px 23px", CS=17, RR=10, RP="9px 15px", RS=18,
                      MR=18, MP=27, MH=15, MF=33),
}


def html(lam, esc, i, total):
    v = dict(esc)
    marca = ('<div class="marca"><img src="%s">'
             '<div class="t">CUMPLI<i>FIX</i></div></div>' % LOGO)
    pie = ('<div class="pie"><div><div class="url">agenda.cumplifix.com</div>'
           '<div class="lema">Cumple tus metas, nosotros tu cumplimiento</div></div>'
           '<div class="num">%d / %d</div></div>' % (i, total))
    return ("<!doctype html><meta charset='utf-8'><style>" + CSS_FUENTES + (BASE % v) +
            "</style><div class='l%s'>%s<div style='height:%dpx'></div>%s<div class='sp'></div>%s</div>"
            % (" oscura" if lam.get("oscura") else "", marca, v["G3"], lam["cuerpo"], pie))


async def main():
    total = len(laminas(0))
    lams = laminas(total)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for red, esc in ESC.items():
            pg = await b.new_page(viewport={"width": esc["W"], "height": esc["H"]},
                                  device_scale_factor=1)
            carpeta = os.path.join(SALIDA, red)
            os.makedirs(carpeta, exist_ok=True)
            for i, lam in enumerate(lams, 1):
                await pg.set_content(html(lam, esc, i, total))
                await pg.wait_for_timeout(260)
                await pg.screenshot(path=os.path.join(carpeta, "%02d.png" % i))
            await pg.close()
            print("%-10s %d láminas · %dx%d" % (red, len(lams), esc["W"], esc["H"]))

        # WhatsApp: una sola imagen de difusión, con lo esencial
        esc = dict(ESC["linkedin"])
        pg = await b.new_page(viewport={"width": esc["W"], "height": esc["H"]})
        wa = dict(oscura=True, cuerpo="""
          <div class="eyebrow">Nuevo · Gratuito</div>
          <h1>Agenda<br>CONDUSEF<br>2026</h1>
          <p>Te dice cada día qué debes reportar,
             cuándo vence y cuánto cuesta no hacerlo.</p>
          <div class="cifras">
            <div class="cifra"><div class="v">160</div><div class="k">obligaciones</div></div>
            <div class="cifra"><div class="v">7</div><div class="k">registros</div></div>
            <div class="cifra"><div class="v">9</div><div class="k">sectores</div></div>
          </div>
          <div class="sp"></div>
          <span class="chip">Sin costo · Sin registro</span>""")
        await pg.set_content(html(wa, esc, 1, 1).replace(
            '<div class="num">1 / 1</div>', '<div class="num"></div>'))
        await pg.wait_for_timeout(260)
        await pg.screenshot(path=os.path.join(SALIDA, "whatsapp-difusion.png"))
        print("%-10s 1 imagen · %dx%d" % ("whatsapp", esc["W"], esc["H"]))
        await b.close()


asyncio.run(main())
