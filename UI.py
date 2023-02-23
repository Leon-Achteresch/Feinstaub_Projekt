import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCalendarWidget, QLabel, QFrame
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6.QtGui import QFont
import log

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MyForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('tbs1.png'))
        self.setWindowTitle("Feinstaub Projekt")

        self.layout = QHBoxLayout()

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
        self.layout.addLayout(left_layout)

        # Rechtes Layout erstellen
        right_layout = QVBoxLayout()

        # Label für die Ausgabe erstellen
        self.ausgabe_label = QLabel("")
        right_layout.addWidget(self.ausgabe_label)

        # Grafik-Layout erstellen
        self.graph_layout = QVBoxLayout()

        # Graph-Klasse erstellen und dem Layout hinzufügen
        self.graph = Graph()
        self.graph_layout.addWidget(self.graph)

        # Grafik-Layout zum rechten Layout hinzufügen
        right_layout.addLayout(self.graph_layout)

        # Rechtes Layout zur Gesamt-LayoutBox hinzufügen
        self.layout.addLayout(right_layout)

        self.setLayout(self.layout)

    def suchen_clicked(self):
        datum = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.ausgabe_label.setText(f"Das ausgewählte Datum ist {datum}.")
        try:
            log.writelog("Datum ausgewählt: " + datum)
        except Exception as e:
            print("Fehler beim Schreiben in die Log-Datei:", e)
        self.graph.plot()


# Klasse für die Graphik
class Graph(QFrame):
    def __init__(self):
        super().__init__()

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self):
        x = [1, 2, 3, 4, 5]
        y = [3, 5, 2, 7, 1]
        self.axes.clear()
        self.axes.bar(x, y)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())
