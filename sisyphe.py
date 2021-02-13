import http.server
import socketserver
from http import HTTPStatus
import os
import mimetypes
import json
import csv

PORT = 8003

class Sisyphe:
    """Sisyphe: contains the data labelling logic.

    This class has a few methods that enable the request handler to interact
    with the data.
    """
    
    def __init__(self,
                 features,
                 categories,
                 logfile,
                 save_callback=lambda x: x,
                 render_callback=lambda x: x,
                 resume=True,
                 multilabel=False,
                 model=None,
                 sep='\t',
                 label_sep='|'):
        """The Sisyphe constructor.

        Args:
            features (dict): A dictionnary that maps ids to example objects.
            categories (:obj:`list` of :obj:`str`): A list of all possible 
                categories as strings.
            logfile (str): File where the labels will be logged, line by line and
                a tab separates the id and the label string.
            save_callback (function): A callback that takes the label dictionnary
                as a parameter and saves it in a user-defined way.
            render_callback (function): A callback that takes the example object
                and returns an html string that will be displayed in the UI.
            resume (bool): Remove the ids that are present in the `logfile` to
                continue the work from where it was stopped.
            multilabel (bool): Informs whether multiple labels are allowed.
            model (obj): An online prediction model that has `predict` and
                `update` methods and understands the example objects and labels.
            sep (str): A string to separate the id and the label in the log file.
            label_sep (str): String to separate the labels if `multilabel` is set
                to `True`.

        """
        self.model = model
        self.multilabel = multilabel
        self.categories = categories
        self.save_callback = save_callback
        self.render_callback = render_callback
        self.features = features
        self.logfile = logfile
        self.sep = sep
        self.label_sep = label_sep
        
        self.labels = {}
        self.todo = set(features)
        
        key_type = type(next(iter(self.todo)))
        
        if resume:
            with open(logfile, newline='') as csvfile:
                previous = csv.reader(csvfile, delimiter=sep)
                for row in previous:
                    try:
                        self.todo.discard(key_type(row[0]))
                    except (TypeError, ValueError, KeyError) as e:
                        raise ValueError("This exception was " + \
        "caused by the fact that the index from `logfile` could " + \
        "not be cast to the type of keys from `features`. Either " + \
        "pass `resume=False`, check that the identifier types are " + \
        "consistent or check that there is no header line in the " + \
        "`logfile`.") from e

    def update(self, identificator, label):
        self.labels[identificator] = label
        self.todo.discard(identificator)
        if self.model:
            self.model.update(self.features[identificator], label)
        with open(self.logfile, 'a') as f:
            f.write(f"{identificator}{self.sep}{label.replace(os.linesep, '')}" + '\n')

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
        return len(self.features), len(self.todo)
    
    def description(self):
        return {'categories': self.categories,
                'multilabel': self.multilabel,
                'labelsep': self.label_sep}
        

def create_handler(sisyphe):
    
    class SisypheRequestHandler(http.server.BaseHTTPRequestHandler):
    
        def do_GET(self):
            if self.path == '/':
                self.return_file('frontend/index.html')
            elif self.path == '/style.css':
                self.return_file('frontend/style.css')
            elif self.path == '/main.js':
                self.return_file('frontend/main.js')
            elif self.path == '/NotoMono-Regular.ttf':
                self.return_file('frontend/NotoMono-Regular.ttf')
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
            obj_str = json.dumps(obj).replace('NaN', 'null').encode('utf8')
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
