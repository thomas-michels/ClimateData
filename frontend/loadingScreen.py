from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QLabel


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(200, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        self.label = QLabel(self)

        self.movie = QMovie('frontend/images/loading.gif')
        self.label.setMovie(self.movie)

        timer = QTimer(self)

        self.start_animation()
        timer.singleShot(3000, self.stop_animation)

        self.show()

    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()
        self.close()
