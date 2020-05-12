import os
import sys
import socket
import pickle
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self, port):
        super().__init__()
        uic.loadUi(f'{os.path.dirname(os.path.abspath(__file__))}/main.ui', self)
        self.port = port
        self.initUI()
    
    def initUI(self):
        self.pushButton.clicked.connect(self.send)
        self.setWindowTitle('Sender')  
        self.setFixedSize(self.size())
    
    def send(self, data):
        title = self.title.text()
        text = self.text.toPlainText()
        mark = ''

        if self.radioButton.isChecked():
            mark = 'olymps'
        elif self.radioButton_2.isChecked():
            mark = 'motivation'
        elif self.radioButton_3.isChecked():
            mark = 'materials'
        elif self.radioButton_4.isChecked():
            mark = 'humor'

        if title == '' or text == '' or mark == '':
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Проверьте, что вы заполнили все поля. Ачччкошники. И заполнили корректно.", QtWidgets.QMessageBox.Ok)
            return
        
        sock = socket.socket()
        sock.connect(('localhost', self.port))

        sock.send(pickle.dumps((title, text, mark)))
        link = sock.recv(1024)
        self.link.setText(link.decode('utf-8'))
        sock.close()


app = QApplication(sys.argv)
ex = MyWidget(int(input('Введите порт: ')))
ex.show()
sys.exit(app.exec_())
