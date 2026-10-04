#!/usr/bin/env python3
"""Genera sitemap.xml con lastmod = fecha del último commit que tocó cada página.

Uso: python3 scripts/generar_sitemap.py  (lo ejecuta también .github/workflows/sitemap.yml en cada push)
Para añadir una página indexable nueva, añádela a PAGINAS.
"""
import subprocess
from datetime import date
from pathlib import Path

DOMINIO = "https://www.jhonyescobar.com"
RAIZ = Path(__file__).resolve().parent.parent

# (archivo, url, changefreq, priority)
PAGINAS = [
    ("index.html", "/", "monthly", "1.0"),
    ("portfolio/index.html", "/portfolio/", "monthly", "0.9"),
    ("portfolio/dream-resort-hotels/index.html", "/portfolio/dream-resort-hotels/", "yearly", "0.8"),
    ("portfolio/control-piscinas/index.html", "/portfolio/control-piscinas/", "yearly", "0.8"),
    ("en/index.html", "/en/", "monthly", "0.9"),
    ("en/portfolio/index.html", "/en/portfolio/", "monthly", "0.8"),
    ("en/portfolio/dream-resort-hotels/index.html", "/en/portfolio/dream-resort-hotels/", "yearly", "0.7"),
    ("en/portfolio/control-piscinas/index.html", "/en/portfolio/control-piscinas/", "yearly", "0.7"),
    ("servicios/index.html", "/servicios/", "monthly", "0.9"),
    ("servicios/marketing-digital/index.html", "/servicios/marketing-digital/", "monthly", "0.8"),
    ("servicios/aplicaciones-y-plantillas/index.html", "/servicios/aplicaciones-y-plantillas/", "monthly", "0.8"),
    ("servicios/automatizaciones/index.html", "/servicios/automatizaciones/", "monthly", "0.8"),
    ("servicios/dashboards-y-business-intelligence/index.html", "/servicios/dashboards-y-business-intelligence/", "monthly", "0.8"),
    ("servicios/marketing-digital/creacion-paginas-web/index.html", "/servicios/marketing-digital/creacion-paginas-web/", "yearly", "0.7"),
    ("servicios/marketing-digital/campanas-shopping/index.html", "/servicios/marketing-digital/campanas-shopping/", "yearly", "0.7"),
    ("servicios/marketing-digital/optimizacion-tecnica-web/index.html", "/servicios/marketing-digital/optimizacion-tecnica-web/", "yearly", "0.7"),
    ("servicios/marketing-digital/seo-local/index.html", "/servicios/marketing-digital/seo-local/", "yearly", "0.7"),
    ("servicios/aplicaciones-y-plantillas/apps-inventario/index.html", "/servicios/aplicaciones-y-plantillas/apps-inventario/", "yearly", "0.7"),
    ("servicios/aplicaciones-y-plantillas/app-facturacion/index.html", "/servicios/aplicaciones-y-plantillas/app-facturacion/", "yearly", "0.7"),
    ("servicios/aplicaciones-y-plantillas/app-plan-negocio/index.html", "/servicios/aplicaciones-y-plantillas/app-plan-negocio/", "yearly", "0.7"),
    ("servicios/aplicaciones-y-plantillas/app-conciliador-bancario/index.html", "/servicios/aplicaciones-y-plantillas/app-conciliador-bancario/", "yearly", "0.7"),
    ("servicios/aplicaciones-y-plantillas/plantillas-excel/index.html", "/servicios/aplicaciones-y-plantillas/plantillas-excel/", "yearly", "0.7"),
    ("servicios/automatizaciones/carruseles-instagram/index.html", "/servicios/automatizaciones/carruseles-instagram/", "yearly", "0.7"),
    ("servicios/automatizaciones/chatbots-whatsapp-ia/index.html", "/servicios/automatizaciones/chatbots-whatsapp-ia/", "yearly", "0.7"),
    ("servicios/automatizaciones/automatizacion-reportes/index.html", "/servicios/automatizaciones/automatizacion-reportes/", "yearly", "0.7"),
    ("servicios/automatizaciones/vba-excel-macros/index.html", "/servicios/automatizaciones/vba-excel-macros/", "yearly", "0.7"),
    ("servicios/automatizaciones/web-scraping/index.html", "/servicios/automatizaciones/web-scraping/", "yearly", "0.7"),
    ("servicios/dashboards-y-business-intelligence/dashboard-de-negocios/index.html", "/servicios/dashboards-y-business-intelligence/dashboard-de-negocios/", "yearly", "0.7"),
    ("servicios/dashboards-y-business-intelligence/implementacion-data-driven/index.html", "/servicios/dashboards-y-business-intelligence/implementacion-data-driven/", "yearly", "0.7"),
    ("servicios/dashboards-y-business-intelligence/reporting-marketing-ads/index.html", "/servicios/dashboards-y-business-intelligence/reporting-marketing-ads/", "yearly", "0.7"),
]
# proyectos/*.html quedaron como redirecciones noindex a las URLs de arriba: no van en el sitemap.


def ultima_fecha(archivo):
    fecha = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", archivo],
        cwd=RAIZ, capture_output=True, text=True,
    ).stdout.strip()
    return fecha or date.today().isoformat()


def main():
    urls = []
    for archivo, url, freq, prio in PAGINAS:
        urls.append(
            "  <url>\n"
            f"    <loc>{DOMINIO}{url}</loc>\n"
            f"    <lastmod>{ultima_fecha(archivo)}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n"
            f"    <priority>{prio}</priority>\n"
            "  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (RAIZ / "sitemap.xml").write_text(xml, encoding="utf-8")


if __name__ == "__main__":
    main()
