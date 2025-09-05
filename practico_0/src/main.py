import sys
from PyQt6.QtWidgets import QApplication
from interfaz.pantalla_inicio import PantallaInicio


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PantallaInicio()
    window.show()
    sys.exit(app.exec())
