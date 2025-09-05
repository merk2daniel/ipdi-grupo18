import logging
from PIL import Image, ImageOps, UnidentifiedImageError
import numpy as np

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

    @staticmethod
    def procesar_yiq(imagen_pil, a=1.0, b=1.0):
        """
        Convierte RGB -> YIQ, aplica escalado a Y, I, Q,
        chequea límites y convierte de nuevo a RGB.
        """
        try:
            img_array = np.array(imagen_pil).astype(np.float32) / 255.0

            # Matrices
            rgb2yiq = np.array([[0.299, 0.587, 0.114],
                                [0.596, -0.274, -0.322],
                                [0.211, -0.523, 0.312]])

            yiq2rgb = np.array([[1.0, 0.956, 0.621],
                                [1.0, -0.272, -0.647],
                                [1.0, -1.106, 1.703]])

            # Transformación RGB -> YIQ
            yiq = img_array @ rgb2yiq.T

            # Escalar componentes
            Y = a * yiq[:, :, 0]
            I = b * yiq[:, :, 1]
            Q = b * yiq[:, :, 2]

            # Chequear límites
            Y = np.clip(Y, 0, 1)
            I = np.clip(I, -0.5957, 0.5957)
            Q = np.clip(Q, -0.5226, 0.5226)

            # Reconstruir YIQ
            yiq_proc = np.stack([Y, I, Q], axis=-1)

            # YIQ -> RGB
            rgb_proc = yiq_proc @ yiq2rgb.T
            rgb_proc = np.clip(rgb_proc, 0, 1)

            # Convertir a bytes [0,255]
            img_uint8 = (rgb_proc * 255).astype(np.uint8)
            return Image.fromarray(img_uint8)

        except Exception as e:
            print(f"Error en procesamiento YIQ: {e}")
            return None


    def rgb_a_yiq(imagen_pil):
        try:
            img_array = np.array(imagen_pil).astype(np.float32) / 255.0

            # Matriz RGB -> YIQ
            matriz = np.array([[0.299, 0.587, 0.114],
                               [0.596, -0.274, -0.322],
                               [0.211, -0.523, 0.312]])

            yiq = img_array @ matriz.T

            # Para visualizar: usamos solo Y (luminancia)
            Y = yiq[:, :, 0]  
            Y_img = (Y * 255).clip(0, 255).astype(np.uint8)
            return Image.fromarray(Y_img)
        except Exception as e:
            print(f"Error en RGB -> YIQ: {e}")
            return None
        
    def normalizar_imagen(imagen_pil):
        try:
            img_array=np.array(imagen_pil).astype(np.float32)
            img_norm=img_array / 255.0
            img_uint8 = (img_norm * 255).astype(np.uint8)
            return Image.fromarray(img_uint8)
        except Exception as e:
            print(f"Error al normalizar: {e}")
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
