from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QFrame,
)
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtCore import Qt, QSize
from paths import LOGO_PATH, ICONS_DIR, ESTILOS_PATH
from interfaz.carga_imagen import AreaCargaImagen
from procesamiento.gestor_imagen import GestorImagen
from PIL import ImageOps


class PantallaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Práctico 0 - Procesamiento de Imágenes")
        self.setGeometry(100, 100, 800, 600)

        self.imagen_original = None
        self.imagen_actual = None
        self.ruta_actual = None

        self.init_ui()
        self.cargar_estilos()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(10)

        # --- Encabezado ---
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(15, 0, 15, 0)
        header_layout.setSpacing(15)

        logo_label = QLabel()
        logo_pixmap = QPixmap(str(LOGO_PATH)).scaled(
            200, 183, Qt.AspectRatioMode.KeepAspectRatio
        )
        logo_label.setPixmap(logo_pixmap)
        header_layout.addWidget(logo_label)

        header_text_layout = QVBoxLayout()
        header_text_layout.setSpacing(5)

        title_label = QLabel("Procesamiento Digital de Imágenes")
        title_label.setObjectName("tituloMateria")
        practico_label = QLabel("Práctico 0")
        practico_label.setObjectName("tituloPractico")
        group_label = QLabel("Grupo 18")
        group_label.setObjectName("grupo")

        names = [
            "Albarracín Agustin Lautaro",
            "Mercado Daniel Arnaldo",
            "Ontiveros Brian Emmanuel",
        ]
        for n in names:
            l = QLabel(n)
            l.setObjectName("nombreIntegrante")
            header_text_layout.addWidget(l)

        header_text_layout.insertWidget(0, group_label)
        header_text_layout.insertWidget(0, practico_label)
        header_text_layout.insertWidget(0, title_label)

        header_layout.addLayout(header_text_layout)
        header_frame.setLayout(header_layout)
        main_layout.addWidget(header_frame)

        # --- Área de carga ---
        self.drop_zone = AreaCargaImagen()
        self.drop_zone.setObjectName("DropZone")
        self.drop_zone.solicitar_archivo.connect(self.abrir_dialogo_imagen)
        self.drop_zone.archivo_arrastrado.connect(self.cargar_imagen)

        if self.drop_zone.layout() is not None:
            self.drop_zone.layout().setContentsMargins(0, 0, 0, 0)
            self.drop_zone.layout().setSpacing(0)

        main_layout.addWidget(self.drop_zone)

        # --- Botones ---
        botones_layout = QHBoxLayout()

        self.boton_invertir = QPushButton("Invertir colores")
        self.boton_invertir.clicked.connect(self.invertir_imagen)
        self.boton_invertir.setIcon(QIcon(str(ICONS_DIR / "invert_colors.svg")))
        self.boton_invertir.setIconSize(QSize(24, 24))
        botones_layout.addWidget(self.boton_invertir)

        self.boton_restaurar = QPushButton("Restaurar imagen")
        self.boton_restaurar.clicked.connect(self.restaurar_imagen)
        self.boton_restaurar.setIcon(QIcon(str(ICONS_DIR / "file_restore.svg")))
        self.boton_restaurar.setIconSize(QSize(24, 24))
        botones_layout.addWidget(self.boton_restaurar)

        self.boton_guardar = QPushButton("Guardar imagen")
        self.boton_guardar.clicked.connect(self.guardar_imagen)
        self.boton_guardar.setIcon(QIcon(str(ICONS_DIR / "image_save.svg")))
        self.boton_guardar.setIconSize(QSize(24, 24))
        botones_layout.addWidget(self.boton_guardar)

        self.boton_salir = QPushButton("Salir")
        self.boton_salir.setObjectName("boton_salir")
        self.boton_salir.clicked.connect(self.close)
        self.boton_salir.setIcon(QIcon(str(ICONS_DIR / "exit_run.svg")))
        self.boton_salir.setIconSize(QSize(24, 24))
        botones_layout.addWidget(self.boton_salir)

        main_layout.addLayout(botones_layout)
        self.setLayout(main_layout)

        self._set_botones_visibles(False)

    def cargar_estilos(self):
        if ESTILOS_PATH.exists():
            with open(ESTILOS_PATH, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def abrir_dialogo_imagen(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar imagen",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)",
        )
        if ruta:
            self.cargar_imagen(ruta)

    def cargar_imagen(self, ruta):
        self.ruta_actual = ruta
        imagen = GestorImagen.abrir_imagen(ruta)
        if imagen:
            imagen = ImageOps.exif_transpose(imagen)
            self.imagen_original = imagen.copy()
            self.imagen_actual = imagen.copy()

            pixmap = self._convertir_pil_a_qpixmap(imagen)
            if pixmap:
                self.drop_zone.mostrar_imagen(pixmap)
                self._set_botones_visibles(True)

    def invertir_imagen(self):
        if self.imagen_actual:
            self.imagen_actual = GestorImagen.invertir_colores(self.imagen_actual)
            self.mostrar_imagen_actual()

    def restaurar_imagen(self):
        if self.imagen_original:
            self.imagen_actual = self.imagen_original.copy()
            self.mostrar_imagen_actual()

    def mostrar_imagen_actual(self):
        if self.imagen_actual:
            pixmap = self._convertir_pil_a_qpixmap(self.imagen_actual)
            if pixmap:
                self.drop_zone.mostrar_imagen(pixmap)

    def guardar_imagen(self):
        if self.imagen_actual:
            ruta, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar imagen como",
                "",
                "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp);;TIFF (*.tiff)",
            )
            if ruta:
                ok = GestorImagen.guardar_imagen(self.imagen_actual, ruta)
                if ok:
                    QMessageBox.information(
                        self, "Éxito", "Imagen guardada correctamente."
                    )
                else:
                    QMessageBox.critical(self, "Error", "No se pudo guardar la imagen.")

    def _convertir_pil_a_qpixmap(self, imagen_pil):
        """Convierte PIL → QPixmap escalado al área de drop_zone."""
        try:
            imagen_rgb = imagen_pil.convert("RGB")
            data = imagen_rgb.tobytes("raw", "RGB")
            qimage = QImage(
                data,
                imagen_rgb.width,
                imagen_rgb.height,
                imagen_rgb.width * 3,
                QImage.Format.Format_RGB888,
            )
            dz_height = self.drop_zone.height()
            dz_width = self.drop_zone.width()
            return QPixmap.fromImage(qimage).scaled(
                dz_width, dz_height, Qt.AspectRatioMode.KeepAspectRatio
            )
        except Exception as e:
            print(f"❌ Error al convertir PIL → QPixmap: {e}")
            return None

    def _set_botones_visibles(self, estado: bool):
        """Muestra/oculta los botones de edición."""
        self.boton_invertir.setVisible(estado)
        self.boton_restaurar.setVisible(estado)
        self.boton_guardar.setVisible(estado)
