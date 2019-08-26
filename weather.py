from http.server import HTTPServer, BaseHTTPRequestHandler
import Adafruit_DHT
from time import time,sleep
from json import dumps
from pijuice import PiJuice

dht22 = Adafruit_DHT.DHT22
pijuice = PiJuice(1, 0x14)

def getData():
  json_dict = {}
  h, t1 = Adafruit_DHT.read_retry(dht22, 4)
  charge = pijuice.status.GetChargeLevel()['data']
  if h is not None and t1 is not None and charge is not None:
    json_dict['humidity'] = h
    json_dict['temp'] = (t1*9/5)+32
    json_dict['last_updated'] = time()
    json_dict['bat_level'] = charge
    print(f"Fetched data {json_dict}")
    return json_dict
  else:
    print("Error fetching data, retrying...")
    sleep(0.5)
    return getData()

class S(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','application/json')
    self.end_headers()
    self.wfile.write(dumps(getData()).encode())

httpd = HTTPServer(('',8000), S)
print("Starting web server on 8000")
print(f"Testing sensors{dumps(getData())}")
httpd.serve_forever()
