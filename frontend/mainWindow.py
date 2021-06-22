import sys

from PyQt5 import QtWidgets

from settings import PROJECT_NAME


class MainWindow:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)

        window = QtWidgets.QMainWindow()
        self.init_gui()

        window.show()
        window.setWindowTitle(PROJECT_NAME)
        window.setGeometry(300, 50, 300, 500)

        sys.exit(app.exec())

    def init_gui(self):
        pass
