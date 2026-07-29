# Publicar con GitHub Desktop

Ya dejé la carpeta lista en tu Mac:

```
MARCO LEGAL CONDUSEF / agenda-cumplifix /
```

---

## Antes que nada: sácala de OneDrive

**No crees el repositorio dentro de OneDrive.** OneDrive sincroniza también la carpeta oculta
`.git` y eso corrompe repositorios con frecuencia — archivos bloqueados a media escritura,
conflictos de sincronización, historial roto. Es de los problemas más comunes y más molestos
de diagnosticar.

En Finder, **copia** la carpeta `agenda-cumplifix` a:

```
Documentos / GitHub / agenda-cumplifix
```

(o donde GitHub Desktop guarde tus repositorios; ahí está `CumpliFix_REUNE`). Deja la copia
original en OneDrive como respaldo, no pasa nada.

---

## Paso 1 · Crear el repositorio (2 min)

En GitHub Desktop:

1. **File → Add Local Repository…**
2. Elige la carpeta `Documentos/GitHub/agenda-cumplifix`
3. Te dirá que no es un repositorio de git y ofrecerá **"create a repository"** — dale clic
4. Nombre: `agenda-cumplifix` · deja el resto como está · **Create Repository**

Verás los 31 archivos en la pestaña *Changes*.

## Paso 2 · Commit y publicar (2 min)

1. Abajo a la izquierda, en *Summary*, escribe: `Agenda regulatoria CONDUSEF 2026`
2. **Commit to main**
3. Arriba aparece **Publish repository** — dale clic
4. **Importante:** desmarca la casilla **"Keep this code private"**

   GitHub Pages con dominio propio solo es gratis en repositorios públicos. Si lo dejas
   privado, no podrás publicarlo en `agenda.cumplifix.com` sin plan de pago.
5. **Publish Repository**

## Paso 3 · Activar GitHub Pages (2 min)

En GitHub Desktop: **Repository → View on GitHub** (o ⌘⇧G). Ya en el navegador:

**Settings → Pages**

- *Source*: **Deploy from a branch**
- *Branch*: `main` · carpeta `/ (root)` → **Save**

En un minuto tendrás `https://TU-USUARIO.github.io/agenda-cumplifix/`. Ábrela y confirma que
carga bien.

## Paso 4 · Apuntar el dominio (5 min + propagación)

En el panel DNS de `cumplifix.com`, agrega:

| Tipo | Nombre / Host | Valor |
|---|---|---|
| CNAME | `agenda` | `TU-USUARIO.github.io` |

El archivo `CNAME` del repositorio ya declara `agenda.cumplifix.com`, así que GitHub lo detecta
solo. Cuando propague (minutos a un par de horas), vuelve a **Settings → Pages** y marca
**Enforce HTTPS**.

## Paso 5 · Avisar al equipo

Manda la liga. Verán arriba la barra amarilla **"Versión en revisión interna"**, y el sitio no
se indexa en buscadores mientras esté activa.

---

## Para hacer cambios después

Editas el archivo en tu Mac con cualquier editor, GitHub Desktop detecta el cambio solo, pones
un *Summary*, **Commit to main** y **Push origin**. Pages republica en menos de un minuto.

Para sustituir el PDF de la agenda: reemplaza el archivo en `assets/` **con el mismo nombre**
(`agenda-cumplifix-condusef-2026.pdf`) y el botón sigue funcionando.

---

## Cuando el equipo dé el visto bueno

### 1. Quitar el modo revisión

En `index.html`, busca `modoRevision: true` y ponlo en `false`. Se va la barra amarilla y se
habilita la indexación en buscadores.

### 2. Conectar los formularios

Mientras `formEndpoint` esté vacío, los formularios abren el cliente de correo del visitante.
**Los registros sectoriales no se guardan en ningún lado** — y ésa es tu fuente de leads.

1. Entra a **web3forms.com**, escribe `info@cumplifix.com` y te llega una *access key*.
2. En `index.html`:
   ```js
   formEndpoint: "https://api.web3forms.com/submit",
   formKey:      "TU-ACCESS-KEY",
   ```
3. Prueba un envío real del formulario de contacto y otro del registro sectorial.

### 3. Cerrar el aviso de privacidad

En `aviso-de-privacidad.html`:

- Completa los campos `[COMPLETAR]`: domicilio fiscal, plazos de respuesta ARCO y proveedores.
- Borra el bloque `<div class="box warn" id="pendiente">…</div>` (el recuadro amarillo).

---

## Lo que conviene decidir con el equipo

| Tema | Pregunta concreta |
|---|---|
| Obligaciones por registro | ¿Coincide la asignación de cada artículo a REUNE, REDECO, REUS, SIPRES, RECO, IFIT y RESBA? |
| Art. 160 | ¿El aviso de publicidad dirigida reporta el mes anterior (criterio aplicado) o el mes en curso? |
| Obligaciones por sector | ¿Qué le toca a cada tipo de institución? Sobre todo RECO, REDECO y el Art. 52. |
| Días inhábiles | ¿Coinciden con el acuerdo publicado por la CONDUSEF? |
| Sanciones | ¿Presentamos el piso del rango, como está, o cambiamos el criterio? |
| Tono comercial | ¿Los nueve bloques de "¿te suena?" dicen lo que queremos decir? |
| Nombre del servicio | ¿Checkup CumpliFix o CumpliCheck? |

El fundamento y el riesgo de cada punto están en `OBSERVACIONES.md`.

---

## Notas

- **`.nojekyll`** es un archivo oculto pero ya está en la carpeta. GitHub Desktop lo sube sin
  problema (a diferencia de arrastrarlo en la web, donde suele perderse). Sin él, Pages ignora
  carpetas que empiezan con guion bajo.
- **`vista-escritorio.png` y `vista-movil.png`** son capturas de referencia. Si no quieres que
  se publiquen, bórralas antes del commit; no afectan al sitio.
- **La carpeta `build/`** contiene los generadores del dataset y del PDF. Súbela: es lo que te
  permite regenerar todo para 2027 cambiando dos valores.
