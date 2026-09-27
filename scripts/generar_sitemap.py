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
    ("proyectos/dream-resort-hotels.html", "/proyectos/dream-resort-hotels.html", "yearly", "0.8"),
    ("proyectos/control-piscinas.html", "/proyectos/control-piscinas.html", "yearly", "0.8"),
]


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
