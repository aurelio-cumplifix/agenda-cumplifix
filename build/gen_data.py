# -*- coding: utf-8 -*-
"""
Genera el dataset normativo de la Agenda de Cumplimiento CONDUSEF 2026.

NORMA APLICABLE
  DISPOSICIÓN en Materia de Registros ante la CONDUSEF
  Acuerdo CONDUSEF/JG/2EXT2022/03 · publicada en el DOF el 14 de octubre de 2022.
  Reforma publicada en el DOF el 28 de septiembre de 2023 (arts. 28 fr. I, 64,
  129 fr. I y Anexos I, II y IV): no altera plazos ni el catálogo de reportes.

REGLA DE PLAZOS — ARTÍCULO 12 (texto verificado)
  "Las Instituciones Financieras, dentro de los primeros 5 (cinco) días hábiles de
   cada mes, deberán cumplir con la obligación de presentar la información del mes
   inmediato anterior a través del PUR, utilizando CICI o CIC, accediendo a la
   sección que corresponda de acuerdo a lo siguiente:
     I.    Validación de la información registrada en el SIPRES         → SIPRES
     II.   Reporte de calidad de información / documento de la SIC      → SIPRES
     III.  Validación de datos de la UNE, medios de recepción y niveles → REUNE
     IV.   Actualización de primas de seguros básicos estandarizados    → RESBA
     V.    Registro de Cartera Total, Vigente y Vencida y N.º Contratos → RECO
     VI.   Quejas por prácticas de cobranza y despachos de cobranza     → REDECO
     VII.  Validación de las fichas técnicas del IFIT                   → IFIT
     VIII. Registro y actualización de actividades publicitarias        → REUS"

  "En el caso del Informe Trimestral del REUNE, las Instituciones Financieras,
   dentro de los primeros 10 (diez) días hábiles de los meses de enero, abril,
   julio y octubre, deberán cumplir con la obligación de presentar la información
   del trimestre inmediato anterior."

  Art. 11 — días hábiles: todos los del año salvo sábados, domingos y los del
  acuerdo anual que publica la Comisión Nacional.

MARCO SANCIONADOR
  · LPDUSF art. 94 — rangos en UMAs según la fracción aplicable.
  · LTOSF art. 41  — de 200 a 2,000 UMAs para infracciones a las disposiciones de
    carácter general (aplicable a REDECO conforme al Amparo en Revisión 323/2025).
  Los montos NO son fijos: la ley establece rangos y la individualización
  corresponde a la autoridad. Aquí se maneja el PISO del rango como referencia
  conservadora y se expone el techo por separado.

NIVEL DE VERIFICACIÓN POR OBLIGACIÓN
  "art12"    → sistema y plazo verificados contra el texto literal del art. 12.
  "literal"  → texto del artículo verificado literalmente.
  "inferido" → asignación razonada, pendiente de validación documental.
"""
import json, datetime as dt

ANIO = 2026

# Días inhábiles CONDUSEF 2026 (adicionales a sábados y domingos).
# Fuente: diapositiva 1 del PPTX de la Agenda CumpliFix.
# PENDIENTE DE VALIDACIÓN contra el acuerdo anual publicado por la CONDUSEF.
INHABILES = [
    (1, [1, 2]), (2, [2]), (3, [16]), (4, [2, 3]), (5, [1, 5]),
    (7, [20, 21, 22, 23, 24, 27, 28, 29, 30, 31]),
    (9, [16]), (11, [2, 16]),
    (12, [17, 18, 21, 22, 23, 24, 25, 28, 29, 30, 31]),
]
INHAB = set()
for m, days in INHABILES:
    for d in days:
        INHAB.add(dt.date(ANIO, m, d))

# Valor diario de la UMA. Se actualiza el 1 de febrero de cada año.
UMA = {2025: 113.14, 2026: 117.31}

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
         "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

