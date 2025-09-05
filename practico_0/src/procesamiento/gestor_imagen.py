import logging
from PIL import Image, ImageOps, UnidentifiedImageError

logging.basicConfig(level=logging.ERROR)


class GestorImagen:
    @staticmethod
    def abrir_imagen(ruta):
        try:
            return Image.open(ruta).convert("RGB")
        except UnidentifiedImageError as e:
            logging.error(f"Archivo no reconocido como imagen: {e}")
            return None
        except OSError as e:
            logging.error(f"Error de lectura del archivo: {e}")
            return None

    @staticmethod
    def invertir_colores(imagen_pil):
        try:
            return ImageOps.invert(imagen_pil)
        except ValueError as e:
            logging.error(f"Error al invertir imagen (formato inválido): {e}")
            return None
        except Exception as e:
            logging.error(f"Error desconocido al invertir imagen: {e}")
            return None

    @staticmethod
    def guardar_imagen(imagen_pil, ruta_destino):
        try:
            imagen_pil.save(ruta_destino)
            return True
        except OSError as e:
            logging.error(f"Error al guardar imagen: {e}")
            return False
        except ValueError as e:
            logging.error(f"Parámetros inválidos al guardar imagen: {e}")
            return False
