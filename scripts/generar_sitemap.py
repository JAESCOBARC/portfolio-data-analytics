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
