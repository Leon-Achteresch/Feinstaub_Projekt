import sys
from PyQt6.QtWidgets import QApplication, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCalendarWidget, QLabel, QFrame, QProgressBar
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6.QtGui import QFont, QIcon
import log
import sqlite3
import threading
import download
import SQL_Import
import SQL_Select
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(15)
        self.unten.addWidget(self.progress_bar, 1, QtCore.Qt.AlignmentFlag.AlignBottom)

        # Grafik-Layout erstellen
        self.graph_layout = QVBoxLayout()

        # Graph-Klasse erstellen und dem Layout hinzufügen
        self.graph = Graph()
        self.graph_layout.addItem(self.graph)

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

        # Thread für den Import erstellen und starten
        self.import_thread = threading.Thread(target=self.import_data)
        self.import_thread.start()

    def suchen_clicked(self):
        datum = self.calendar.selectedDate().toString("yyyy-MM-dd")
        try:
            log.writelog("Datum ausgewählt: " + datum)
        except Exception as e:
            print("Fehler beim Schreiben in die Log-Datei:", e)
        x = SQL_Select.SELECT(datum,self.Combo_Box.currentText(),'DATUM')
        y = SQL_Select.SELECT(datum,self.Combo_Box.currentText(),'WERT')
        #download.checkdate(datum)
        self.graph.plot(x,y)

    def import_data(self):
        conn = sqlite3.connect("sensor-data.db")
        c = conn.cursor()
        SQL_Import.importtoDB(c,conn)
    def download_data(self):
        conn = sqlite3.connect("sensor-data.db")
        c = conn.cursor()
        download.download_days(download.getdays(c,conn))

# Klasse für die Graphik
class Graph(QFrame):
    def __init__(self):
        super().__init__()
        plt.style.use('ggplot')
        plt.axis('scaled')
        plt.xlabel("Pollution")
        plt.ylabel("Time")
        plt.title("Pollution Data")
        #x = SQL_Select.SELECT(datum,self.Combo_Box.currentText(),'DATUM')
        #y = SQL_Select.SELECT(datum,self.Combo_Box.currentText(),'WERT')
        plt.plot(x,y)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self,x,y):
        self.axes.clear()
        self.axes.plot([x,y])
        self.canvas.draw()
    def getFigure(self):
        return self.figure
    def draw(self):
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())
         
