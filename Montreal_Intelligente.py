# Data from:
# http://donnees.ville.montreal.qc.ca/dataset/abattage-arbres-publics
# https://automating-gis-processes.github.io/2017/lessons/L5/interactive-map-folium.html

# --General modules--
from PyQt5.QtWidgets import *
import sys
import os
from PyQt5.QtGui import QIcon
import qdarkstyle
# --My modules--
from tab_widget import TabWidget


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('Montréal Intelligente')
        self.create_toolbar()
        # message at the bottom
        self.intro_message = 'Montréal la ville intelligente (HackaTown 2019)...'
        self.statusBar().showMessage(self.intro_message)

    def initUI(self):
        self.tab_w = TabWidget(self)
        self.setCentralWidget(self.tab_w)
        self.setGeometry(0, 0, 1000, 1000)
        self.show()

    def create_toolbar(self):
        main_tb = QToolBar('main actions')
        main_tb.addAction(self.create_exit_action())
        main_tb.addAction(self.create_dark_mode_activator())
        self.addToolBar(main_tb)

    def create_exit_action(self):
        base_path = os.getcwd()
        path = os.path.join(base_path, 'toolbar_icon/exit.png')
        exitIcon = QIcon(path)
        exitAct = QAction(exitIcon, 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)
        return exitAct

    def create_dark_mode_activator(self):
        base_path = os.getcwd()
        path = os.path.join(base_path, 'toolbar_icon/light_mode.png')
        light_act = QAction(QIcon(path), 'change light style', self)
        light_act.setStatusTip('Change style to qdarkstyle')
        light_act.triggered.connect(self.change_light_style)
        return light_act

    def change_light_style(self):
        self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWin()
    sys.exit(app.exec_())
