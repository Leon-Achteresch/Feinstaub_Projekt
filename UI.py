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
        
        #self.setStyleSheet("background-color: #C0FDFF;")

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(10)
        shadow_effect.setColor(QColor(0, 0, 0, 80))
        shadow_effect.setOffset(0, 0)
        
        self.oben = QHBoxLayout()
        self.unten = QHBoxLayout()


        self.layout = QVBoxLayout()

        # Linkes Layout erstellen
        left_layout = QVBoxLayout()
        #left_layout1 = QVBoxLayout()
        # Label für den Kalender erstellen
        self.label = QLabel("Wähle ein Datum:")
        self.label.setStyleSheet("Color: #EE4540")
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
                                    "  color: black;"
                                    "  border-radius: 20px;"
                                    "}"
                                    "QCalendarWidget QAbstractItemView:enabled {"#Grid
                                    "  selection-background-color: #db1414;"
                                    "  background-color: #ffffff;"
                                    "  border: none;"
                                    "  color: black;"
                                    "  border-radius: 10px;"
                                    "}"
                                    "#qt_calendar_navigationbar"
                                    "{"
                                    "background-color: #00396c;"
                                    " border-radius: 10px;"
                                    " color: black;"
                                    "}"
                                    "#qt_calendar_prevmonth {"
                                    "  background-color: transparent;"
                                    "  icon-size: 30px;"
                                    "  margin-left: 5px;"
                                    "  border-radius: 20px;"
                                    "  qproperty-icon: url(assets/images/interface-arrows-button-left.svg);"
                                    "}"
                                    "#qt_calendar_nextmonth {"
                                    "  background-color: transparent;"
                                    "  icon-size: 30px;"
                                    "   margin-right: 5px;"
                                    "  border-radius: 20px;"
                                    "  qproperty-icon: url(assets/images/interface-arrows-button-right.svg);"
                                    "}"
                                    """#QSpinBox {
                                    color: black;
                                    selection-background-color: black;
  	                                selection-color: black;
                                    }"""
                             "")

        left_layout.addWidget(self.calendar)

        # Button für Suche erstellen
        self.button = QPushButton("Suche")
        self.button.clicked.connect(self.suchen_clicked)
        self.button.setGraphicsEffect(shadow_effect)
        self.button.setStyleSheet(
            "QPushButton {"
            "  border-radius: 10px;"
            "  color: #fff;"
            "  height: 50px;"
            "  line-height: 1.5;"
            "  outline: none;"
            "  vertical-align: top;"
            "  font-size: 16px;"
            "  font-family: 'Roboto', sans-serif;"
            "  white-space: nowrap;"
            "  background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,"
            "    stop: 0 #ff8a00, stop: 1 #e52e71);"
            "}"
            ""
            "QPushButton:hover {"
            "  background-color: #3b8cf3;"
            "}"
            ""
            "QPushButton:pressed {"
            "  background-color: #2567c9;"
            "}"
        )

        left_layout.addWidget(self.button)

        #Frame erstellen
        self.frame = QFrame()
        #self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self.frame.setStyleSheet("QFrame{background-color: #2D142C; border: 0px solid black; border-radius: 20px;}")
        self.frame.setLineWidth(3)
        
        self.frame.setLayout(left_layout)
        self.oben.addWidget(self.frame)

        self.frame4 = QFrame()
        self.frame4.setFrameStyle(QFrame.Shape.StyledPanel)
        self.frame4.setStyleSheet("QFrame{background-color: #2D142C; border: 0px solid black; border-radius: 20px;}")
        self.frame4.setLineWidth(3)
        
        self.frame4.setLayout(left_layout)
        self.oben.addWidget(self.frame4)

        unten_layout = QVBoxLayout()
        unten_layout1 = QVBoxLayout()
        

        # Rechtes Layout erstellen
        right_layout = QVBoxLayout()

        self.labelInfo = QLabel("Aktualisiere Daten")
        font = QFont("Roboto", 10)
        self.labelInfo.setStyleSheet("Color: #EE4540")
        self.labelInfo.setFont(font)
        unten_layout.addWidget(self.labelInfo)




        # Grafik-Layout erstellen
        self.graph_layout = QVBoxLayout()

        # ScatterGraph-Klasse erstellen und dem Layout hinzufügen
        self.line_graph = LineGraph()
        self.line_graph.setBackground('transparent')
        self.graph_layout.addWidget(self.line_graph)

        self.Combo_Box = QComboBox()
        self.Combo_Box.setGraphicsEffect(shadow_effect)
        self.Combo_Box.addItem("Temperatur")
        self.Combo_Box.addItem("Luftfeuchtigkeit")
        self.Combo_Box.addItem("P1")
        self.Combo_Box.addItem("P2")
        self.Combo_Box.setItemIcon(0, QIcon("assets\images\interface-weather-temperature-hot.png"))
        self.Combo_Box.setItemIcon(1, QIcon("assets\images\interface-weather-wind.png"))
        self.Combo_Box.setItemIcon(2, QIcon("assets\images\interface-weather-rain-drop.png"))
        self.Combo_Box.setItemIcon(3, QIcon("assets\images\co2-icon.svg"))
        self.Combo_Box.setStyleSheet("QComboBox {\n"
        "  background-color: #FFFFFF;\n"
        "  border: 1px solid #CCCCCC;\n"
        "  border-radius: 3px;\n"
        "  padding: 5px;\n"
        "  margin: 10px;\n"
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
        "  border-top-right-radius: 30px;\n"
        "  border-bottom-right-radius: 30px;\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow {\n"
        "  image: url('assets/images/interface-arrows-button-down.png');\n"
        "  width: 10px;\n"
        "  height: 10px;\n"
        "  margin: 10px;\n"
        "  padding-right: 1px;\n"
        "}\n"
        "QComboBox QAbstractItemView {"
        "background-color: white;"
        "}"
        "")
        right_layout.addWidget(self.Combo_Box)
        
        # Grafik-Layout zum rechten Layout hinzufügen
        right_layout.addLayout(self.graph_layout)

        
        self.WerteLBL = QLabel("")
        self.WerteLBL.setStyleSheet("Color: #EE4540")
        
        unten_layout1.addWidget(self.WerteLBL)
        
        self.oben.addSpacing(25)

        # Rechtes Layout zur Gesamt-LayoutBox hinzufügen
        self.frame1 = QFrame()
        #self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame1.setFrameStyle(QFrame.Shape.StyledPanel)
        self.frame1.setStyleSheet("QFrame{background-color: #2D142C; border: 0px solid black; border-radius: 20px;}")
        self.frame1.setLineWidth(3)
       
        self.frame1.setLayout(right_layout)
        self.oben.addWidget(self.frame1)

        self.layout.addLayout(self.oben)

        self.frame2 = QFrame()
        
        self.frame2.setFrameStyle(QFrame.Shape.StyledPanel)
        self.frame2.setStyleSheet("QFrame{background-color: #2D142C; border: 0px solid black; border-radius: 10px;margin-left:20px}")
        self.frame2.setFixedWidth(200)
       
        self.frame2.setLayout(unten_layout)
        self.unten.addWidget(self.frame2)

        self.frame3 = QFrame()
        self.frame3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame3.setStyleSheet("QFrame{background-color: #2D142C; border-radius: 10px;}")
        self.frame3.setLineWidth(3)

        self.frame3.setLayout(unten_layout1)
        self.unten.addWidget(self.frame3)

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

        try:
            log.writelog("Datum ausgewählt: " + datum, selected_value)
        except Exception as e:
            print("Fehler beim Schreiben in die Log-Datei:", e)
        x = SQL.SELECT(datum, selected_value, 'DATUM')
        y = SQL.SELECT(datum, selected_value, 'WERT')
        
        # Durchschnittswerte etc hinzufügen
        List = SQL.sql_min(datum,selected_value)
        self.WerteLBL.setText('Minimum: ' + str(List[0]) + ' Maximum: ' + str(List[1]) + ' Durchschnitt: ' + str(List[2]))
        
        if not x or not y:
            self.labelInfo.setText("Die Listen sind leer.")
            self.line_graph.plot(0, 0, selected_value)  
        else:
            self.line_graph.plot(x, y, selected_value)
            self.labelInfo.setText("")
            
    def download_data(self):
        conn = sqlite3.connect("sensor-data.db")
        c = conn.cursor()
        days_to_download = download.getdays(c, conn)
        
        if days_to_download == 1: 
            self.labelInfo.setText('')
        else:
            self.labelInfo.setText("Download Data...")
            download.download_days(0)
            SQL.importtoDB(c, conn, self.labelInfo)
            
class LineGraph(PlotWidget):
    def __init__(self, parent=None):
        super(LineGraph, self).__init__(parent)

    def plot(self, x, y, selected_value):
        self.clear()
        try:
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
            self.plotItem.setLabel('left',selected_value)
            self.plotItem.setLabel('bottom','Uhrzeit')
           # axis.setTickSpacing(1000000,1,1)
            x = tick_values
            self.plotItem.plot(x, y, fillLevel=(True))
            if min(y)>0:
                self.plotItem.vb.setLimits(xMin=min(x)-5, xMax=max(x)+5, yMin=0, yMax=max(y)+5)
            else:
               self.plotItem.vb.setLimits(xMin=min(x)-5, xMax=max(x)+5, yMin=min(y)-5, yMax=max(y)+5) 
            self.setTitle('Sensor Data')
        except Exception as e:
            self.label.setText(e)
        

    def clear(self):
        self.plotItem.clear()
        
if __name__ == '__main__':
    
    #Installiert alle nicht vorhandenen Packages
    download.install_packages('requirements.txt')

    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())
         

