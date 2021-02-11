import http.server
import socketserver
from http import HTTPStatus
import os
import mimetypes
import json

PORT = 8003

class Sisyphe:
    """Labelizer logic
    
    param: features (dict) a mapping of ids to features
    
    """
    
    def __init__(self,
                 features,
                 categories,
                 save_callback=lambda x: x,
                 render_callback=lambda x: x,
                 multilabel=False,
                 model=None):
        self.model = model
        self.multilabel = multilabel
        self.categories = categories
        self.save_callback = save_callback
        
        self.features = features
        self.labels = {}
        self.todo = set(features)

    def update(self, identificator, label):
        self.labels[identificator] = label
        self.todo.discard(identificator)
        if self.model:
            self.model.update(self.features[identificator], label)

    def save(self):
        self.save_callback(self.labels)
    
    def get(self, identificator=None):
        if identificator == None:
            identificator = next(iter(self.todo))
        result = {'id': identificator,
                  'example': self.render_callback(self.features[identificator]),
                  'progress': self.progress()}
        if self.model:
            result['probabilities'] = self.model.predict(self.features[identificator])
        return result

    def progress(self):
        return len(features), len(todo)
    
    def description(self):
        return {'categories': self.categories,
                'multilabel': self.multilabel}
        

def create_handler(sisyphe):
    
    class SisypheRequestHandler(http.server.BaseHTTPRequestHandler):
    
        def do_GET(self):
            if self.path == '/':
                self.return_file('frontend/index.html')
            elif self.path == '/style.css':
                self.return_file('frontend/style.css')
            elif self.path == '/main.js':
                self.return_file('frontend/main.js')
            elif self.path == '/save':
                sisyphe.save()
                self.return_object({'saved': True})
            elif self.path == '/job':
                self.return_object(sisyphe.description())
            elif '/example' in self.path:
                head, tail = os.path.split(self.path)
                if tail == 'example':
                    self.return_object(sisyphe.get())
                else:
                    example = sisyphe.get(int(tail))
                    self.return_object(example)
            else:
                print("path not registered", self.path)
    
        def do_POST(self):
            if self.path == '/label':
                obj = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                sisyphe.update(obj['id'], obj['label'])
                self.success()
            else:
                raise ValueError('unknown path {self.path}')
                
        
        def success(self):
            self.send_response_only(HTTPStatus.OK)
            self.send_header("Content-type", 'text/plain')
            self.send_header("Content-Length", '6')
            self.end_headers()
            self.wfile.write(b'thanks')
        
        
        def fail(self, message):
            message = message.encode('utf8')
            self.send_response_only(HTTPStatus.NOT_ACCEPTABLE)
            self.send_header("Content-type", 'text/plain')
            self.send_header("Content-Length", len(message))
            self.end_headers()
            self.wfile.write(message)
        
        def return_file(self, file):
            f = open(file, 'rb')
            fs = os.fstat(f.fileno())
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", mimetypes.guess_type(file)[0])
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
    
        def return_object(self, obj):
            obj_str = json.dumps(obj).encode('utf8')
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", 'application/json')
            self.send_header("Content-Length", str(len(obj_str)))
            self.end_headers()
            self.wfile.write(obj_str)

        def return_error(self, message):
            self.send_response(HTTPStatus.NOT_OK)
            self.send_header("Content-type", 'text/plain')
            self.send_header("Content-Length", str(len(message)))
            self.end_headers()
            self.wfile.write(message)
            
    return SisypheRequestHandler


def run(sisyphe):
    with socketserver.TCPServer(("", PORT), create_handler(sisyphe)) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
