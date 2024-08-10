from main import *
import cgi
from jinja2 import Environment, FileSystemLoader

import sqlite3
db=sqlite3.connect('db.db')
env = Environment(loader=FileSystemLoader('template'))


cursor=db.cursor()

cursor.execute('SELECT * FROM USER')
info=cursor.fetchall()
@app.route('/')
def index(environ):
    if environ['REQUEST_METHOD'] == 'GET':
        response_body = render_template('./view_template/index.html', {'title':"View"})
        return '200 OK', [('Content-Type', 'text/html; charset=utf-8')], response_body
    
@app.route('/info')
def info(environ):
    if environ['REQUEST_METHOD'] == 'GET':
        cursor.execute('SELECT * FROM USER')
        info = cursor.fetchall()
        response_body = render_template('./UserList.html', {'info': info,'title':"UserList"})
        return '200 OK', [('Content-Type', 'text/html; charset=utf-8')], response_body





if __name__ == '__main__':
    server = make_server('localhost', 8000, app)
    print("Serving on http://localhost:8000")
    server.serve_forever()



