import sys
sys.path.append("/usr/local/lib/python3.13/dist-packages")

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QMovie, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer
import os
from gui.main_window import MainWindow

class SplashWidget(QWidget):
    def __init__(self, gif_path=None):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 400, 300)

        if gif_path and os.path.exists(gif_path):
            self.movie = QMovie(gif_path)
            self.label.setMovie(self.movie)
            self.movie.start()
        else:
            pixmap = QPixmap(400, 300)
            pixmap.fill(Qt.black)
            self.label.setPixmap(pixmap)
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setFont(QFont("Courier", 14))
            self.label.setText("Initialisation de RedSpectre...")

def launch_gui():
    app = QApplication(sys.argv)
    gif_path = "/opt/redspectre/assets/splash_scanner.gif"
    splash = SplashWidget(gif_path)
    splash.show()

    def start_main():
        splash.close()
        global main_window
        main_window = MainWindow()
        main_window.show()

    QTimer.singleShot(3000, start_main)
    sys.exit(app.exec_())

if __name__ == "__main__":
    launch_gui()
