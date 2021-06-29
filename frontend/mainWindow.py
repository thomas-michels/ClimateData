import sys
from datetime import date

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel

from frontend.styleSheet import STYLE
from settings import PROJECT_NAME, INIT_SCREEN_X, INIT_SCREEN_Y, SIZE_X, SIZE_Y, VERSION


class MainWindow:

    _components = {}

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        self.window = QtWidgets.QMainWindow()

        self._font = QtGui.QFont('Lucida Console')
        self._font.setPointSize(12)

        self._font_credit = QtGui.QFont('Lucida Console')
        self._font_credit.setPointSize(8)

        self._font_bold = QtGui.QFont('Helvetica')
        self._font_bold.setPointSize(12)
        self._font_bold.setBold(True)

        self.init_gui()
        self.lbl_load = self.load()

        self.btn_download.clicked.connect(self.start_load)

        self.window.show()
        self.window.setWindowTitle(PROJECT_NAME)
        self.window.setStyleSheet(STYLE)
        self.window.setGeometry(INIT_SCREEN_X, INIT_SCREEN_Y, SIZE_X, SIZE_Y)

        sys.exit(self.app.exec())

    def init_gui(self):

        lbl_files = self._create_label("Quantidade de Arquivos", 55, 20, 200, 30, bold=True)
        self._components['lbl_files'] = lbl_files

        cb_files = self._create_combo_box(80, 60, 190, 100)
        cb_files.addItem('1 Arquivo')
        cb_files.addItem('Vários Arquivos')
        self._components['cb_files'] = cb_files

        lbl_extract = self._create_label("EXTRAÇÃO", 110, 130, 190, 30, bold=True)
        self._components['lbl_extract'] = lbl_extract

        lbl_url = self._create_label('URL', 55, 190, 190, 30)
        self._components['lbl_url'] = lbl_url

        cb_station = self._create_combo_box(140, 190, 190, 30)
        cb_station.addItem('Weather')
        self._components['cb_station'] = cb_station

        lbl_station = self._create_label("Estação", 30, 230, 190, 30)
        self._components['lbl_station'] = lbl_station

        et_station = self._create_edit_text(120, 230, 150, 30)
        self._components['et_station'] = et_station

        lbl_init_date = self._create_label('Data Início', 20, 270, 190, 30)
        self._components['lbl_init_date'] = lbl_init_date

        dt_init = self._create_date_edit(140, 275, 190, 30)
        self._components['dt_init'] = dt_init

        lbl_final_date = self._create_label('Data Final', 20, 310, 190, 30)
        self._components['lbl_final_date'] = lbl_final_date

        dt_final = self._create_date_edit(140, 315, 190, 30)
        self._components['dt_final'] = dt_final

        self.btn_download = self._create_button('BAIXAR', 90, 420, 120, 40)
        self._components['btn_download'] = self.btn_download

        lbl_version = self._create_label(VERSION, 10, 470, 300, 30, credit=True)

    def load(self):
        label = QLabel(self.window)

        self.movie = QMovie('frontend/images/loading.gif')
        label.setMovie(self.movie)
        label.setScaledContents(True)
        label.setGeometry(25, 100, 250, 250)
        label.setVisible(False)
        return label

    def start_load(self):
        self._components_visible(False)
        self.lbl_load.setVisible(True)
        self.movie.start()

    def stop_load(self):
        self.movie.stop()
        self.lbl_load.setVisible(False)
        self._components_visible(True)

    def _components_visible(self, bool):
        for component in self._components.keys():
            self._components[component].setVisible(bool)

    def _create_button(self, text, pos_x, pos_y, tam_x, tam_y):
        btn = QtWidgets.QPushButton(text, self.window)
        btn.setGeometry(pos_x, pos_y, tam_x, tam_y)
        btn.setFont(self._font)
        return btn

    def _create_label(self, text, pos_x, pos_y, tam_x, tam_y, bold=False, credit=False):
        lbl = QtWidgets.QLabel(text, self.window)
        lbl.setGeometry(pos_x, pos_y, tam_x, tam_y)
        if bold:
            lbl.setFont(self._font_bold)

        else:
            lbl.setFont(self._font)

        if credit:
            lbl.setFont(self._font_credit)

        return lbl

    def _create_combo_box(self, pos_x, pos_y, tam_x, tam_y):
        widget = QtWidgets.QWidget(self.window)
        widget.setGeometry(pos_x, pos_y, tam_x, tam_y)
        cb = QtWidgets.QComboBox(widget)
        cb.setFont(self._font_bold)
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

    def _loading(self, path):
        image = QtGui.QImage(path)
        display_image = QtGui.QPixmap.fromImage(image)
        lbl = self._create_label('', 0, 75, 300, 300)
        lbl.setPixmap(display_image)
        lbl.setScaledContents(True)
        return lbl
