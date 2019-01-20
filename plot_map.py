# Data from:
# http://donnees.ville.montreal.qc.ca/dataset/abattage-arbres-publics
# https://automating-gis-processes.github.io/2017/lessons/L5/interactive-map-folium.html

# --General module--
import folium
from PyQt5 import QtWebEngineWidgets, QtCore
from PyQt5.QtWidgets import *
from functools import partial
import sys
import os
import pandas
import numpy as np
from pyqtgraph.dockarea import *
# --My Modules--
from inner_dock import InnerDock
from select_file import select_file


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.table_widget.setWindowTitle('HackaTown')
        self.setGeometry(0, 0, 1000, 1000)
        self.show()


class MyTableWidget(QWidget):
    def __init__(self, main_win):
        super(QWidget, self).__init__(main_win)
        self.main_win = main_win

        self.base_path = os.getcwd()
        self.main_layout = QGridLayout(self)

        self.dock_area = DockArea()
        self.main_layout.addWidget(self.dock_area)

        self.lat_str = 'LATITUDE_ORIGINE'
        self.long_str = 'LONGITUDE_ORIGINE'
        self.csv_path = 'remorquages.csv'

        self.map_path = os.path.join(self.base_path, 'montreal_map.html')
        # Select file
        self.create_select_file_form()
        # Map
        self.m = self.create_map()
        # self.add_data_to_map()
        # View
        view = self.create_view()
        self.main_layout.addWidget(view, 2, 0, 1, 3)

        self.setLayout(self.main_layout)

    def create_inner_dock(self, layout):
        inner_dock = InnerDock(
                layout, 'Inner dock', b_pos=(1, 1), toggle_button=True,
                b_checked=False, background_color='k')
        return inner_dock

    def create_select_file_form(self):
        # Create dock
        # opening_dock = InnerDock(
        #     self.layout, 'Saving', b_pos=(0, 0), toggle_button=True,
        #     size=(1, 1))
        # self.dock_area.addDock(opening_dock.dock)

        csv_path_edit = QLineEdit('')
        # Buttons
            # Choose map b
        choose_map_file_b = QPushButton('Choose map file')
        choose_map_file_b.clicked.connect(
            partial(self.select_f, csv_path_edit))
            # Open data b
        add_data_to_map_b = QPushButton('Add data to map')
        add_data_to_map_b.clicked.connect( self.refresh_map)
        # Add to layout
        self.main_layout.addWidget(choose_map_file_b, 0, 0)
        self.main_layout.addWidget(csv_path_edit, 0, 1)
        self.main_layout.addWidget(add_data_to_map_b, 0, 2)

    def select_f(self, csv_path_edit):
        f_name = select_file(self.main_win, open=True, f_extension='.csv')
        csv_path_edit.setText(f_name)
        self.csv_path = f_name

    def refresh_map(self):
        print('refreshing')
        self.create_map()
        self.add_data_to_map()
        view = self.create_view()
        self.main_layout.addWidget(view, 2, 0, 1, 3)

    def create_map(self):
        m = folium.Map(
            location=[45.5088, -73.554], tiles='Stamen Toner', zoom_start=12,
            control_scale=True)
        m.save('montreal_map.html')
        return m

    def read_data(self):
        remorquage_csv = pandas.read_csv(self.csv_path)
        remorquage_df = pandas.DataFrame(remorquage_csv)
        lats = np.array(remorquage_df[self.long_str])[0:100]
        longs = np.array(remorquage_df[self.lat_str])[0:100]
        return lats, longs

    def add_data_to_map(self):
        lats, longs = self.read_data()
        for lat, long in zip(lats, longs):
            try:
                folium.Marker([long, lat]).add_to(self.m)
            except ValueError as e:
                pass
        self.m.save('montreal_map.html')

    def create_view(self):
        view = QtWebEngineWidgets.QWebEngineView()
        view.load(QtCore.QUrl().fromLocalFile(
                os.path.join(self.base_path, 'montreal_map.html')))
        return view


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWin()
    sys.exit(app.exec_())
