import os
import pandas
import numpy as np
from pyqtgraph.dockarea import *
import pyqtgraph as pg
from date_axis import DateAxis
import folium
from PyQt5 import QtWebEngineWidgets, QtCore
from PyQt5.QtWidgets import *
from functools import partial
# --My Modules--
from inner_dock import InnerDock
from select_file import select_file
from colors import *
from btn import btn


class MapTabWidget(QWidget):
    def __init__(self, main_win):
        super(QWidget, self).__init__(main_win)
        self.main_win = main_win

        self.base_path = os.getcwd()
        self.main_layout = QGridLayout(self)

        self.dock_area = DockArea()
        self.main_layout.addWidget(self.dock_area, 1, 0, 4, 6)

        self.lat_str = 'LATITUDE_ORIGINE'
        self.long_str = 'LONGITUDE_ORIGINE'
        self.csv_path = 'csv_data/remorquages.csv'
        self.lats = None
        self.longs = None
        self.t_span_left = 0
        self.t_span_right = 100

        self.map_path = os.path.join(self.base_path, 'montreal_map.html')
        # Select file
        self.create_select_file_form()
        # Settings dock
        self.create_settings_dock()
        # Map
        self.m = self.create_map()
        # self.add_data_to_map()
        # View
        self.view_dock = InnerDock(
            self.main_layout, 'Saving', b_pos=(2, 0),
            toggle_button=False, size=(40, 40))
        self.create_view()
        # Time span dock
        self.time_span_dock = self.create_time_span_dock()

        self.setLayout(self.main_layout)

    def create_settings_dock(self):
        settings_dock = InnerDock(
            self.main_layout, 'Settings', b_pos=(0, 1),
            toggle_button=True, size=(1, 1))
        self.dock_area.addDock(settings_dock.dock)
        # Line edit
        form = QGroupBox('')
        f_l = QFormLayout()
        form.setLayout(f_l)
        df_possible_val = [
            'Latitude field', 'Longitude field', 'Time field']
        self.df_combobox = [QComboBox() for _ in range(len(df_possible_val))]
        for val, cb in zip(df_possible_val, self.df_combobox):
            f_l.addRow(QLabel(f'{val}: '), cb)
            cb.name = val
            cb.activated[str].connect(partial(self.set_cb_val, cb))
        settings_dock.layout.addWidget(form)
        return settings_dock

    def change_t_boundaries(self, r):
        self.t_span_left= int(r.boundingRect().left())
        self.t_span_right = int(r.boundingRect().right())
        print('left: ', self.t_span_left, 'right: ', self.t_span_right)

    def set_cb_val(self, cb, cb_val):
        if cb.name == 'Latitude field':
            self.lat_str = cb_val
        elif cb.name == 'Longitude field':
            self.long_str = cb_val

    def create_time_span_dock(self):
        time_span_dock = InnerDock(
            self.main_layout, 'Time span', b_pos=(0, 2),
            toggle_button=True, size=(1, 1))
        self.dock_area.addDock(time_span_dock.dock)
        # Date
        d_axis = DateAxis(orientation='bottom')
        # time plot region
        t_plot = pg.PlotWidget(
            background=dark_grey, axisItems={'bottom':d_axis})
        t_plot.setXRange(0, 100)
        t_plot.hideAxis('left')
        # Region
        t_region = pg.LinearRegionItem([0, 10])
        t_region.sigRegionChanged.connect(
            partial(self.change_t_boundaries, t_region))
        t_plot.addItem(t_region, ignoreBounds=True)

        time_span_dock.layout.addWidget(t_plot)
        return time_span_dock, t_plot

    def create_select_file_form(self):
        # Dock
        opening_dock = InnerDock(
            self.main_layout, 'Select file', b_pos=(0, 0),
            toggle_button=True, size=(1, 1))
        self.dock_area.addDock(opening_dock.dock)

        csv_path_edit = QLineEdit('')
        # Buttons
        # Choose map b
        choose_map_file_b = QPushButton('Choose csv data file')
        choose_map_file_b.clicked.connect(
            partial(self.select_f, csv_path_edit))
        # Read csv_data b
        read_header_b = btn(
            'Read csv data', opening_dock.layout, pos=(0, 2),
            func_conn=self.read_header, color=map_blue_b, txt_color=white)
        # Open csv_data b
        add_data_to_map_b = btn(
            'Add csv data to map', opening_dock.layout, pos=(0, 3),
            func_conn=self.refresh_map, color=map_blue_b, txt_color=white)
        # add_data_to_map_b.clicked.connect( self.refresh_map)
        # Add to layout
        opening_dock.layout.addWidget(choose_map_file_b, 0, 0)
        opening_dock.layout.addWidget(csv_path_edit, 0, 1)
        # .addWidget(add_data_to_map_b, 0, 2)

    def select_f(self, csv_path_edit):
        f_name = select_file(self.main_win, open=True, f_extension='.csv')
        csv_path_edit.setText(f_name)
        self.csv_path = f_name

    def refresh_map(self):
        self.create_map()
        self.add_data_to_map()
        self.create_view()
        try:
            self.time_span_dock.dock.close()
        except AttributeError as e:
            print(e)
        self.time_span_dock, self.t_plot = self.create_time_span_dock()

    def create_map(self):
        m = folium.Map(
            location=[45.5088, -73.554], tiles='Stamen Toner', zoom_start=12,
            control_scale=True)
        m.save('mtl_map.html')
        return m

    def create_combobox(self, df_vals):
        for cb in self.df_combobox:
            for val in df_vals:
                cb.addItem(val)

    def read_header(self):
        remorquage_csv = pandas.read_csv(self.csv_path)
        remorquage_df = pandas.DataFrame(remorquage_csv)
        df_vals = remorquage_df.columns.values
        self.create_combobox(df_vals)

    def read_data(self):
        remorquage_csv = pandas.read_csv(self.csv_path)
        remorquage_df = pandas.DataFrame(remorquage_csv)
        print('left', self.t_span_left, 'right', self.t_span_right)
        self.lats = np.array(
                remorquage_df[self.lat_str])[
                        self.t_span_left:self.t_span_right]
        self.longs = np.array(
                remorquage_df[self.long_str])[
                        self.t_span_left:self.t_span_right]

    def add_data_to_map(self):
        self.read_data()
        for lat, long in zip(self.lats, self.longs):
            try:
                folium.Marker([lat, long]).add_to(self.m)
            except ValueError as e:
                pass
        self.m.save('mtl_map.html')

    def create_view(self):
        view = QtWebEngineWidgets.QWebEngineView()
        view.load(QtCore.QUrl().fromLocalFile(
                os.path.join(self.base_path, 'mtl_map.html')))
        self.view_dock.layout.addWidget(view, 0, 0)
        self.dock_area.addDock(self.view_dock.dock)
