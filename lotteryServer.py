from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import simplejson
import random
import json

from sklearn import tree
import pandas as pd

class S(BaseHTTPRequestHandler):
    data = pd.read_csv('thLotto_49-59.csv')
    day = list(zip(data['day'],data['month'],data['year']))
    first = data['first']
    digit3 = data['3digit']
    last_2digit_top = data['last_2digit_top']
    first_3digit_1 = data['first_3digit_1']
    first_3digit_2 = data['first_3digit_2']
    last_3digit_1 = data['last_3digit_1']
    last_3digit_2 = data['last_3digit_2']
    last_2digit_down = data['last_2digit_down']
    iD = int(16)
    iM = int(04)
    iY = int(2014)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        message_parts = {
            "first":"%s"% perdictLotto(self.iD,self.iM,self.iY,self.day,self.first),
            "tree":"%s"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.digit3),
            "first_tree1":"%s"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.first_3digit_1),
            "first_tree2":"%s"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.first_3digit_2),
            "last_tree1":"%s"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.last_3digit_1),
            "last_tree2":"%s"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.last_3digit_2),
            "two_1":"%s"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.last_2digit_top),
            "two_2":"%s"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.last_2digit_down)
        }
        
        #print("\nFirst: %.0f"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.first))
        #print("Three digit: %.0f"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.digit3))
        #print("The first three digits: %.0f"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.first_3digit_1))
        #print("                        %.0f"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.first_3digit_2))

        #print("The last three digits:  %.0f"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.last_3digit_1))
        #print("                        %.0f"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.last_3digit_2))
        #print("Two digits:    %.0f"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.last_2digit_top))
        #print("               %.0f"%perdictLotto(self.iD,self.iM,self.iY,self.day,self.last_2digit_down))
      
        json_string = json.dumps(message_parts)
        self.wfile.write(json_string)
        self.end_headers()
        #self.send_response(200)

def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

def perdictLotto(d,m,y,data1,data2):
    classifier = tree.DecisionTreeClassifier()
    classifier.fit(data1,data2)
    return classifier.predict([[d,m,y]])[0]
	

if __name__ == "__main__":
    from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()