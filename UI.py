import sys
from PyQt6.QtWidgets import QApplication, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCalendarWidget, QLabel, QFrame, QProgressBar
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QProgressBar
import log
import sqlite3
import threading
import download
import SQL_Import
import SQL_Select
from pyqtgraph import PlotWidget, AxisItem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

conn2 = sqlite3.connect("sensor-data.db")
c2 = conn2.cursor()

class MyForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('assets\images\hippie-marijuana-weed.svg'))
        self.setWindowTitle("Feinstaub Projekt")

        self.oben = QHBoxLayout()
        self.unten = QHBoxLayout()

        self.layout = QVBoxLayout()

        # Linkes Layout erstellen
        left_layout = QVBoxLayout()

        # Label für den Kalender erstellen
        self.label = QLabel("Wähle ein Datum:")
        font = QFont("Roboto", 20)
        self.label.setFont(font)
        left_layout.addWidget(self.label)

        # Kalender erstellen
        self.calendar = QCalendarWidget()
        left_layout.addWidget(self.calendar)

        # Button für Suche erstellen
        self.button = QPushButton("Suche")
        self.button.clicked.connect(self.suchen_clicked)
        left_layout.addWidget(self.button)

        # Linkes Layout zur Gesamt-LayoutBox hinzufügen
        self.oben.addLayout(left_layout)

        # Rechtes Layout erstellen
        right_layout = QVBoxLayout()

        self.label = QLabel("Aktualisiere Daten")
        font = QFont("Roboto", 10)
        self.label.setFont(font)
        self.unten.addWidget(self.label)

        # Grafik-Layout erstellen
        self.graph_layout = QVBoxLayout()

        # ScatterGraph-Klasse erstellen und dem Layout hinzufügen
        self.line_graph = LineGraph()
        self.graph_layout.addWidget(self.line_graph)

        self.Combo_Box = QComboBox()
        self.Combo_Box.addItem("Temperatur")
        self.Combo_Box.addItem("Luftfeuchtigkeit")
        self.Combo_Box.addItem("P1")
        self.Combo_Box.addItem("P2")
        self.Combo_Box.addItem("Gesamt")
        self.Combo_Box.setItemIcon(1, QIcon("assets\images\interface-weather-rain-drop.png"))
        self.Combo_Box.setItemIcon(3, QIcon("assets\images\co2-icon.svg"))

        right_layout.addWidget(self.Combo_Box)

        # Grafik-Layout zum rechten Layout hinzufügen
        right_layout.addLayout(self.graph_layout)

        # Rechtes Layout zur Gesamt-LayoutBox hinzufügen
        self.oben.addLayout(right_layout)

        self.layout.addLayout(self.oben)
        self.layout.addLayout(self.unten)
        self.setLayout(self.layout)

        # Thread für den Download erstellen und starten
        self.download_thread = threading.Thread(target=self.download_data)
        self.download_thread.start()

    def suchen_clicked(self):
        datum = self.calendar.selectedDate().toString("yyyy-MM-dd")
        try:
            log.writelog("Datum ausgewählt: " + datum)
        except Exception as e:
            print("Fehler beim Schreiben in die Log-Datei:", e)
        selected_value = self.Combo_Box.currentText()
        x = SQL_Select.SELECT(datum, selected_value, 'DATUM')
        y = SQL_Select.SELECT(datum, selected_value, 'WERT')

        self.line_graph.plot(x, y)

    def download_data(self):
        conn = sqlite3.connect("sensor-data.db")
        c = conn.cursor()
        days_to_download = download.getdays(c, conn)
        if days_to_download == 0: 
            self.label.hide()
        else:
            self.label.setText("Download Data")
            download.download_days(days_to_download)
            SQL_Import.importtoDB(c, conn, self.label)
            
class LineGraph(PlotWidget):
    def __init__(self, parent=None):
        super(LineGraph, self).__init__(parent)

    def plot(self, x, y):
        self.clear()
        self.plotItem.plot(x, y, pen='r')
        self.setTitle('Sensor Data')

    def clear(self):
        self.plotItem.clear()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())
         

