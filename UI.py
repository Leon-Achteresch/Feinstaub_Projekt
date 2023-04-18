import sys
from PyQt6.QtWidgets import QApplication, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCalendarWidget, QLabel, QFrame, QProgressBar,QGraphicsDropShadowEffect
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6.QtGui import QFont, QIcon, QColor
from PyQt6.QtWidgets import QProgressBar
import log
import sqlite3
import threading
import download
import SQL
#import SQL_Select
from pyqtgraph import PlotWidget, AxisItem
from datetime import datetime, timedelta
import pyqtgraph as pg

conn2 = sqlite3.connect("sensor-data.db")
c2 = conn2.cursor()

class MyForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('assets\images\hippie-marijuana-weed.svg'))
        self.setWindowTitle("Feinstaub Projekt")
        
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(10)
        shadow_effect.setColor(QColor(0, 0, 0, 80))
        shadow_effect.setOffset(0, 0)
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
        self.calendar.setGraphicsEffect(shadow_effect)
        self.calendar.setStyleSheet("QCalendarWidget {"
                             "  border: none;"
                             "  font-family: 'Roboto', sans-serif;"
                             "  font-size: 16px;"
                             "  border-radius: 10px;"
                             "}"
                             ""
                             "QCalendarWidget QAbstractItemView {"
                             "  selection-background-color: #db1414;"
                             "  background-color: #fff;"
                             "  border: none;"
                             "  border-radius: 10px;"
                             "  color: #333;"
                             "}"
                             "")

        left_layout.addWidget(self.calendar)

        # Button für Suche erstellen
        self.button = QPushButton("Suche")
        self.button.clicked.connect(self.suchen_clicked)
        self.button.setGraphicsEffect(shadow_effect)
        self.button.setStyleSheet(""
        " QPushButton {"
        "  background-color: #2f80ed;"
        "  border-radius: 10px;"
        "  color: #fff;"
        "  height: 50px;"
        "  line-height: 1.5;"
        "  outline: none;"
        "  vertical-align: top;"
        "  font-size: 16px;"
        "  font-family: 'Roboto', sans-serif;"
        "  white-space: nowrap;"
        "}"
        ""
        "  QPushButton:hover {"
        "    background-color: #3b8cf3;"
        "  }"
        "  QPushButton:pressed {"
        "    background-color: #2567c9;"
        "  }"
        "")
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
        self.Combo_Box.setGraphicsEffect(shadow_effect)
        self.Combo_Box.addItem("Temperatur")
        self.Combo_Box.addItem("Luftfeuchtigkeit")
        self.Combo_Box.addItem("P1")
        self.Combo_Box.addItem("P2")
        self.Combo_Box.addItem("Gesamt")
        self.Combo_Box.setItemIcon(0, QIcon("assets\images\interface-weather-temperature-hot.png"))
        self.Combo_Box.setItemIcon(1, QIcon("assets\images\interface-weather-wind.png"))
        self.Combo_Box.setItemIcon(2, QIcon("assets\images\interface-weather-rain-drop.png"))
        self.Combo_Box.setItemIcon(3, QIcon("assets\images\co2-icon.svg"))
        self.Combo_Box.setItemIcon(4, QIcon("assets\images\hippie-marijuana-weed.svg"))
        self.Combo_Box.setStyleSheet("QComboBox {\n"
        "  background-color: #FFFFFF;\n"
        "  border: 1px solid #CCCCCC;\n"
        "  border-radius: 3px;\n"
        "  padding: 5px;\n"
        "  min-width: 6em;\n"
        "  font-size: 14px;\n"
        "}\n"
        "\n"
        "QComboBox::drop-down {\n"
        "  subcontrol-origin: padding;\n"
        "  subcontrol-position: top right;\n"
        "  width: 15px;\n"
        "  border-left-width: 1px;\n"
        "  border-left-color: #CCCCCC;\n"
        "  border-left-style: solid;\n"
        "  border-top-right-radius: 3px;\n"
        "  border-bottom-right-radius: 3px;\n"
        "  background-color: #FFFFFF;\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow {\n"
        "  image: url('assets/images/interface-arrows-button-down.png');\n"
        "  width: 14px;\n"
        "  height: 14px;\n"
        "  padding-right: 1px;\n"
        "}\n"
        "")
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
        selected_value = self.Combo_Box.currentText()
        if selected_value == 'Temperatur':
            selected_value='temp'
        elif selected_value == 'Luftfeuchtigkeit':
            selected_value='feuchtigkeit'
        elif selected_value == 'Gesamt':
            selected_value='feuchtigkeit'

        try:
            log.writelog("Datum ausgewählt: " + datum, selected_value)
        except Exception as e:
            print("Fehler beim Schreiben in die Log-Datei:", e)
        x = SQL.SELECT(datum, selected_value, 'DATUM')
        y = SQL.SELECT(datum, selected_value, 'WERT')
        if not x or not y:
            print("Die Listen sind leer.")
        else:
            self.line_graph.plot(x, y)
            
    def download_data(self):
        conn = sqlite3.connect("sensor-data.db")
        c = conn.cursor()
        days_to_download = download.getdays(c, conn)
        if days_to_download == 0: 
            self.label.hide()
        else:
            self.label.setText("Download Data...")
            download.download_days(0)
            SQL.importtoDB(c, conn, self.label)
            
class LineGraph(PlotWidget):
    def __init__(self, parent=None):
        super(LineGraph, self).__init__(parent)

    def plot(self, x, y):
        self.clear()
        
        axis = pg.AxisItem(orientation='bottom')
        tick_values = []
        tick_labels = []
        time_format = '%H:%M:%S'
        for timestamp in x:
            dt = datetime.strptime(timestamp, time_format)
            tick_values.append((dt - datetime(dt.year, dt.month, dt.day)).total_seconds())
            tick_labels.append(dt.strftime('%H:%M'))
        axis.setTicks([list(zip(tick_values, tick_labels))])
        self.setAxisItems({'bottom': axis})

        x = tick_values
        #self.plotItem.setDownsampling(mode='peak')
        #self.plotItem.setClipToView(True)
        self.plotItem.plot(x, y, fillLevel=(True))
        self.plotItem.vb.setLimits(xMin=min(x)-5, xMax=max(x)+5, yMin=min(y)-5, yMax=max(y)+5)
        self.setTitle('Sensor Data')

    def clear(self):
        self.plotItem.clear()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())
         

