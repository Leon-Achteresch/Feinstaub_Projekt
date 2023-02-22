import sys
from PyQt6.QtWidgets import QApplication, QWidget,QLabel, QLineEdit, QVBoxLayout, QPushButton, QDateTimeEdit, QCalendarWidget
from PyQt6.QtCore import Qt

class MyForm(QWidget):
    def __init__(self):
        super().__init__()

        # Fenster-Layout erstellen
        self.layout = QVBoxLayout()

        # Label erstellen
        self.label = QLabel("Name:")
        self.layout.addWidget(self.label)

        # Textfeld erstellen
        self.textbox = QLineEdit()
        self.layout.addWidget(self.textbox)

        # Button erstellen
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.submit_clicked)
        self.layout.addWidget(self.button)

        self.calendar = QCalendarWidget()
        self.layout.addWidget(self.calendar)

        self.setLayout(self.layout)

    def submit_clicked(self):
        name = self.textbox.text()
        print("Hello,", name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())
