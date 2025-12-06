# Doctor Cañamo

Proyecto para monitoreo y automatización de un cuarto de cultivo basado en tres pilares:

1. **Adquisición de datos:** lectura de métricas de Growee (pH, EC, temperatura de agua), sensores SmartLife (temperatura y humedad ambiente) y fotos almacenadas en Drive.
2. **Diagnóstico con IA:** combinación de análisis de sensores y visión para detectar carencias nutricionales, estrés hídrico o térmico, y recomendar ajustes.
3. **Automatización correctiva:** ejecutar acciones sobre SmartLife (clima) y Growee (nutrientes) de forma segura, con registro y validaciones.

Consulta `docs/architecture.md` para el plan técnico detallado, el pipeline de datos, los componentes de IA y el roadmap de implementación.

## Integración continua
- Cada push o pull request dispara un workflow de GitHub Actions que instala dependencias y ejecuta el pipeline en modo `--dry-run`, subiendo el Excel generado como artefacto (`.github/workflows/ci.yml`).
- Úsalo para comprobar rápidamente que los conectores sintéticos, las validaciones y las exportaciones siguen funcionando antes de mezclar cambios.

## Quickstart (prototipo)
1. Instala dependencias: `pip install -r requirements.txt`.
2. Ejecuta el pipeline con métricas sintéticas y genera un Excel de control:
   ```bash
   PYTHONPATH=src python -m doctor_canamo.cli --dry-run --output outputs/doctor_canamo.xlsx
   ```
3. Reemplaza `--dry-run` y exporta variables `GROWEE_BASE_URL`, `GROWEE_TOKEN`, `SMARTLIFE_API_URL`, `SMARTLIFE_ACCESS_TOKEN` para consumir datos reales. Puedes sincronizar fotos de Drive a una carpeta local y pasarla con `--drive-folder` para registrar referencias.

El Excel generado incluye:
- `metrics`: datos recopilados normalizados.
- `diagnoses`: alertas y recomendaciones básicas por umbral.
- `data_quality`: posibles problemas de ingesta (valores faltantes, timestamps viejos, unidades vacías).
- `actions`: acciones sugeridas para Growee/SmartLife en base a las alertas.
