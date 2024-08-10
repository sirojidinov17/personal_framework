from jinja2 import Environment, FileSystemLoader
from typing import Any
from wsgiref.simple_server import make_server
import os

env = Environment(loader=FileSystemLoader('template'))

def render_template(template_name, context=None):
    context = context or {}
    template = env.get_template(template_name)
    return template.render(context).encode('utf-8')

class Main:
    def __init__(self):
        self.routes = {}
        self.static_folder = 'static'  # Statik fayllar joylashgan papka

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        
        if path.startswith('/static/'):
            # Statik fayllarni xizmat qilish
            return self.serve_static_file(environ, start_response)

        handler = self.routes.get(path)
        if handler:
            status, headers, response = handler(environ)
        else:
            status, headers, response = '404 Not Found', [('Content-Type', 'text/plain')], b'Not Found'
        
        start_response(status, headers)
        return [response]

    def serve_static_file(self, environ, start_response):
        path = environ['PATH_INFO']
        file_path = os.path.join(self.static_folder, path.lstrip('/'))
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            status = '200 OK'
            headers = [('Content-Type', self.get_content_type(file_path))]
            start_response(status, headers)
            return [content]
        else:
            status = '404 Not Found'
            headers = [('Content-Type', 'text/plain')]
            start_response(status, headers)
            return [b'Not Found']

    def get_content_type(self, file_path):
        ext = os.path.splitext(file_path)[1]
        if ext == '.css':
            return 'text/css'
        elif ext == '.js':
            return 'application/javascript'
        elif ext in ('.png', '.jpg', '.jpeg', '.gif'):
            return 'image/' + ext[1:]
        else:
            return 'application/octet-stream'

app = Main()

class AuthMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if not self.is_authenticated(environ):
            status = '403 Forbidden'
            headers = [('Content-Type', 'text/plain')]
            response = b'Forbidden'
            start_response(status, headers)
            return [response]
        return self.app(environ, start_response)

    def is_authenticated(self, environ):
        # Misol uchun: HTTP_AUTHORIZATION sarlavhasida 'valid_token' mavjudligini tekshiradi
        return environ.get('HTTP_AUTHORIZATION') == 'valid_token'
