#coding: utf-8
import os
import socket
import pickle

def load(title, text, link='', classificator=1, img=None):
    text_record = "\t<!-- record -->\n\t\n\t<div class='record-text'>\n\t\t<rtitle>{}</rtitle>\n\t\t<rtext>{}</rtext>\n\t\t<rlink>{}</rlink>\n\t</div>"

    img_record = "t<!-- record -->\n\t\n\t<div class='record-img'>\n\t\t<rtitle>{}</rtitle>\n\t\t<rtext>{}</rtext>\n\t\t<rimg><img src='{}'></rimg>\n\t\t<rlink>{}</rlink>\n\t</div>"

    if classificator == 1:
        data = text_record.format(title, text, link)
    else:
        data = img_record.format(title, text, img, link)

    with open('templates/news.html', 'r', encoding='utf-8') as source:
        lines = source.readlines()
        for i, line in enumerate(lines):
            if line.strip() == '<!-- record -->':
                insert_index = i
    
        lines.pop(insert_index)
        lines.insert(insert_index, data)

    os.remove('templates/news.html')
    with open('templates/news.html', 'w', encoding='utf-8') as result:
        result.writelines(lines)

sock = socket.socket()
sock.bind(('localhost', int(input('Введите порт: '))))
sock.listen(1)

while True:
    conn, addr = sock.accept()
    data = pickle.loads(conn.recv(8096))
    if len(data) == 3:
        title, text, link = data
        classificator = 1
        load(title, text, link, classificator)
    elif len(data) == 4:
        title, text, link, img = data
        classificator = 2
        load(title, text, link, classificator, img)

    conn.send("success".encode('utf-8'))
    conn.close()

sock.close()
