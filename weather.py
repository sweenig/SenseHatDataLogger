from http.server import HTTPServer, BaseHTTPRequestHandler
import Adafruit_DHT
from time import time,sleep

dht22 = Adafruit_DHT.DHT22

def getData():
  json_dict = {}
  h, t1 = Adafruit_DHT.read_retry(dht22, 4)
  if h is not None and t1 is not None:
    json_dict['humidity'] = h
    json_dict['t1'] = t
    json_dict['last_updated'] = time.time()
    return json_dict
  else:
    sleep(0.5)
    return getData()

class S(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','application/json')
    self.end_headers()
    self.wfile.write(b'Hello world!')

httpd = HTTPServer(('',8000), S)
print("Starting web server on 8000")
httpd.serve_forever()