SECTORES = [
    {"id": "banca",     "nombre": "Instituciones de Banca Múltiple", "corto": "Banca",
     "desc": "Bancos y sus unidades especializadas de atención a usuarios"},
    {"id": "sofom_enr", "nombre": "SOFOM E.N.R.",                    "corto": "SOFOM E.N.R.",
     "desc": "Sociedades Financieras de Objeto Múltiple no reguladas"},
    {"id": "sofom_er",  "nombre": "SOFOM E.R.",                      "corto": "SOFOM E.R.",
     "desc": "Sociedades Financieras de Objeto Múltiple reguladas"},
    {"id": "seguros",   "nombre": "Instituciones de Seguros y Fianzas", "corto": "Seguros",
     "desc": "Aseguradoras y afianzadoras con obligaciones ante CONDUSEF"},
    {"id": "eacp",      "nombre": "SOFIPO, SOFINCO y SOCAP",         "corto": "SOFIPO / SOCAP",
     "desc": "Sector de ahorro y crédito popular"},
    {"id": "uniones",   "nombre": "Uniones de Crédito",              "corto": "Uniones",
     "desc": "Uniones de crédito con cartera registrada"},
    {"id": "ifpe",      "nombre": "IFPE — Fondos de Pago Electrónico", "corto": "IFPE",
     "desc": "Instituciones de fondos de pago electrónico (Ley Fintech)"},
    {"id": "ifc",       "nombre": "IFC — Financiamiento Colectivo",  "corto": "IFC",
     "desc": "Instituciones de financiamiento colectivo (Ley Fintech)"},
    {"id": "bolsa",     "nombre": "Casas de Bolsa y otras",          "corto": "Casas de Bolsa",
     "desc": "Intermediarios bursátiles y demás entidades registradas en SIPRES"},
]

# ---------------------------------------------------------------------------
# Aplicabilidad por sector.
#
# Fuente: DISPOSICIÓN en Materia de Registros ante la CONDUSEF, DOF 14-10-2022,
# artículo 3 (Ámbito de aplicación). Esa norma consolidó en un solo instrumento
# los registros antes dispersos y define, fracción por fracción, qué tipo de
# entidad queda sujeta a cada uno.
#
#   fr. I    Disposiciones generales, PUR, SINE, SIPRES (caps. I a IV), REUNE,
#            BURÓ, REUS y SIGE  →  todas las Instituciones Financieras
#   fr. II   SIPRES caps. V y VI                        →  SOFOM E.N.R.
#   fr. III  RECA y REDECO                              →  instituciones de crédito,
#            SOFOM, SOFIPO, SOFINCO, SOCAP, fiduciarias de fideicomisos de crédito,
#            uniones de crédito e Instituciones de Tecnología Financiera
#   fr. IV   RECAS y RESBA                              →  instituciones de seguros
#   fr. V    RECO                                       →  SOFOM E.N.R., SOFIPO,
#            SOFINCO, SOCAP y uniones de crédito
#
# "Instituciones de Tecnología Financiera" está definido en el art. 4 fr. XVI de
# la Ley Fintech como el género que comprende TANTO a las IFC COMO a las IFPE, de
# modo que la fr. III alcanza a ambas. Ver la nota sobre REDECO en OBSERVACIONES.md.
# ---------------------------------------------------------------------------
TODOS   = ["banca","sofom_enr","sofom_er","seguros","eacp","uniones","ifpe","ifc","bolsa"]
FR_III  = ["banca","sofom_enr","sofom_er","eacp","uniones","ifpe","ifc"]   # RECA y REDECO

# CRITERIO CUMPLIFIX — REDECO no se le requiere a las IFPE.
#
# El art. 3 fr. III enumera genéricamente a las "Instituciones de Tecnología Financiera",
# y el art. 4 fr. XVI de la Ley Fintech define ese género como comprensivo de IFC e IFPE.
# Leído al pie de la letra, el REDECO alcanzaría también a las IFPE.
#
# Confirmado por CumpliFix el 30 de julio de 2026: la redacción de la Disposición es
# defectuosa en este punto y, en los hechos, la obligación no se le requiere a las
# Instituciones de Fondos de Pago Electrónico. Se excluyen del REDECO. Las IFC se
# mantienen, porque su operación sí supone intermediación de financiamiento y, por
# tanto, gestión de cobranza.
REDECO_SEC = ["banca","sofom_enr","sofom_er","eacp","uniones","ifc"]
FR_V    = ["sofom_enr","eacp","uniones"]                                    # RECO
SOLO_EN = ["sofom_enr"]                                                     # SIPRES caps. V y VI
SEGUROS = ["seguros"]                                                       # RESBA

