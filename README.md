# Kronautomation Platform

Plataforma central de Kronautomation. Hub público + dashboards de cliente con login por subdominio.

🌐 **Producción**: https://kronautomation.co

## Estructura

```
kronautomation-platform/
├── hub/                  # Sitio público en kronautomation.co
│   ├── index.html        # Landing con cards de proyectos
│   └── assets/
└── shared/               # Componentes reusables para los dashboards
    ├── auth.js           # Cliente Supabase + gating de sesión
    ├── login.html        # Pantalla de login (template)
    └── login.css         # Estilos del login
```

## Subdominios

| URL | Proyecto | Repo origen |
|---|---|---|
| `kronautomation.co` | Hub público | este repo (`hub/`) |
| `bareno.kronautomation.co` | Dr. John Bareño | `dr-bareno-dashboard` |
| `marfil.kronautomation.co` | Marfil | `reporte-marfil` |
| `research.kronautomation.co` | Research Lab | `RESEARCH` |
| `seo.kronautomation.co` | SEO Toolkit | `seo-system` |

## Stack

- **Hosting**: Cloudflare Pages (auto-deploy on push)
- **Dominio + DNS**: Cloudflare Registrar
- **Auth**: Supabase (email + password, sesión JWT)
- **Frontend**: HTML/CSS/JS vanilla, sin framework

## Agregar un nuevo proyecto

1. Copiar `shared/auth.js` y `shared/login.html` al folder del dashboard
2. Setear `PROJECT_ID` único en `auth.js`
3. Agregar 3 líneas al `<head>` del `index.html`:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
   <script src="auth.js"></script>
   <script>requireAuth('mi-proyecto');</script>
   ```
4. Cloudflare Pages → New project → conectar repo, branch `gh-pages`
5. Cloudflare DNS → CNAME `mi-proyecto` → Pages project
6. Supabase → crear usuario con `project='mi-proyecto'`

## Costos

| Item | Anual |
|---|---|
| Dominio `.co` (Cloudflare) | ~$12 USD |
| Cloudflare Pages | $0 |
| Supabase (free tier) | $0 |
| **Total** | **~$12 USD** |
