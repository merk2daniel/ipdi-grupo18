from pathlib import Path

# Directorio base = carpeta "src"
BASE_DIR = Path(__file__).resolve().parent

# Carpeta assets
ASSETS_DIR = BASE_DIR / "assets"

# Rutas específicas
LOGO_PATH = ASSETS_DIR / "logo_fi_unju.png"
ICONS_DIR = ASSETS_DIR / "icons"

# Extensiones válidas para imágenes
EXTENSIONES_VALIDAS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff"}

# Ruta del archivo de estilos
ESTILOS_PATH = BASE_DIR / "estilos.qss"