# Rangos de sanción en UMAs. El piso proviene de la Agenda CumpliFix; el techo,
# de los rangos de la LPDUSF art. 94 / LTOSF art. 41. PENDIENTE DE VALIDACIÓN
# la correspondencia fracción por fracción.
CATALOGO = [
    dict(art="Art. 158", sistema="REUS", obl="Reporte de no Consentimiento",
         desc="Reportar a los usuarios que manifestaron no querer recibir publicidad, "
              "dados de alta en la segunda quincena del mes anterior.",
         periodicidad="Quincenal", periodo="q2_anterior", hito="reus1",
         umas=250, umas_max=2000, sancionador="LPDUSF art. 94",
         verif="inferido", sectores=TODOS,   aplic="fr. I"),
    dict(art="Art. 124", sistema="REDECO", obl="Informe de quejas por gestión de cobranza",
         desc="Informe de las quejas relacionadas con la gestión de los despachos de "
              "cobranza que la entidad conozca, capte, reciba o atienda por cualquier medio.",
         periodicidad="Mensual", periodo="anterior", hito="validacion",
         umas=200, umas_max=2000, sancionador="LTOSF art. 41",
         verif="literal", sectores=REDECO_SEC, aplic="fr. III · criterio CumpliFix"),
    dict(art="Art. 130", sistema="REDECO", obl="Registro y actualización de despachos de cobranza",
         desc="Mantener actualizada en el REDECO la información de los despachos de "
              "cobranza contratados, o señalar que no se cuenta con éstos.",
         periodicidad="Mensual", periodo="anterior", hito="validacion",
         umas=200, umas_max=2000, sancionador="LTOSF art. 41",
         verif="art12", sectores=REDECO_SEC, aplic="fr. III · criterio CumpliFix"),
    dict(art="Art. 160", sistema="REUS", obl="Aviso de publicidad dirigida",
         desc="Informar si la institución realizará publicidad dirigida a usuarios "
              "inscritos, conforme al registro de actividades publicitarias del REUS.",
         periodicidad="Mensual", periodo="anterior", hito="validacion",
         umas=250, umas_max=2000, sancionador="LPDUSF art. 94",
         verif="art12", sectores=TODOS,   aplic="fr. I"),
    dict(art="Art. 161", sistema="REUS", obl="Información de la publicidad realizada",
         desc="Registrar y actualizar la información relativa a las actividades "
              "publicitarias o mercadotécnicas efectivamente realizadas.",
         periodicidad="Mensual", periodo="anterior", hito="validacion",
         umas=250, umas_max=2000, sancionador="LPDUSF art. 94",
         verif="art12", sectores=TODOS,   aplic="fr. I"),
    dict(art="Art. 66", sistema="REUNE", obl="Validación de la información de la UNE",
         desc="Validar datos de la Unidad Especializada, medios de recepción o canal y "
              "niveles de atención o contacto registrados en el REUNE.",
         periodicidad="Mensual", periodo="anterior", hito="validacion",
         umas=500, umas_max=2000, sancionador="LPDUSF art. 94, fr. VIII",
         verif="art12", sectores=TODOS,   aplic="fr. I"),
    dict(art="Art. 50", sistema="SIPRES", obl="Validación de información corporativa y datos generales",
         desc="Validar que la información del SIPRES está vigente y actualizada. Durante "
              "el periodo de validación no se puede sustituir al responsable de la CICI.",
         periodicidad="Mensual", periodo="anterior", hito="validacion",
         umas=200, umas_max=1000, sancionador="LPDUSF art. 94",
         verif="literal", sectores=TODOS,   aplic="fr. I"),
    dict(art="Art. 52", sistema="SIPRES", obl="Reporte de calidad de datos (SOFOM)",
         desc="Ingresar el reporte de calidad de información o el documento emitido por "
              "la Sociedad de Información Crediticia respecto de los créditos otorgados.",
         periodicidad="Mensual", periodo="anterior", hito="validacion",
         umas=200, umas_max=1000, sancionador="LPDUSF art. 94",
         verif="literal", sectores=SOLO_EN, aplic="fr. II"),
    dict(art="Art. 143", sistema="IFIT", obl="Validación de fichas técnicas de productos y servicios",
         desc="Validar las fichas técnicas del IFIT que alimentan el Catálogo Nacional de "
              "Productos y Servicios Financieros.",
         periodicidad="Mensual", periodo="anterior", hito="validacion",
         umas=200, umas_max=1000, sancionador="LPDUSF art. 94",
         verif="art12", sectores=TODOS,   aplic="sin verificar"),
    dict(art="Art. 134, Fr. XIII", sistema="IFIT", obl="Programas de Educación Financiera",
         desc="Validar o registrar los programas de educación financiera de la institución.",
         periodicidad="Mensual", periodo="anterior", hito="validacion",
         umas=200, umas_max=1000, sancionador="LPDUSF art. 94",
         verif="inferido", sectores=TODOS,   aplic="sin verificar"),
    dict(art="Art. 115", sistema="RECO", obl="Registro de cartera de crédito",
         desc="Registrar cartera total, vigente y vencida al mes, así como el número de "
              "contratos, en la sección RECO.",
         periodicidad="Mensual", periodo="anterior", hito="validacion",
         umas=200, umas_max=1000, sancionador="LPDUSF art. 94",
         verif="art12", sectores=FR_V,    aplic="fr. V"),
    dict(art="Art. 12, Fr. IV", sistema="RESBA", obl="Actualización de primas de seguros básicos estandarizados",
         desc="Actualizar las primas de tarifas de los seguros básicos estandarizados en "
              "la sección RESBA.",
         periodicidad="Mensual", periodo="anterior", hito="validacion",
         umas=200, umas_max=1000, sancionador="LPDUSF art. 94",
         verif="art12", sectores=SEGUROS, aplic="fr. IV"),
    dict(art="Art. 158", sistema="REUS", obl="Reporte de no Consentimiento",
         desc="Reportar a los usuarios dados de alta en la primera quincena del mes en curso.",
         periodicidad="Quincenal", periodo="q1_curso", hito="reus2",
         umas=250, umas_max=2000, sancionador="LPDUSF art. 94",
         verif="inferido", sectores=TODOS),
    dict(art="Art. 71", sistema="REUNE", obl="Informe trimestral de consultas, aclaraciones y reclamaciones",
         desc="Presentar el informe trimestral del REUNE correspondiente al trimestre "
              "inmediato anterior, dentro de los primeros 10 días hábiles.",
         periodicidad="Trimestral", periodo="trimestre", hito="reune",
         umas=500, umas_max=2000, sancionador="LPDUSF art. 94, fr. VIII",
         verif="art12", sectores=TODOS,   aplic="fr. I"),
]

