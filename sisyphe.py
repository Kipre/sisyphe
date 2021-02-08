import http.server
import socketserver
from http import HTTPStatus
import os
import mimetypes
import json
import pandas as pd
import numpy as np

PORT = 8003

class Sisyphe:
    
    def __init__(self, 
                 filename, 
                 categories,
                 render):
        self.filename = filename
        self.categories = categories
        self.render = render
        self.id = -1
        self.df = pd.read_csv(filename, index_col=0)
        if 'label' not in self.df.columns:
            self.df['label'] = np.nan
        self.todo = set(self.df[self.df['label'].isna()].index)
        self.precedent = None

    def update(self, id, label):
        self.df[id]['label'] = label;
        self.df.to_csv(filename)
    
    def element(self):
        if self.precedent:
            return {'id': self.precedent,
                    'example': self.render(self.df.loc[self.precedent]),
                    'progress': self.progress()}
        else:
            raise ValueError('no element available')

    def progress(self):
        return 1 - len(self.todo) - len(self.df.index)

    def next(self):
        self.precedent = self.todo.pop()
        return self.element()
        
    
    def description(self):
        return {'title': self.filename,
                'categories': [{'name': cat[0], 'label': cat[1]} for cat in self.categories]}

def create_handler(sisyphe):
    
    class SisypheRequestHandler(http.server.BaseHTTPRequestHandler):
    
        def do_GET(self):
            if self.path == '/':
                self.return_file('frontend/index.html')
            elif self.path == '/style.css':
                self.return_file('frontend/style.css')
            elif self.path == '/main.js':
                self.return_file('frontend/main.js')
            elif self.path == '/job':
                self.return_object(sisyphe.description())
            elif self.path == '/next':
                self.return_object(sisyphe.next())
            else:
                print("path not registered", self.path)
    
        def do_POST(self):
            print(self.path, dir(self));
        
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
            
    return SisypheRequestHandler


def run(sisyphe):
    with socketserver.TCPServer(("", PORT), create_handler(sisyphe)) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
