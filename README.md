# agenda.cumplifix.com — Control Center regulatorio CONDUSEF

Micrositio público que muestra el estado del cumplimiento CONDUSEF del día, el semáforo anual
de la institución, la agenda personalizada por sector financiero, y que canaliza hacia los
servicios de CumpliFix.

> **CumpliFix | Cumple tus metas, nosotros tu cumplimiento**

---

## 1. Qué hace

| Módulo | Qué resuelve |
|---|---|
| **Estado del día** | Semáforo (preparación / validación abierta / cierre inminente / día inhábil), cuenta regresiva en días-horas-minutos y próxima acción concreta. Se calcula en zona `America/Mexico_City`, no con la hora del visitante. |
| **Calendario mensual** | Días inhábiles, periodo de validación, REUS quincenal y REUNE trimestral, con navegación por los 12 meses. |
| **Línea de tiempo** | Los siguientes 6 hitos del año con el conteo de días. |
| **Radar de sistemas** | REUNE, REDECO, REUS, SIPRES, RECO, IFIT y RESBA con su estado en el periodo en curso. |
| **Tabla de obligaciones** | Fundamento, periodicidad, periodo reportado, fecha límite, sanción mínima y sancionador aplicable. Con casillas de avance que persisten en el navegador. |
| **Semáforo anual** | De enero a hoy: cuántas ventanas ya cerraron, cuántas quedaron sin marcar y la exposición acumulada. Es el gancho natural hacia el Checkup de 5 años. |
| **Vista por sector** | SOFOM, Banca Múltiple, Seguros y Fianzas, SOFIPO/SOCAP, Uniones de Crédito, IFPE/IFC y Casas de Bolsa. Requiere registro; el registro llega como lead. |
| **Utilidades** | Exportar el año completo a `.ics`, descargar la lista de verificación del mes en CSV, compartir el estado por WhatsApp e imprimir para el expediente. |
| **Conversión** | 9 bloques de "¿te suena?" ligados a servicios reales, 12 tarjetas de servicio, quiénes somos, brochure y formulario de contacto. |

---

## 2. Contenido del repositorio

```
/
├── index.html                     El micrositio completo (autocontenido)
├── aviso-de-privacidad.html       Aviso de privacidad integral
├── CNAME                          agenda.cumplifix.com
├── .nojekyll                      Evita el procesamiento Jekyll de GitHub Pages
├── robots.txt · sitemap.xml       SEO
├── assets/
│   ├── agenda-cumplifix-condusef-2026.pdf   Agenda en PDF (15 páginas, generada del mismo dataset)
│   ├── brochure-cumplifix.pdf               Brochure institucional
│   ├── logo-cumplifix.png · favicon.png
├── build/
│   ├── gen_data.py                Genera el dataset desde las reglas normativas
│   ├── agenda-2026.json           Dataset del año
│   ├── gen_pdf.py                 Genera el PDF de la agenda
│   ├── verificar.py               Contrasta el dataset contra el PPTX fuente
│   ├── plantilla.html · aviso.html   Plantillas con marcadores
│   └── build.py                   Ensambla todo y escribe la raíz
├── README.md · PUBLICAR.md      Referencia completa y guía corta de publicación
└── OBSERVACIONES.md               Hallazgos normativos que requieren tu validación
```

---

> **¿Vas a publicar ya?** `PUBLICAR.md` trae la versión corta: subir, activar Pages, apuntar
> el dominio y avisar al equipo. Esta sección es la referencia completa.

## 3. Publicar en GitHub Pages

1. **Crear el repositorio.** En github.com/new, nómbralo por ejemplo `agenda-cumplifix`.
   Puede ser público (recomendado para Pages gratis) o privado si tu plan lo permite.

2. **Subir los archivos.** Desde la terminal, dentro de esta carpeta:

   ```bash
   git init
   git add .
   git commit -m "Agenda regulatoria CONDUSEF 2026"
   git branch -M main
   git remote add origin https://github.com/USUARIO/agenda-cumplifix.git
   git push -u origin main
   ```

   O bien arrastra los archivos en **Add file → Upload files** desde la web de GitHub.

3. **Activar Pages.** En el repositorio: **Settings → Pages → Build and deployment**.
   En *Source* elige **Deploy from a branch**, rama `main`, carpeta `/ (root)`. Guarda.

4. **Apuntar el dominio.** En el panel DNS de `cumplifix.com` crea un registro:

   | Tipo | Nombre | Valor |
   |---|---|---|
   | CNAME | `agenda` | `USUARIO.github.io` |

   El archivo `CNAME` de este repositorio ya declara `agenda.cumplifix.com`, así que Pages lo
   toma automáticamente. Una vez propagado (de minutos a un par de horas), activa
   **Enforce HTTPS** en Settings → Pages.

5. **Verificar.** Abre `https://agenda.cumplifix.com` y comprueba que el estado del día
   corresponde a la fecha real y que el PDF descarga.

---

## 4. Configuración antes de publicar

Abre `index.html` y busca el bloque `const CONFIG = {`:

