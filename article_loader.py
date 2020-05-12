import os
import shutil
import socket
import pickle


def create_article(title, text, mark):
    global count

    with open('articles_count.txt') as count:
        count = count.read()
        print(count)

    statia = '\n\t\t<rtitle>{}</rtitle>\n\t\t<rtext><p>{}</p></rtext>\n'
    try:
        os.mkdir('articles/{}'.format(mark))
        os.mkdir('articles/{}/{}_{}'.format(mark, count, title))
        os.mkdir('articles/{}/{}_{}/static'.format(mark, count, title))
    except:
        try:
            os.mkdir('articles/{}/{}_{}'.format(mark, count, title))
            os.mkdir('articles/{}/{}_{}/static'.format(mark, count, title))
        except:
            pass

    with open('articles/{}/{}_{}/index.html'.format(mark, count, title), 'w') as state:
        with open('blueprint.html') as pattern:
            lines = pattern.readlines()
            for i, line in enumerate(lines):
                if line.strip() == '<!-- place -->':
                    lines.pop(lines.index(line))
                    insert_index = i
                    break
            lines.insert(insert_index, statia.format(title, text))
            state.writelines(lines)
    
    with open('articles/{}/{}_{}/style.css'.format(mark, count, title), 'w') as style:
         with open('style_blueprint.css') as pattern:
            lines = pattern.readlines()
            style.writelines(lines)

    for static_elem in os.listdir('static/'):
        shutil.copy('static/{}'.format(static_elem), 'articles/{}/{}_{}/static/{}'.format(mark, count, title, static_elem))

    os.remove('articles_count.txt')
    with open('articles_count.txt', 'w') as counter:
        counter.write(str(int(count) + 1))

    return int(count)

sock = socket.socket()
sock.bind(('localhost', int(input('Введите порт: '))))
sock.listen(1)

while True:
    conn, addr = sock.accept()
    data = pickle.loads(conn.recv(8096))
    title, text, mark = data
    count = create_article(title, text, mark)
    conn.send('articles/{}/{}_{}'.format(mark, count, title).encode('utf-8'))
    conn.close()