SISTEMAS = [
    dict(id="REUNE",  nombre="REUNE",  desc="Unidad Especializada de Atención a Usuarios",
         detalle="Datos de la UNE, medios de recepción, niveles de atención e informe trimestral de consultas, aclaraciones y reclamaciones."),
    dict(id="REDECO", nombre="REDECO", desc="Despachos de Cobranza",
         detalle="Registro de despachos contratados e informe mensual de quejas por prácticas de cobranza."),
    dict(id="REUS",   nombre="REUS",   desc="Usuarios de Servicios Financieros",
         detalle="Reporte quincenal de no consentimiento y registro de actividades publicitarias o mercadotécnicas."),
    dict(id="SIPRES", nombre="SIPRES", desc="Prestadores de Servicios Financieros",
         detalle="Información corporativa, datos generales y reporte de calidad de datos crediticios."),
    dict(id="RECO",   nombre="RECO",   desc="Registro de Cartera",
         detalle="Cartera total, vigente y vencida al mes, y número de contratos."),
    dict(id="IFIT",   nombre="IFIT",   desc="Fichas Técnicas y Educación Financiera",
         detalle="Fichas técnicas de productos y servicios del Catálogo Nacional, y programas de educación financiera."),
    dict(id="RESBA",  nombre="RESBA",  desc="Seguros Básicos Estandarizados",
         detalle="Actualización de primas de tarifas de los seguros básicos estandarizados."),
]

TRIMESTRE = {
    1: "octubre, noviembre y diciembre de 2025",
    4: "enero, febrero y marzo de 2026",
    7: "abril, mayo y junio de 2026",
    10: "julio, agosto y septiembre de 2026",
}


def es_habil(d):
    return d.weekday() < 5 and d not in INHAB


def habiles_del_mes(anio, mes):
    d, out = dt.date(anio, mes, 1), []
    while d.month == mes:
        if es_habil(d):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def siguiente_habil(d):
    while not es_habil(d):
        d += dt.timedelta(days=1)
    return d


def uma_de(mes):
    return UMA[2025] if mes == 1 else UMA[2026]


def fmt(d):
    return d.isoformat()


def texto_fecha(d):
    return "{} de {} de {}".format(d.day, MESES[d.month - 1], d.year)


