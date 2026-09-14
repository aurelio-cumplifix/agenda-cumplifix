# Observaciones normativas — Agenda CONDUSEF 2026

Documento de trabajo para CumpliFix S.C. Registra lo verificado, lo corregido, lo asumido y lo
que requiere validación documental antes de difundir el micrositio y la siguiente edición del PDF.

**Fuentes revisadas:** Agenda de Cumplimiento Anual CumpliFix – CONDUSEF 2026 (PPTX, 10 diapositivas);
Disposición en Materia de Registros ante la CONDUSEF; LPDUSF; LTOSF; Amparo en Revisión 323/2025 (SCJN).
**Fecha del análisis:** 29 de julio de 2026.

---

## 0. Matriz de aplicabilidad por sector — RECONSTRUIDA

**Actualizado el 30 de julio de 2026.** Esta sección sustituye la asignación por sector de la
primera versión, que estaba construida por inferencia. Ahora tiene fundamento normativo expreso.

### La norma que resuelve la pregunta

**DISPOSICIÓN en Materia de Registros ante la CONDUSEF**, DOF **14 de octubre de 2022**, con
modificación de Anexos por ACUERDO del **28 de septiembre de 2023**.

Esa Disposición consolidó en un solo instrumento los registros antes dispersos —SIPRES, REUNE,
RECA, RECAS, RESBA, RECO, REDECO, REUS, SIGE, SINE, IFIT— bajo el Portal Único de Registros
(PUR). Su **artículo 3 (Ámbito de aplicación)** dice, fracción por fracción, qué tipo de entidad
queda sujeta a cada registro:

| Fracción | Registros | Sujetos obligados |
|---|---|---|
| **I** | Disposiciones generales, PUR, SINE, **SIPRES** (caps. I–IV), **REUNE**, BURÓ, **REUS**, SIGE | Todas las Instituciones Financieras |
| **II** | SIPRES caps. V y VI | **SOFOM E.N.R.** |
| **III** | **RECA y REDECO** | Instituciones de crédito, SOFOM, SOFIPO, SOFINCO, SOCAP, fiduciarias de fideicomisos que otorguen crédito, uniones de crédito e **Instituciones de Tecnología Financiera** |
| **IV** | RECAS y **RESBA** | Instituciones de Seguros |
| **V** | **RECO** | **SOFOM E.N.R.**, SOFIPO, SOFINCO, SOCAP y uniones de crédito |

