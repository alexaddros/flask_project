import os
import sys
import socket
import pickle
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

    def send(self):
        title = self.title.text()
        text = self.text.toPlainText()
        sign = self.sign.text()

        if self.img_check.isChecked():
            img = self.img.text()
            self.connect_and_send(pickle.dumps((title, text, sign, img)))
        else:
            self.connect_and_send(pickle.dumps((title, text, sign)))
    
    def connect_and_send(self, data):
        sock = socket.socket()
        sock.connect(('localhost', self.port))
        sock.send(data)
        print(sock.recv(1024).decode('utf-8'))
        sock.close()


app = QApplication(sys.argv)
ex = MyWidget(int(input('Введите порт: ')))
ex.show()
sys.exit(app.exec_())
