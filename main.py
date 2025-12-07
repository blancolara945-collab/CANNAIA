"""
Punto de entrada simplificado para depuración local.

Permite ejecutar el pipeline sin necesidad de ajustar PYTHONPATH manualmente
porque agrega automáticamente la carpeta ``src`` al ``sys.path``. Expone los
mismos flags que ``doctor_canamo.cli`` para mantener compatibilidad.
"""
from pathlib import Path
import sys

# Asegura que la carpeta src esté en el path para importaciones locales
ROOT = Path(__file__).parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from doctor_canamo.cli import main


if __name__ == "__main__":
    main()