data = {
    "meta": {
        "anio": ANIO,
        "uma": UMA,
        "norma": "Disposición en Materia de Registros ante la CONDUSEF (DOF 14-oct-2022, reforma DOF 28-sep-2023)",
        "regla_plazo": "Art. 12: primeros 5 días hábiles de cada mes, información del mes inmediato anterior. Informe trimestral REUNE: primeros 10 días hábiles de enero, abril, julio y octubre.",
        "zona_horaria": "America/Mexico_City",
        "pdf": "assets/agenda-cumplifix-condusef-2026.pdf",
    },
    "sectores": SECTORES,
    "sistemas": SISTEMAS,
    "inhabiles": sorted(fmt(d) for d in INHAB),
    "meses": [],
}

for mes in range(1, 13):
    hab = habiles_del_mes(ANIO, mes)
    val_ini, val_fin = hab[0], hab[4]
    reus1 = hab[0]
    reus2 = siguiente_habil(dt.date(ANIO, mes, 16))
    reune = {"inicio": fmt(hab[0]), "fin": fmt(hab[9])} if mes in (1, 4, 7, 10) else None

    u = uma_de(mes)
    ma = (mes - 2) % 12 + 1
    aa = ANIO - 1 if mes == 1 else ANIO
    obligaciones = []
    for c in CATALOGO:
        if c["hito"] == "reune" and reune is None:
            continue
        p = c["periodo"]
        if p == "anterior":
            periodo = "Mes de {} de {}".format(MESES[ma - 1], aa)
        elif p == "curso":
            periodo = "Mes de {} de {}".format(MESES[mes - 1], ANIO)
        elif p == "q2_anterior":
            periodo = "2da quincena de {} de {}".format(MESES[ma - 1], aa)
        elif p == "q1_curso":
            periodo = "1era quincena de {} de {}".format(MESES[mes - 1], ANIO)
        else:
            periodo = "Meses de " + TRIMESTRE[mes]

        if c["hito"] == "validacion":
            limite = "Del {} al {} de {} de {}".format(val_ini.day, val_fin.day, MESES[mes - 1].upper(), ANIO)
            ini, fin = fmt(val_ini), fmt(val_fin)
        elif c["hito"] == "reus1":
            limite = "Solo el {}".format(texto_fecha(reus1)); ini = fin = fmt(reus1)
        elif c["hito"] == "reus2":
            limite = "Solo el {}".format(texto_fecha(reus2)); ini = fin = fmt(reus2)
        else:
            limite = "Del {} al {} de {} de {}".format(hab[0].day, hab[9].day, MESES[mes - 1].upper(), ANIO)
            ini, fin = fmt(hab[0]), fmt(hab[9])

        obligaciones.append({
            "art": c["art"], "sistema": c["sistema"], "obligacion": c["obl"],
            "desc": c["desc"], "periodicidad": c["periodicidad"], "periodo": periodo,
            "limite": limite, "inicio": ini, "cierre": fin,
            "umas": c["umas"], "umasMax": c["umas_max"],
            "sancion": round(c["umas"] * u, 2), "sancionMax": round(c["umas_max"] * u, 2),
            "sancionador": c["sancionador"], "verif": c["verif"], "sectores": c["sectores"],
            "aplic": c.get("aplic",""),
        })

    data["meses"].append({
        "mes": mes, "nombre": MESES[mes - 1],
        "validacion": {"inicio": fmt(val_ini), "fin": fmt(val_fin)},
        "reus": [fmt(reus1), fmt(reus2)],
        "reune": reune, "uma": u,
        "obligaciones": obligaciones,
    })

with open("agenda-2026.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

print("OK · {} meses · {} obligaciones/año".format(
    len(data["meses"]), sum(len(m["obligaciones"]) for m in data["meses"])))
for m in data["meses"]:
    tot = sum(o["umas"] for o in m["obligaciones"])
    print("  {:<11} val {} → {} | REUS {} y {} | REUNE {:<7} | {:>2} obl | piso {:>5} UMAs = ${:>11,.2f}".format(
        m["nombre"], m["validacion"]["inicio"][-5:], m["validacion"]["fin"][-5:],
        m["reus"][0][-5:], m["reus"][1][-5:],
        (m["reune"]["inicio"][-5:] + "-" + m["reune"]["fin"][-2:]) if m["reune"] else "—",
        len(m["obligaciones"]), tot, tot * m["uma"]))

print("\nObligaciones por sector (año completo):")
for s in SECTORES:
    n = sum(1 for m in data["meses"] for o in m["obligaciones"] if s["id"] in o["sectores"])
    umas = sum(o["umas"] for m in data["meses"] for o in m["obligaciones"] if s["id"] in o["sectores"])
    print("  {:<32} {:>3} obligaciones · piso {:>6,} UMAs".format(s["nombre"], n, umas))
