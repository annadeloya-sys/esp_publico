# Plataforma de espacios públicos — NOM-001-SEDATU-2021 (ECOURBA)

Dashboard estático (SPA) de análisis de accesibilidad a espacios públicos por red vial:
áreas de servicio (isócronas Valhalla), cobertura por población, con ámbito **CDMX** y **Nacional (32 estados)**.

## Contenido (sitio)
- `index.html` — la aplicación (3 vistas: Resumen · Mapa · Territorio).
- `dashboard_datos.js` — indicadores CDMX (`window.DASH`).
- `mapa_datos.js` — capas del mapa CDMX (`window.ESPPUB`).
- `mapa_nacional_datos.js` — capas del mapa nacional (`window.ESPPUB_NAC`).
- `nacional_datos.js` — datos nacionales de Territorio/Resumen (`window.NAC`).
- `.nojekyll` — para que GitHub Pages sirva los `.js` tal cual.

## Publicar en GitHub Pages
1. Crear un repositorio en GitHub y subir esta carpeta (ver comandos abajo).
2. Settings → Pages → Source: **Deploy from a branch** → Branch: `main` / carpeta `/ (root)` → Save.
3. El sitio queda en `https://<usuario>.github.io/<repo>/`.

## Requisitos en tiempo de ejecución
Solo un navegador con **internet** (para las teselas del mapa base OSM/CARTO/Esri y Leaflet vía CDN).
No requiere backend, base de datos, Valhalla ni Python: el análisis ya está precalculado en los `.js`.

## Actualizar los datos
Los `.js` se regeneran con el pipeline Python del proyecto (scripts `10`–`15`, Valhalla). Tras regenerarlos,
subir de nuevo los archivos y hacer `git push`.
