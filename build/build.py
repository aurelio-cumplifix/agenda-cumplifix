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

n1 = escribir("index.html", leer("plantilla.html")
              .replace("__DATA__", datos).replace("__LOGO__", logo).replace("__FAVICON__", favicon))
n2 = escribir("aviso-de-privacidad.html", leer("aviso.html")
              .replace("__LOGO__", logo).replace("__FAVICON__", favicon).replace("__FECHA__", fecha))

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
         '<lastmod>{}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>\n'
         '  <url><loc>https://agenda.cumplifix.com/aviso-de-privacidad.html</loc>'
         '<lastmod>{}</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>\n'
         '</urlset>\n'.format(hoy.isoformat(), hoy.isoformat()))

d = json.loads(datos)
print("index.html                 {:>7,} bytes".format(n1))
print("aviso-de-privacidad.html   {:>7,} bytes".format(n2))
print("CNAME · .nojekyll · robots.txt · sitemap.xml  escritos")
print("dataset: {} meses · {} obligaciones · {} sectores · {} sistemas".format(
    len(d["meses"]), sum(len(m["obligaciones"]) for m in d["meses"]),
    len(d["sectores"]), len(d["sistemas"])))
