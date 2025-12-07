# Doctor Cañamo

Proyecto para monitoreo y automatización de un cuarto de cultivo basado en tres pilares:

1. **Adquisición de datos:** lectura de métricas de Growee (pH, EC, temperatura de agua), sensores SmartLife (temperatura y humedad ambiente) y fotos almacenadas en Drive.
2. **Diagnóstico con IA:** combinación de análisis de sensores y visión para detectar carencias nutricionales, estrés hídrico o térmico, y recomendar ajustes.
3. **Automatización correctiva:** ejecutar acciones sobre SmartLife (clima) y Growee (nutrientes) de forma segura, con registro y validaciones.

Consulta `docs/architecture.md` para el plan técnico detallado, el pipeline de datos, los componentes de IA y el roadmap de implementación.

👉 Para ver qué falta para que el sistema sea operativo end-to-end, revisa `docs/gap_analysis.md`.
👉 Para inspirarte en soluciones similares y buenas prácticas, explora `docs/research_landscape.md`.

## Integración continua
- Cada push o pull request dispara un workflow de GitHub Actions que instala dependencias y ejecuta el pipeline en modo `--dry-run`, subiendo el Excel generado como artefacto (`.github/workflows/ci.yml`).
- Úsalo para comprobar rápidamente que los conectores sintéticos, las validaciones y las exportaciones siguen funcionando antes de mezclar cambios.

## Quickstart (prototipo)
1. Instala dependencias: `pip install -r requirements.txt`.
2. Ejecuta el pipeline con métricas sintéticas y genera un Excel de control (elige el comando que te resulte más cómodo):
   ```bash
   # Opción clásica usando el CLI como módulo
   PYTHONPATH=src python -m doctor_canamo.cli --dry-run --output outputs/doctor_canamo.xlsx

   # Opción lista para depurar con breakpoints en el repo (inyecta src en sys.path)
   python main.py --dry-run --output outputs/doctor_canamo.xlsx
   ```
3. Reemplaza `--dry-run` y exporta variables `GROWEE_BASE_URL`, `GROWEE_TOKEN`, `SMARTLIFE_API_URL`, `SMARTLIFE_ACCESS_TOKEN` para consumir datos reales. Puedes sincronizar fotos de Drive a una carpeta local y pasarla con `--drive-folder` para registrar referencias.

### Depuración y trazas
- Añade `--log-level DEBUG` para ver qué conector se está invocando, cuántas métricas devuelve y cuántas alertas/diagnósticos se generan:
  ```bash
  PYTHONPATH=src python -m doctor_canamo.cli --dry-run --log-level DEBUG --output outputs/doctor_canamo.xlsx
  ```
- Si prefieres un flujo de depuración listo para breakpoint sin exportar `PYTHONPATH`, ejecuta directamente `python main.py --log-level DEBUG --dry-run --output outputs/doctor_canamo.xlsx`.
- Si quieres inspeccionar las métricas sin usar APIs reales, combina `--dry-run` con `--drive-folder` apuntando a una carpeta local de imágenes para verificar que se registran en el Excel.
- El punto de entrada es `doctor_canamo/cli.py`, por lo que puedes colocar breakpoints en ese archivo o en los conectores (`ingestion/`) y ejecutar `python -m doctor_canamo.cli` desde tu IDE o PowerShell para depurar paso a paso.

### Ejecución en PowerShell (Windows)
1. Ubícate en la raíz del proyecto: `cd CANNAIA`.
2. Instala dependencias: `python -m pip install -r requirements.txt`.
3. Ejecuta el pipeline en modo sintético y genera el Excel (la variable de entorno `PYTHONPATH` se establece con `$env:`):
   ```powershell
   $env:PYTHONPATH = "src"
   python -m doctor_canamo.cli --dry-run --output outputs\doctor_canamo.xlsx
   ```
4. Para usar datos reales, define las credenciales en la misma consola antes de ejecutar:
   ```powershell
   $env:GROWEE_BASE_URL = "https://api.mygrowee.com"
   $env:GROWEE_TOKEN = "<token>"
   $env:SMARTLIFE_API_URL = "https://api.smartlife.com"
   $env:SMARTLIFE_ACCESS_TOKEN = "<token>"
   python -m doctor_canamo.cli --output outputs\doctor_canamo.xlsx
   ```

El punto de entrada es `doctor_canamo/cli.py` y se invoca con `python -m doctor_canamo.cli`, de modo que no necesitas un ejecutable adicional ni un script separado para PowerShell.

El Excel generado incluye:
- `metrics`: datos recopilados normalizados.
- `diagnoses`: alertas y recomendaciones básicas por umbral.
- `data_quality`: posibles problemas de ingesta (valores faltantes, timestamps viejos, unidades vacías).
- `actions`: acciones sugeridas para Growee/SmartLife en base a las alertas.