```js
const CONFIG = {
  pdf: "assets/agenda-cumplifix-condusef-2026.pdf",
  brochure: "assets/brochure-cumplifix.pdf",
  efemerides: "https://docs.google.com/forms/d/e/1FAIpQLSc.../viewform",
  formEndpoint: "",   // ← configurar
  formKey: "",        // ← configurar
  correo: "info@cumplifix.com",
  whatsapp: "525571462367",
  sitio: "https://agenda.cumplifix.com"
};
```

### Formularios — esto es lo único que falta para que "sí mande correos"

Hoy, con `formEndpoint` vacío, los formularios **abren el cliente de correo del visitante** con
el mensaje prellenado hacia `info@cumplifix.com`. Funciona, pero depende de que la persona
tenga configurado un cliente de correo y pierdes trazabilidad de los leads.

Para que los envíos lleguen solos a tu buzón, el camino más simple —y gratuito hasta cierto
volumen— es **Web3Forms**:

1. Entra a `web3forms.com`, escribe `info@cumplifix.com` y te llega una *access key* por correo.
2. En `index.html` pon:
   ```js
   formEndpoint: "https://api.web3forms.com/submit",
   formKey:      "TU-ACCESS-KEY",
   ```
3. Listo. Cada envío del formulario de contacto y de cada registro sectorial llega a tu correo
   con el asunto `[agenda.cumplifix.com] …`.

Formspree funciona igual: pega la URL del formulario en `formEndpoint` y deja `formKey` vacío.

> **Importante para la trazabilidad:** el registro sectorial es tu principal fuente de leads
> calificados. Mientras `formEndpoint` esté vacío, los datos de quien se registra **no se guardan
> en ningún lado** —solo se abre su cliente de correo—. Configúralo antes de difundir el sitio.

### Modo revisión

`index.html` incluye `modoRevision: true` en el bloque `CONFIG`. Mientras esté activo:

- Se muestra una barra amarilla **"Versión en revisión interna"** arriba de todo.
- Se inyecta `<meta name="robots" content="noindex,nofollow">`, así que el sitio no aparece
  en buscadores mientras tu equipo lo revisa.

Cuando esté aprobado, cámbialo a `false`.

### Otros ajustes

- **PDF de la agenda.** Ya viene generado. Si lo sustituyes, conserva el nombre del archivo.
- **Efemérides.** Apunta al Google Form actual. Cambia la URL en `CONFIG.efemerides` si migras.
- **Enlaces de servicios.** Los botones de servicio llevan al formulario de contacto con el tema
  preseleccionado. Si más adelante creas páginas por servicio, sustituye el `href="#contacto"`.

---

## 5. Mantenimiento

**Mensual: ninguno.** El estado, el contador, el calendario, la tabla y el semáforo anual se
calculan solos con la fecha del día.

**Anual (para 2027):**

1. En `build/gen_data.py` cambia `ANIO = 2027`, actualiza la lista `INHABILES` con el acuerdo de
   días inhábiles que publique la CONDUSEF, y el valor de la UMA.
2. Ejecuta:
   ```bash
   cd build
   python3 gen_data.py     # regenera agenda-2026.json
   python3 gen_pdf.py      # regenera el PDF
   python3 build.py        # reensambla index.html y aviso-de-privacidad.html
   ```
3. Haz commit y push. GitHub Pages publica en menos de un minuto.

Requisitos: Python 3 y `playwright` (`pip install playwright`) para el PDF.

---

## 6. Antes de difundir — lista de verificación

- [ ] Poner `modoRevision: false` en el bloque `CONFIG` de `index.html`
- [ ] Completar los campos `[COMPLETAR]` del aviso de privacidad y borrar el recuadro amarillo de revisión interna
- [ ] Configurar `formEndpoint` y `formKey`, y probar un envío real de cada formulario
- [ ] Validar los hallazgos normativos de `OBSERVACIONES.md`
- [ ] Contrastar los días inhábiles contra el acuerdo publicado por la CONDUSEF
- [ ] Confirmar el valor de la UMA 2026 contra la publicación del INEGI en el DOF
- [ ] Revisar la asignación de obligaciones por sector con el criterio de la firma
- [ ] Verificar que el enlace de la Academia y el del Google Form apunten a donde deben
- [ ] Probar en celular: es donde va a llegar la mayoría del tráfico de WhatsApp y LinkedIn

---

## 7. Notas técnicas

- **Sin dependencias.** No usa frameworks, CDNs ni build tools. `index.html` es un solo archivo
  con el dataset, el logo y toda la lógica embebidos. Funciona incluso abierto desde el disco.
- **Almacenamiento local.** El sector elegido y las casillas marcadas se guardan en
  `localStorage` con un envoltorio tolerante a fallos: si el navegador lo bloquea (modo
  privado, políticas corporativas), el sitio sigue funcionando en memoria sin errores.
- **Accesibilidad.** La paleta de colores del calendario y de los estados fue validada para
  daltonismo (deuteranopía, protanopía y tritanopía) y contraste contra el fondo. Ningún estado
  se comunica solo con color: todos llevan icono y etiqueta de texto.
- **Impresión.** La hoja de estilos oculta navegación, CTAs y formularios al imprimir, dejando
  solo el calendario, la tabla y el semáforo, para que sirva como evidencia de control interno.