Fuentes: [PDF CONDUSEF](https://www.condusef.gob.mx/documentos/marco_legal/DispRegistrosAnte-CONDUSEF.pdf) ·
[DOF 14-10-2022](https://dof.gob.mx/nota_detalle.php?codigo=5668453&fecha=14%2F10%2F2022) ·
[ACUERDO de reformas, sep-2023](https://www.condusef.gob.mx/documentos/marco_legal/AcuerdoReformasDR-sep2023.pdf)

### Cambios aplicados

**1. Se separaron IFPE e IFC.** Tenías razón en que no son lo mismo: la IFPE emite fondos de pago
electrónico y la IFC intermedia financiamiento colectivo. Antes estaban agrupadas como "Fintech"
y eso ocultaba la diferencia.

**2. Se separó SOFOM E.R. de SOFOM E.N.R.**, porque el RECO y los capítulos V y VI del SIPRES
aplican **solo a las no reguladas**. Agruparlas producía un calendario incorrecto para ambas.

**3. Se corrigió el RECO — éste era el error de fondo.** Lo teníamos aplicando a banca, SOFOM,
SOFIPO/SOCAP, uniones y fintech. Conforme al art. 3 fr. V aplica **únicamente a SOFOM E.N.R.,
SOFIPO, SOFINCO, SOCAP y uniones de crédito**.

La razón está en el **artículo 6 de la LTOSF**: su primer párrafo obliga a instituciones de
crédito, SOFOM E.R. **y a las instituciones de tecnología financiera** a registrar sus comisiones
ante el **Banco de México**; el quinto párrafo traslada esa atribución a la CONDUSEF **solo**
respecto de SOFOM E.N.R., SOFIPO, SOFINCO, SOCAP y uniones de crédito. La lista de la fr. V es
exactamente el reflejo de ese quinto párrafo. Los bancos y las fintech sí registran comisiones,
pero ante Banxico.

**4. Se marcó el IFIT como pendiente de verificar.** El art. 3 fr. I no lo enumera entre los
registros aplicables a todas las Instituciones Financieras. Por ahora aplica a todos los
sectores, pero **es la asignación menos sólida del dataset**.

### REDECO para IFPE — RESUELTO por criterio CumpliFix

**Confirmado por Aurelio Castro el 30 de julio de 2026: el REDECO no se le requiere a las IFPE.
Ya está aplicado en el dataset.**

Conviene dejar asentado por qué el criterio se aparta del texto, porque es previsible que
alguien lo cuestione:

- El art. 3 **fr. III** de la Disposición enumera genéricamente a las **"Instituciones de
  Tecnología Financiera"** entre los sujetos obligados de RECA y REDECO.
- El art. 4 fr. XVI de la Ley Fintech define ese género como comprensivo de **IFC e IFPE**, sin
  distinguir.
- Leído al pie de la letra, el REDECO alcanzaría también a las IFPE.

**La Disposición está defectuosamente redactada en este punto.** Al agrupar a ambas figuras bajo
un género único, extiende a las IFPE una obligación cuya materia —la gestión de despachos de
cobranza sobre cartera crediticia— no corresponde a su operación. En los hechos la obligación no
se les requiere.

**Las IFC sí se mantienen** en el REDECO, porque su operación supone intermediación de
financiamiento y, por tanto, sí puede haber gestión de cobranza.

**Cómo quedó documentado:** el criterio está escrito en `build/gen_data.py`, en el bloque
`REDECO_SEC`, con la explicación completa. En la matriz aparece marcado como
*"fr. III · criterio CumpliFix"* para distinguirlo de las asignaciones que se sostienen en el
texto literal.

> **Nota de trazabilidad.** Éste es el único punto de la agenda donde el criterio CumpliFix se
> aparta del texto expreso de la norma. Conviene conservar el sustento —oficio, criterio de
> supervisión o precedente— que respalda que la CONDUSEF no lo requiere, por si llega a
> cuestionarse la asignación.

### Matriz completa, obligación por obligación

| Registro y artículo | Obligación | Banca | SOFOM E.N.R. | SOFOM E.R. | Seguros | SOFIPO / SOCAP | Uniones | IFPE | IFC | Casas de Bolsa | Fundamento |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IFIT · Art. 134, Fr. XIII | Programas de Educación Financiera | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | sin verificar |
| IFIT · Art. 143 | Validación de fichas técnicas de productos y s | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | sin verificar |
| RECO · Art. 115 | Registro de cartera de crédito | · | ✓ | · | · | ✓ | ✓ | · | · | · | fr. V |
| REDECO · Art. 124 | Informe de quejas por gestión de cobranza | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ | · | fr. III |
| REDECO · Art. 130 | Registro y actualización de despachos de cobra | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ | · | fr. III |
| RESBA · Art. 12, Fr. IV | Actualización de primas de seguros básicos est | · | · | · | ✓ | · | · | · | · | · | fr. IV |
| REUNE · Art. 66 | Validación de la información de la UNE | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | fr. I |
| REUNE · Art. 71 | Informe trimestral de consultas, aclaraciones  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | fr. I |
| REUS · Art. 158 | Reporte de no Consentimiento | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |  |
| REUS · Art. 160 | Aviso de publicidad dirigida | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | fr. I |
| REUS · Art. 161 | Información de la publicidad realizada | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | fr. I |
| SIPRES · Art. 50 | Validación de información corporativa y datos  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | fr. I |
| SIPRES · Art. 52 | Reporte de calidad de datos (SOFOM) | · | ✓ | · | · | · | · | · | · | · | fr. II |

*Fundamento* remite a la fracción del art. 3 de la Disposición en Materia de Registros.
"sin verificar" significa que no se localizó la fracción aplicable y la asignación es tentativa.

### Lo que sigue requiriendo validación

1. **REDECO para IFPE** — descrito arriba.
2. **IFIT** — no se localizó su fracción en el art. 3.
3. **RECA no está en la agenda.** Es un registro vigente (art. 11 LTOSF) aplicable a los mismos
   sujetos de la fr. III. No aparece porque el PPTX del que se construyó el dataset no lo
   incluye —probablemente porque no genera obligación periódica mensual, sino registro previo a
   la utilización de cada contrato de adhesión—. Conviene decidir si se suma como sección aparte.
4. **Fiduciarias de fideicomisos de crédito** — la fr. III las menciona como sujeto obligado y
   hoy no existen como sector en el sitio.

---

## 1. Hallazgo de partida: la norma no es la que se venía citando

La disposición vigente es la **DISPOSICIÓN en Materia de Registros ante la CONDUSEF**, aprobada
por acuerdo CONDUSEF/JG/2EXT2022/03 del 29 de septiembre de 2022 y publicada en el **DOF el 14 de
octubre de 2022**. Consolidó en un solo cuerpo normativo las obligaciones de registro que antes
estaban dispersas, incluidas las modificadas por el acuerdo publicado en el DOF el 11 de diciembre
de 2018.

Única reforma localizada entre 2022 y 2026: **DOF 28 de septiembre de 2023**, que reforma la
fracción I del artículo 28, el párrafo primero y el numeral 3 de la fracción V del artículo 64, la
fracción I del artículo 129, y los Anexos I, II y IV. **No altera plazos ni el catálogo de reportes.**

> **Acción:** actualizar el pie de fuente del PPTX y de todo el material comercial. Citar "las
> disposiciones de 2018" resta credibilidad frente a un área de cumplimiento informada.

---

## 2. La regla de plazos sí es general — artículo 12 (texto verificado)

> "Las Instituciones Financieras, dentro de los primeros 5 (cinco) días hábiles de cada mes,
> deberán cumplir con la obligación de presentar **la información del mes inmediato anterior** a
> través del PUR, utilizando CICI o CIC, accediendo a la sección que corresponda de acuerdo a lo
> siguiente: I. Validación de la información registrada en el SIPRES […]; II. Ingreso del reporte
> de calidad de información o del documento emitido por la Sociedad de Información Crediticia […];
> III. Validación de la información de datos registrados de la UNE, Medios de recepción o canal y
> Niveles de atención o contacto, registrados en el REUNE […]; IV. Actualización de las primas de
> tarifas de seguros básicos estandarizados, en la sección 'RESBA'; V. Registro de su Cartera
> Total, Vigente y Vencida al mes y Número de Contratos, en la sección 'RECO'; VI. Quejas por
> prácticas de Cobranza y actualización de la información de los Despachos de Cobranza a través del
> REDECO; VII. Validación de las fichas técnicas del IFIT […]; VIII. Registro y actualización de la
> información relativa a sus actividades publicitarias o mercadotécnicas, en la sección 'REUS'."

Y en los párrafos finales del mismo artículo:

> "En el caso del Informe Trimestral del REUNE, las Instituciones Financieras, **dentro de los
> primeros 10 (diez) días hábiles de los meses de enero, abril, julio y octubre**, deberán cumplir
> con la obligación de presentar la información del trimestre inmediato anterior."

Complementa el **artículo 11**: son hábiles todos los días del año con excepción de sábados,
domingos y los establecidos en el acuerdo que cada año publica la Comisión Nacional.

**Consecuencia práctica.** Las fechas del calendario no dependen de una tabla que haya que
transcribir cada año: son derivables. Reconstruimos los 12 meses de 2026 con estas reglas y las
contrastamos contra las fechas declaradas literalmente en las tablas del PPTX (enero a agosto):
**27 de 27 fechas límite coinciden, cero discrepancias.** Por eso el micrositio calcula solo los
meses de septiembre a diciembre, que el PPTX no desarrollaba.

---

## 3. Correcciones aplicadas al catálogo

### 3.1 Cinco obligaciones estaban asignadas al registro equivocado

Conforme al artículo 12, la asignación correcta es:

| Artículo | Obligación | Registro en el PPTX | Registro correcto | Base |
|---|---|---|---|---|
| Art. 66 | Validación de la información de la UNE | SIPRES | **REUNE** | Art. 12, fr. III |
| Art. 115 | Registro de cartera de crédito | SIPRES | **RECO** | Art. 12, fr. V |
| Art. 143 | Validación de fichas técnicas | RECA | **IFIT** | Art. 12, fr. VII |
| Art. 160 | Aviso de publicidad dirigida | SIPRES | **REUS** | Art. 12, fr. VIII |
| Art. 161 | Información de la publicidad realizada | SIPRES | **REUS** | Art. 12, fr. VIII |

Solo los artículos 50 y 52 corresponden efectivamente a SIPRES.

**Riesgo de no corregirlo.** Una agenda que manda a validar en SIPRES lo que se valida en REUNE
lleva al usuario al módulo equivocado del PUR. Es el tipo de error que se detecta al primer intento
de uso y erosiona la confianza en todo el documento.

### 3.2 Faltaba una obligación: RESBA

El artículo 12, fracción IV, obliga a la actualización de las primas de tarifas de los seguros
básicos estandarizados en la sección RESBA. No aparecía en el catálogo. Se agregó, aplicable al
sector de seguros y fianzas.

### 3.3 El Art. 160 no reporta el mes en curso

En el PPTX, el Art. 160 reporta el mes en curso en cinco meses y el mes anterior en enero, abril y
julio. En el análisis previo se propuso homologar al "mes en curso" por coherencia conceptual
—un aviso previo—. **Ese criterio no resiste el texto verificado:** el encabezado del artículo 12
somete toda la fracción VIII (REUS-publicidad) a "la información del mes inmediato anterior".

Para sostener que el Art. 160 es un aviso previo del mes en curso haría falta una regla especial en
el propio artículo 160, que **no fue posible verificar**. Ante la duda, el micrositio aplica la
regla general del artículo 12: **mes inmediato anterior, en los doce meses**.

> **Acción prioritaria:** leer el texto literal de los artículos 160 y 161 en el PDF oficial de la
> Disposición y confirmar. Si el 160 sí contiene una regla especial, se cambia en una línea del
> generador de datos. Mientras tanto, el criterio conservador es el que está aplicado.

### 3.4 Las sanciones no son montos fijos

El PPTX presenta 200, 250 y 500 UMAs como si fueran la multa. **La ley establece rangos:**

- **LPDUSF, artículo 94** — rangos según la fracción aplicable (200 a 1,000; 250 a 2,000;
  500 a 2,000; y otros). En caso de reincidencia la sanción puede duplicarse.
- **LTOSF, artículo 41** — de 200 a 2,000 UMAs a las entidades que infrinjan las disposiciones de
  carácter general que la Comisión expida. **Éste, y no el art. 94, es el sancionador aplicable a
  REDECO** (artículos 124 y 130), conforme al Amparo en Revisión 323/2025 de la SCJN, que además
  sostuvo que la Disposición en materia de registros no viola el principio de seguridad jurídica.

El micrositio y el PDF ahora muestran la cifra como **"sanción mínima / desde N UMAs"**, indican el
sancionador de cada obligación y explican el rango en las notas. La métrica global se llama
**"exposición mínima"**.

Comercialmente esto es más fuerte, no más débil: "$363,661 es el piso de un mes" pega más que una
cifra que un abogado puede desarmar en treinta segundos.

### 3.5 La cifra del mockup no reconciliaba

El diseño de referencia mostraba $417,075 (3,555 UMAs) para agosto. Con el catálogo corregido, el
piso de agosto es **3,100 UMAs = $363,661.00**. Todas las cifras del sitio se calculan sumando las
obligaciones visibles en la tabla, de modo que siempre son rastreables a su origen.

### 3.6 Coincidencia que vale la pena usar

El catálogo corregido arroja **160 obligaciones al año** en el calendario general, que coincide con
el "más de 160 obligaciones anuales" que ya declara el brochure para CumpliFix 360. La cifra del
material comercial queda respaldada por el cálculo.

---

## 4. Pendientes de validación documental

| # | Pendiente | Por qué importa |
|---|---|---|
| 1 | **Texto literal de los artículos 66, 71, 115, 130, 134 fr. XIII, 143, 158, 160 y 161.** Los mirrors públicos accesibles se truncan alrededor del artículo 57. | Confirma la asignación de registro, el periodo reportado y las reglas especiales. Con el PDF oficial completo se cierra en una sesión. |
| 2 | **Acuerdo anual de días inhábiles 2026 de la CONDUSEF.** | Los días inhábiles se tomaron del marcado cromático del PPTX. Si uno está mal, todas las ventanas de ese mes se desplazan. |
| 3 | **Valor de la UMA 2026 ($117.31) contra la publicación del INEGI en el DOF.** | Está parametrizado en un solo punto del código; corregirlo es inmediato. |
| 4 | **Fracción concreta del art. 94 LPDUSF que corresponde a cada obligación.** | Hoy se cita el artículo, no la fracción. Precisarlo eleva el nivel técnico del documento. |
| 5 | **Asignación de obligaciones por sector.** | Es criterio CumpliFix, no texto normativo. Debe revisarse contra el objeto social, la autorización y los productos de cada tipo de entidad. Especialmente: quién reporta RECO, quién reporta REDECO y el alcance del Art. 52 (redactado para SOFOM). |
| 6 | **Ubicación normativa del Art. 134 fr. XIII (educación financiera).** | Es la única obligación cuyo registro no pudo confirmarse ni por texto ni por el art. 12. Marcada con indicador "?" en el sitio. |
| 7 | **Aviso de privacidad.** | Requiere domicilio fiscal completo, plazos de respuesta ARCO y encargados. Los campos `[COMPLETAR]` están señalados en la página. |
| 8 | **Denominación comercial del servicio de 5 años.** | El brochure dice "Checkup CumpliFix"; en la conversación se mencionó "CumpliCheck". El sitio usa la del brochure. Conviene unificar. |

---

## 5. Desalineación menor en el PPTX

En la diapositiva 1, la rejilla de enero corresponde a **enero de 2026** (el día 1 cae en jueves,
correcto para 2026), pero al estar colocada al final del recorrido visual —después de diciembre—
se lee como si fuera enero de 2027. Conviene moverla al inicio o rotularla explícitamente.

---

## 6. Próximos pasos

| # | Acción | Responsable | Prioridad |
|---|---|---|---|
| 1 | Leer el PDF oficial completo de la Disposición y cerrar los pendientes 1 y 6 | Aurelio / equipo técnico | Alta |
| 2 | Contrastar los días inhábiles contra el acuerdo de la CONDUSEF | Equipo | Alta |
| 3 | Completar el aviso de privacidad y borrar el recuadro de revisión interna | Aurelio | Alta — bloquea la publicación |
| 4 | Configurar el endpoint de formularios y probar un envío real | Equipo técnico | Alta — bloquea la captación |
| 5 | Corregir el PPTX: fuente normativa, asignación de registros y RESBA | Equipo | Media |
| 6 | Revisar la asignación por sector con criterio de la firma | Aurelio | Media |
| 7 | Confirmar la UMA 2026 contra el DOF | Equipo | Media |
| 8 | Unificar la denominación Checkup CumpliFix / CumpliCheck | Aurelio | Baja |
| 9 | Precisar la fracción sancionadora por obligación | Equipo | Baja — mejora técnica |

---

## Corrección del criterio de "mes activo" — 9 de septiembre de 2026

**Cómo se detectó.** El 9 de septiembre el micrositio mostraba el panorama de
**octubre** y el contador principal marcaba **22 días**, cuando el reporte quincenal
del REUS de septiembre vencía el **día 17, a 8 días**. La línea de tiempo, que sí
lo listaba, contradecía al contador.

**Causa.** El mes activo se determinaba únicamente por el cierre de la ventana de
validación (`HOY <= validacion.fin`). Cerrada esa ventana el día 7, el sitio daba el
mes por terminado y avanzaba al siguiente.

**Por qué importa.** Es un error en la dirección más peligrosa para una herramienta
preventiva: **subestima la urgencia**. La ventana de validación de los primeros días
del mes no agota las obligaciones del periodo. El reporte quincenal del REUS (art. 158)
y el informe trimestral del REUNE (art. 71) corren por su propio plazo y se sancionan
de forma independiente.

**Criterio adoptado.** El mes activo es el primero que conserva **alguna fecha límite
por delante**, considerando ventana de validación, quincenales del REUS, informe del
REUNE y el cierre de cada obligación del catálogo. Se incorporó un cuarto estado al
semáforo —*ventana cerrada con pendientes*— que antes no existía: el sitio sólo
contemplaba antes, durante y después de la ventana.

**Alcance de la corrección.** La misma lógica alimenta el panorama del mes, el radar
de sistemas, la tabla de obligaciones, el acento de temporada y el contador. Los cuatro
mostraban octubre estando en septiembre.

**Verificación.** Se simularon 20 fechas a lo largo de 2026 —dentro de la ventana, en
el tramo entre el cierre y el quincenal, en días inhábiles y en el periodo inhábil de
diciembre— comprobando que el contador nunca declare más días de los que faltan para
el siguiente vencimiento real. Sin excepciones.

### Colisión de color en el calendario

En los **12 meses** el REUS quincenal cae en el primer día de la ventana de validación,
y en enero, abril, julio y octubre el informe del REUNE abarca la ventana completa.
Como cada día pintaba un solo color, la ventana aparentaba empezar un día tarde y la
banda del REUNE aparentaba empezar el día 8. El calendario contradecía su propio pie
de página. Ahora el fondo lleva la banda dominante y los hitos que coinciden se marcan
con un punto. Corregido también en el PDF descargable, que arrastraba el mismo defecto.

---

## Validación contra fuente primaria — 14 de septiembre de 2026

### 1. Días inhábiles 2026 — VALIDADO, sin discrepancias

Se contrastó el calendario de la agenda contra el **Acuerdo publicado en el DOF el 23 de
diciembre de 2025**, por el que la CONDUSEF da a conocer los días de 2026 en que cerrará sus
puertas y suspenderá operaciones.

| Acuerdo | En la agenda |
|---|---|
| 1 y 2 de enero | Sí |
| 2 de febrero (conmemoración del 5) | Sí |
| 16 de marzo (conmemoración del 21) | Sí |
| 2 y 3 de abril | Sí |
| 1 y 5 de mayo | Sí |
| Del 20 al 31 de julio | Sí |
| 16 de septiembre | Sí |
| 2 y 16 de noviembre | Sí |
| Del 17 al 31 de diciembre | Sí |

**Coincidencia íntegra.** Las seis fechas que a primera vista faltaban del listado —25 y 26 de
julio, 19, 20, 26 y 27 de diciembre— son sábados y domingos, que el sitio ya trata como
inhábiles por regla separada. Se retiró en consecuencia la advertencia de "pendiente de
validación" del micrositio y del PDF, sustituida por la cita de la fuente.

### 2. Artículo 158 — texto literal obtenido

> *"Artículo 158.- Las Instituciones Financieras deberán informar a la CONDUSEF, el nombre
> completo, CURP cuando hayan obtenido dicho dato, teléfonos y Correos Electrónicos de los
> clientes que no hayan aceptado, que su información sea utilizada para Fines mercadotécnicos
> o publicitarios, con el fin de mantener actualizado el REUS"*, conforme a la tabla:
> inscripciones **entre el día 1 y 15** se informan **el día 16 del mes que se reporta**, y las
> inscripciones **entre el día 16 y último** se informan **el día 1 del mes siguiente**, en ambos
> casos *"en caso de que sea hábil, o al día hábil siguiente"*.

Se verificaron las 24 fechas del año contra esta regla: **las 24 coinciden**. La bandera pasó de
*asignación razonada* a *texto verificado*.

### 3. Artículo 160 vs. 161 — criterio corregido

El contraste entre ambos artículos es textual y resuelve la duda que estaba abierta:

| | Texto literal | Periodo que se reporta |
|---|---|---|
| **Art. 160** | *"informar o en su caso validar mensualmente… dentro de los primeros 5 días hábiles **del mes que corresponda**"* | **Mes en curso** |
| **Art. 161** | *"informar de manera mensual… dentro de los primeros 5 días hábiles **del mes siguiente al que se reporta**"* | **Mes anterior** |

Tiene lógica: el 160 es una declaración vigente —cómo haces publicidad, con qué medios de
contacto, con qué base de números telefónicos—, mientras que el 161 reporta actividades ya
realizadas. **Se corrigió el art. 160 en las 12 filas del año**, que venía marcado como mes
anterior.

### 4. Programas de Educación Financiera — fundamento re-citado

El **artículo 134** dice *"El Buró contendrá lo siguiente"*: es una norma descriptiva del
contenido del Buró, no una obligación de la institución. La obligación nace en otro lado:

- **Art. 136 fr. IX** — la ficha técnica debe contener *"Nombre, descripción, alcances y
  dirección electrónica específica de sus programas de educación financiera"*.
- **Art. 143** — la institución *"deberá validar en cada Período de Cumplimiento… que la
  información que se encuentra en la plataforma del IFIT está vigente y actualizada"*.

Por decisión de la firma se conserva la fila —el PUR la pide por separado— pero con el
fundamento corregido a **Art. 136 fr. IX · 143**. Los totales del año no cambian.

### Resultado

**Cero obligaciones quedan marcadas como asignación razonada.** De las trece, siete se sostienen
en texto literal verificado y seis en el artículo 12. El único pendiente documental que subsiste
es la fracción sancionadora concreta aplicable a cada obligación.
