# No Frontend Build Tools (Pure Tailwind CDN + Vanilla JS)

## Purpose
Specifies asset management and frontend architecture rules for **The Admirable**. The application is built with server-side rendered (SSR) Jinja2 templates using Tailwind CSS via CDN and Vanilla JavaScript.

## Rules
1. **NO Node.js / NPM / Vite build step:** Do not introduce `package.json`, `vite.config.js`, `tailwind.config.js`, `postcss.config.js`, or `node_modules`.
2. **Tailwind CSS:** Loaded exclusively via CDN script tag: `<script src="https://cdn.tailwindcss.com"></script>`.
3. **Tailwind Theme Customization:** Theme customizations (such as Apple design tokens, colors, custom fonts) are declared inline within layout templates via `<script> tailwind.config = { ... } </script>`.
4. **JavaScript:** Use native Vanilla JavaScript (ES6+) directly embedded in Jinja2 templates or partials. External libraries (e.g. SortableJS) must be loaded via CDN.
5. **Runtime Server:** The web server runs with Uvicorn (`uv run uvicorn admirable.presentation.web.main:app`).
