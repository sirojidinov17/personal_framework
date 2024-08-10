# server.py

from main import Main, AuthMiddleware
from route import app

# Middleware bilan `app`ni o'ralash
app_with_middleware = AuthMiddleware(app)

def wsgi_app(environ, start_response):
    return app_with_middleware(environ, start_response)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8000, wsgi_app)
    print("Serving on http://localhost:8000")
    server.serve_forever()
