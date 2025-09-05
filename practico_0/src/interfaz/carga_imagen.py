from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt, pyqtSignal
from pathlib import Path
from paths import ICONS_DIR, EXTENSIONES_VALIDAS


class AreaCargaImagen(QFrame):
    solicitar_archivo = pyqtSignal()
    archivo_arrastrado = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("DropZone")
        self.setFixedHeight(300)
        self.setAcceptDrops(True)

        self.pixmap_visualizacion = None

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.icon_label = QLabel()
        icon_pixmap = QPixmap(str(ICONS_DIR / "image_placeholder.svg")).scaled(
            80, 80, Qt.AspectRatioMode.KeepAspectRatio
        )
        self.icon_label.setPixmap(icon_pixmap)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text_label = QLabel("Arrastrá una imagen o hacé clic para cargar")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        self.setLayout(layout)

    # ---- Arrastrar y soltar ----
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                ruta = urls[0].toLocalFile()
                ext = Path(ruta).suffix.lower()
                if ext in EXTENSIONES_VALIDAS:
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            ruta = event.mimeData().urls()[0].toLocalFile()
            self.archivo_arrastrado.emit(ruta)

    # ---- Hover y click ----
    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.solicitar_archivo.emit()

    def mostrar_imagen(self, qpixmap):
        self.pixmap_visualizacion = qpixmap
        self.icon_label.setPixmap(self.pixmap_visualizacion)
        self.text_label.setVisible(False)
