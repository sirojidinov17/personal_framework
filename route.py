from main import *
import cgi

import sqlite3
db=sqlite3.connect('db.db')


cursor=db.cursor()

cursor.execute('SELECT * FROM USER')


info=cursor.fetchall()

@app.route('/')
def index(environ):
    if environ['REQUEST_METHOD'] == 'GET':
        response_body = render_template('./template/index.html')
        return '200 OK', [('Content-Type', 'text/html; charset=utf-8')], response_body

@app.route('/info')
def info(environ):
    if environ['REQUEST_METHOD'] == 'POST':
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ, keep_blank_values=True)
        name = form.getvalue('name', 'No Name Provided')
        lastname = form.getvalue('lastname', 'No Latname Provided')

        # Ma'lumotlarni ma'lumotlar bazasiga qo'shish
        cursor.execute('''INSERT INTO USER (name, lastname) VALUES (?, ?)''', (name, lastname))
        db.commit()  # O'zgarishlarni saqlash

    # Ma'lumotlarni olish va render qilish
    cursor.execute('SELECT * FROM USER')
    info = cursor.fetchall()
    response_body = render_template('./template/allinfo.html', {'info': info})
    return '200 OK', [('Content-Type', 'text/html; charset=utf-8')], response_body

if __name__ == '__main__':
    server = make_server("localhost", 8000, app)
    print("Serving on http://localhost:8000")
    server.serve_forever()
db.close()