#!/usr/bin/env python3
"""
Extrae el grafo de enlaces internos de jhonyescobar.com a partir de los
archivos .html del repo, y lo deja como JSON listo para alimentar el
artefacto D3.js del dashboard.

Uso:
    python3 extract_links.py [--root <ruta-del-repo>] [--out <ruta-json>]

Salida (JSON):
{
  "base_url": "https://www.jhonyescobar.com/",
  "pages": [
    {"id": "index.html", "incoming": 12, "outgoing": 6, "incoming_ids": [...], "outgoing_ids": [...]},
    ...
  ],
  "edges": [["source.html", "target.html"], ...],      # únicos, con peso SEO
  "edges_all": [["source.html", "target.html"], ...],  # incluye legales, sin dedupe por página (para cifras)
  "legal_pages": [],                                   # este sitio no tiene páginas legales todavía
  "broken_targets": ["plantillas/"],  # hrefs enlazados que no resuelven a un archivo real
  "redirect_pages": []                # detectadas por <meta http-equiv="refresh"> o
                                       # window.location.replace
}

No inventa nada: solo reporta lo que efectivamente encuentra en el HTML.
Cualquier página con lógica de redirección se marca automáticamente
inspeccionando el propio archivo (meta refresh / location.replace), no por
una lista fija — así el script sigue siendo correcto si el sitio cambia.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

HREF_RE = re.compile(r'href=["\']([^"\'#]+)["\']', re.IGNORECASE)
ASSET_EXTS = {
    '.css', '.js', '.png', '.jpg', '.jpeg', '.svg', '.webp',
    '.xml', '.txt', '.ico', '.json', '.pdf', '.woff', '.woff2', '.ttf',
    '.jpg', '.JPG'
}
SKIP_SCHEMES = ('mailto:', 'tel:', 'javascript:', '#')
# Este sitio no tiene páginas legales (aviso-legal.html/politica-privacidad.html)
# todavía. Si las añades más adelante, súmalas aquí para que el grafo SEO no
# las cuente como ruido de footer en todas las páginas.
LEGAL_PAGES = set()


def find_html_files(root: Path):
    return sorted(p for p in root.rglob('*.html') if '.git' not in p.parts and 'node_modules' not in p.parts)


def normalize(base_url: str, source_path: Path, root: Path, href: str):
    href = href.strip()
    if not href or href.startswith(SKIP_SCHEMES):
        return None
    if href.startswith(('http://', 'https://')) and not href.startswith(base_url):
        return None  # external domain

    # resolve relative to the *source file's own URL* on the real domain
    rel_from_root = source_path.relative_to(root).as_posix()
    source_url = urljoin(base_url, rel_from_root)
    resolved = urljoin(source_url, href)

    parsed = urlparse(resolved)
    if parsed.netloc and parsed.netloc != urlparse(base_url).netloc:
        return None

    path = parsed.path
    base_path = urlparse(base_url).path or '/'
    if not path.startswith(base_path):
        return None
    rel = path[len(base_path):]  # site-relative path, no leading slash

    if rel == '':
        return 'index.html'

    # URLs "bonitas" (/portfolio/, /portfolio/control-piscinas/) apuntan al
    # index.html de esa carpeta — igual que lo sirve GitHub Pages.
    if rel.endswith('/'):
        candidate = rel + 'index.html'
        if (root / candidate).exists():
            return candidate
        return rel  # se reportará como broken_target si no existe

    ext = Path(rel).suffix.lower()
    if ext:
        if ext in ASSET_EXTS:
            return None
        if ext != '.html':
            # extensión desconocida -> se trata como asset, se descarta
            return None
    return rel


def detect_redirect(html: str) -> bool:
    if re.search(r'http-equiv=["\']refresh["\']', html, re.IGNORECASE):
        return True
    if 'window.location.replace(' in html:
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.', help='Raíz del repo (donde están los .html)')
    ap.add_argument('--base-url', default='https://www.jhonyescobar.com/')
    ap.add_argument('--out', default=None, help='Ruta de salida del JSON (por defecto stdout)')
    args = ap.parse_args()

    root = Path(args.root).resolve()
    base_url = args.base_url

    html_files = find_html_files(root)
    if not html_files:
        print(f'No se encontraron archivos .html bajo {root}', file=sys.stderr)
        sys.exit(1)

    all_ids = set()
    for f in html_files:
        rel = f.relative_to(root).as_posix()
        all_ids.add(rel)

    edges_all = []        # every raw (source,target) occurrence, legal pages included
    edges_seen = set()    # deduped (source,target) pairs, legal pages included
    redirect_pages = set()
    broken_targets = set()

    for f in html_files:
        source_id = f.relative_to(root).as_posix()
        html = f.read_text(encoding='utf-8', errors='ignore')

        if detect_redirect(html):
            redirect_pages.add(source_id)

        for m in HREF_RE.finditer(html):
            target = normalize(base_url, f, root, m.group(1))
            if target is None or target == source_id:
                continue
            edges_all.append((source_id, target))
            pair = (source_id, target)
            if pair not in edges_seen:
                edges_seen.add(pair)
                if target not in all_ids:
                    broken_targets.add(target)

    # every discovered id becomes a node, plus any real html file not otherwise linked
    node_ids = set(all_ids)
    for s, t in edges_seen:
        node_ids.add(s)
        node_ids.add(t)

    incoming = {nid: set() for nid in node_ids}
    outgoing = {nid: set() for nid in node_ids}
    for s, t in edges_seen:
        outgoing[s].add(t)
        incoming[t].add(s)

    # edges with SEO weight: dedupe pairs, drop legal-page targets (footer noise, present on every page)
    edges_seo = sorted({(s, t) for (s, t) in edges_seen if t not in LEGAL_PAGES})

    pages = []
    for nid in sorted(node_ids):
        pages.append({
            'id': nid,
            'incoming': len(incoming.get(nid, set())),
            'outgoing': len(outgoing.get(nid, set())),
            'incoming_ids': sorted(incoming.get(nid, set())),
            'outgoing_ids': sorted(outgoing.get(nid, set())),
            'exists': nid in all_ids,
            'is_redirect': nid in redirect_pages,
        })

    result = {
        'base_url': base_url,
        'pages': pages,
        'edges': edges_seo,
        'edges_all': sorted(set(edges_seen)),
        'legal_pages': sorted(LEGAL_PAGES & node_ids),
        'broken_targets': sorted(broken_targets),
        'redirect_pages': sorted(redirect_pages),
    }

    out_json = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(out_json, encoding='utf-8')
        print(f'Escrito {args.out} ({len(pages)} páginas, {len(edges_seo)} enlaces con peso SEO)', file=sys.stderr)
    else:
        print(out_json)


if __name__ == '__main__':
    main()
