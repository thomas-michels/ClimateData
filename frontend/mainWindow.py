import sys
from datetime import date

from PyQt5 import QtWidgets, QtGui

from frontend.styleSheet import STYLE
from settings import PROJECT_NAME, INIT_SCREEN_X, INIT_SCREEN_Y, SIZE_X, SIZE_Y


class MainWindow:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        self.window = QtWidgets.QMainWindow()

        self._font = QtGui.QFont()
        self._font.setPointSize(12)

        self.init_gui()

        self.window.show()
        self.window.setWindowTitle(PROJECT_NAME)
        self.window.setStyleSheet(STYLE)
        self.window.setGeometry(INIT_SCREEN_X, INIT_SCREEN_Y, SIZE_X, SIZE_Y)

        sys.exit(self.app.exec())

    def init_gui(self):

        lbl_files = self._create_label("Quantidade de Arquivos", 55, 20, 190, 30)

        cb_files = self._create_combo_box(55, 60, 190, 30)
        cb_files.addItem('1 Arquivo')
        cb_files.addItem('Vários Arquivos')

        lbl_extract = self._create_label("Extração", 55, 100, 190, 30)

        lbl_url = self._create_label('URL', 55, 135, 190, 30)

        cb_station = self._create_combo_box(120, 140, 190, 30)
        cb_station.addItem('Weather')

        lbl_station = self._create_label("Estação", 55, 180, 190, 30)

        et_station = self._create_edit_text(120, 180, 150, 30)

        lbl_init_date = self._create_label('Data Início', 55, 220, 190, 30)

        dt_init = self._create_date_edit(140, 220, 190, 30)

        lbl_final_date = self._create_label('Data Final', 55, 260, 190, 30)

        dt_final = self._create_date_edit(140, 260, 190, 30)

        btn_download = self._create_button('BAIXAR', 90, 420, 120, 40)

    def _create_button(self, text, pos_x, pos_y, tam_x, tam_y):
        btn = QtWidgets.QPushButton(text, self.window)
        btn.setGeometry(pos_x, pos_y, tam_x, tam_y)
        btn.setFont(self._font)
        return btn

    def _create_label(self, text, pos_x, pos_y, tam_x, tam_y):
        lbl = QtWidgets.QLabel(text, self.window)
        lbl.setGeometry(pos_x, pos_y, tam_x, tam_y)
        lbl.setFont(self._font)
        return lbl

    def _create_combo_box(self, pos_x, pos_y, tam_x, tam_y):
        widget = QtWidgets.QWidget(self.window)
        widget.setGeometry(pos_x, pos_y, tam_x, tam_y)
        cb = QtWidgets.QComboBox(widget)
        cb.setFont(self._font)
        return cb

    def _create_edit_text(self, pos_x, pos_y, tam_x, tam_y):
        et = QtWidgets.QTextEdit(self.window)
        et.setGeometry(pos_x, pos_y, tam_x, tam_y)
        et.setFont(self._font)
        return et

    def _create_date_edit(self, pos_x, pos_y, tam_x, tam_y):
        widget = QtWidgets.QWidget(self.window)
        widget.setGeometry(pos_x, pos_y, tam_x, tam_y)
        dt = QtWidgets.QDateEdit(widget)
        dt.setDate(date.today())
        dt.setCalendarPopup(True)
        dt.setFont(self._font)
        return dt
