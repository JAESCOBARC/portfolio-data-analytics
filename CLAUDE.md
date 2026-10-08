# jhonyescobar.com — portfolio-data-analytics

Sitio estático (HTML/CSS/JS sin build step) de Jhony Escobar, desplegado en GitHub Pages detrás de Cloudflare, dominio `www.jhonyescobar.com`. Todo el contenido es bilingüe: cada página en `/` tiene su espejo exacto bajo `/en/`.

## Regla permanente: framework de 5 capas de optimización

Todo lo que se cree o modifique en este proyecto — página nueva, sección nueva, componente, copy — pasa por este checklist antes de darse por terminado. No es opcional ni se pregunta cada vez: se aplica por defecto, igual que el resto de convenciones de este archivo. Basado en "Las Capas del SEO: del rastreo a los resultados" (SEO → AEO → GEO/AIO → SXO).

### 1. SEO — Ser rastreado → indexado → posicionado
- `<title>` único y descriptivo, meta description ≤160 caracteres, canonical, hreflang (es/en/x-default) en toda página nueva.
- La página se da de alta en `scripts/generar_sitemap.py` (lista `PAGINAS`) y queda enlazada desde al menos un punto del sitio — nunca una página huérfana. Verificar con `.claude/skills/enlaces/scripts/extract_links.py` (`broken_targets` debe salir `[]`).
- Jerarquía de encabezados correcta: un único `<h1>`, `<h2>`/`<h3>` en orden lógico (no `<span>` disfrazando un título real).
- Enlazado interno con anchor text descriptivo, no genérico.

### 2. AEO — Ser la respuesta directa
- Cuando la página responde preguntas frecuentes reales de un usuario, usar bloques de pregunta/respuesta directos y autocontenidos (1–3 frases), con `FAQPage`/`Question`/`Answer` en JSON-LD — nunca inventar preguntas o respuestas que no se sostienen con contenido real del sitio.
- Datos clave en listas, tablas o bullets en vez de párrafos largos que diluyan el dato.
- Antes de añadir un nuevo bloque de FAQ, comprobar que no quede huérfano de los ya existentes en `index.html`, `en/index.html`, `servicios/dashboards-y-business-intelligence/` — mismo tono, mismo nivel de concreción.

### 3. GEO + AIO (fusionadas) — Ser citado y comprendido por IA
En un sitio de este tamaño ambas capas se reducen a lo mismo en la práctica: contenido estructurado, verificable y con una identidad de entidad coherente. Tratarlas como un único checklist, no como trabajo duplicado:
- **Coherencia de entidad, sin excepción**: el JSON-LD `Person` de Jhony Escobar debe usar el mismo `jobTitle` en todas las páginas que lo declaren (home, portfolio, ES y EN). Si una página necesita matizar un ángulo distinto (ej. "especialista en BI" vs "consultor de automatización"), eso va en `description`/`knowsAbout`, nunca en un `jobTitle` distinto. Antes de tocar cualquier JSON-LD de Person, grepear `"jobTitle"` en todo el repo y confirmar que sigue siendo uno solo.
- Toda cifra, fecha o credencial en el contenido o en JSON-LD debe ser real y ya establecida — si no se conoce un dato exacto (ej. un año de graduación), se omite, nunca se inventa.
- Datos estructurados del tipo que corresponda (`Service`, `CreativeWork`, `BreadcrumbList`, `ItemList`, `Person`) usando solo datos verificables.
- Contenido fresco: cuando se actualiza una página con cambios sustantivos, su `lastmod` en el sitemap se actualiza solo vía el workflow de GitHub Actions — no hace falta tocarlo a mano.
- Alt text descriptivo en imágenes de contenido real (no decorativas); las decorativas (iconos SVG puramente visuales) llevan `alt=""` a propósito, no por omisión.

### 4. SXO — Convertir visitas en clientes
- Cada página tiene un objetivo de conversión único y claro, sin CTAs contradictorios.
- El evento de conversión por WhatsApp ya está centralizado en `componentes/tracking.js` (dataLayer `contact_click` / `contact_method: whatsapp`) y cableado a GTM-N9XLDFCS — cualquier nuevo punto de contacto (nuevo botón, nuevo canal) debe reusar ese mismo mecanismo, no inventar uno nuevo.
- Mobile-first real: toda página nueva se verifica con Playwright a 375px y 1920px (overflow 0) antes de darse por terminada, igual que se ha hecho en el resto del sitio.
- Velocidad: imágenes con `width`/`height` explícitos y `loading="lazy"` fuera del viewport inicial; fuentes de Google cargadas con el patrón `media="print" onload="this.media='all'"` ya usado en el resto del sitio.

## Convenciones ya establecidas (no reinventar)

- **Bilingüe sistemático**: todo lo que se construye en `/` se construye también en `/en/`, en el mismo turno, sin que haga falta pedirlo.
- **Componentes compartidos**: `estilos/base.css` es la única fuente de los estilos reutilizables (`.portfolio-grid`/`.proyecto-card`, `.lang-switch`, botones, etc.) — nunca duplicar CSS de un componente ya existente en el `<style>` de una página suelta.
- **`componentes/tracking.js`**: único script de tracking del sitio (GTM + eventos de contacto), cargado con `defer` en el `<head>` de cada página; el `<noscript>` de GTM va justo después de `<body>`.
- **QA antes de commitear**: Playwright (overflow en 375/1280/1920px, conteo de `<h1>`, JSON-LD parseable) + `extract_links.py` (`broken_targets: []`) en cada cambio no trivial.
- **No fabricar datos**: estadísticas, fechas, credenciales — todo tiene que ser real y ya confirmado por el usuario; omitir en vez de inventar.
