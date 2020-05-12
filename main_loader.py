#coding: utf-8
import os
import socket
import pickle

def load(data):
    img = pickle.loads(data)[0]
    mark = pickle.load(data)[1]
    with open('main/{}.jpg'.format(mark), 'wb') as target:
        target.writelines(img)

sock = socket.socket()
sock.bind(('localhost', int(input('Введите порт: '))))
sock.listen(1)

while True:
    conn, addr = sock.accept()
    name = str(conn.recv(1024)).split('\\')[0]

    with open('main/{}.jpg'.format(name), 'wb') as target:
        while True:
            data = conn.recv(1024)
            if 'end' not in str(data):
                target.write(data)
            else:
                break

    print('accepted')
    conn.close()

sock.close()
    