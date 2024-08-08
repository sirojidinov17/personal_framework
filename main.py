from wsgiref.simple_server import make_server


class Main:
    def __init__(self):
        self.routes={}
    

    def route(self,path):
        def wrapper(handler):
            self.routes[path]=handler
            return handler
        return wrapper
    def __call__(self, environ, start_response):
        path=environ['PATH_INFO']
        method=environ['REQUEST_METHOD']
        handler=self.routes.get(path)
        if handler:
                status, headers,response=handler(environ)
        else:
            status, headers, response='404 Not Found', [('Content-Type', 'text/plain')], b'Not Found'
        start_response(status, headers)
        return [response]
def render_template(template_name, context=None):
    context =context or {}
    with open(template_name, 'r', encoding='utf-8') as template_file:
        template= template_file.read()
        return template.format(**context).encode('utf-8') 


app=Main()




if __name__=='__main__':
    server=make_server('localhost', 8000, app)
    print("Serving on http://localhost:8000")
    server.serve_forever()