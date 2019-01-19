import folium
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWebEngineWidgets, QtCore

# Create a Map instance
m = folium.Map(
        location=[45.5088, -73.554], tiles='Stamen Toner',
        zoom_start=12, control_scale=True)

m.save('my_map.html')

app = QApplication(sys.argv)
view = QtWebEngineWidgets.QWebEngineView()

view.load(QtCore.QUrl().fromLocalFile(
        '/home/alex/Documents/CODING/2018/Hackatown/my_map.html'))

view.show()
sys.exit(app.exec_())
