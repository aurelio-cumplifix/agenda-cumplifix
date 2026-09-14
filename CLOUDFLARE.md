# Activar la medición sin cookies

Cinco minutos. Al terminar sabrás cuánta gente entra a la agenda, de dónde llega y qué
secciones mira. Sin cookies, sin banner de consentimiento y sin datos personales.

## 1. Crear la cuenta

1. Entra a **dash.cloudflare.com/sign-up** y regístrate con `aurelio@cumplifix.com`.
2. En el menú lateral, **Analytics & Logs → Web Analytics**.
3. **Add a site** y escribe `agenda.cumplifix.com`.

No necesitas mover el DNS ni pasar el dominio a Cloudflare. Web Analytics funciona con un
fragmento de código, que es justo lo que ya está preparado en el sitio.

## 2. Copiar el token

Cloudflare te muestra un fragmento parecido a esto:

```html
<script defer src='https://static.cloudflareinsights.com/beacon.min.js'
        data-cf-beacon='{"token": "a1b2c3d4e5f6..."}'></script>
```

**Sólo necesitas el token**, la cadena que va entre comillas después de `"token":`.

## 3. Pegarlo en el sitio

En `build/plantilla.html`, busca `analyticsToken` —está cerca del inicio, junto a
`modoRevision`— y pega el token entre las comillas:

```js
analyticsToken: "a1b2c3d4e5f6..."
```

Luego, en la carpeta `build/`, ejecuta:

```
python3 build.py
```

Commit y push, y listo. Los primeros datos aparecen en Cloudflare en unos minutos.

## Por qué está atado al aviso de privacidad

El apartado de "Consulta sin identificación" del aviso se genera a partir de ese token. Con el
token vacío, el aviso afirma que el sitio no incorpora herramientas de terceros. En cuanto
pegas el token y reconstruyes, el aviso incorpora solo el párrafo que describe la medición:
qué recaba, qué no, y por qué no requiere consentimiento previo.

Esto es deliberado. El aviso de privacidad de una firma de cumplimiento no puede afirmar algo
distinto de lo que el sitio hace. Atarlo al token elimina la posibilidad de que se
desincronicen por olvido.

## Qué recaba y qué no

| Recaba | No recaba |
|---|---|
| Página consultada y sitio de procedencia | Cookies o identificadores en el equipo |
| Tipo de navegador, dispositivo y sistema | Huella digital del navegador |
| País | Seguimiento entre sitios distintos |
| Tiempos de carga | Perfil del visitante |

Por no requerir almacenamiento de información en el equipo del visitante, esta medición no
está sujeta a consentimiento previo. Esa es la razón por la que la elegimos y no Google
Analytics, que sí usa cookies y obligaría a un banner y a declarar transferencia internacional.

---

*CumpliFix S.C. | Cumple tus metas, nosotros tu cumplimiento*
