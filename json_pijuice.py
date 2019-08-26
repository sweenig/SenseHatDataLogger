from http.server import HTTPServer, BaseHTTPRequestHandler
from time import time,sleep
from json import dumps
from pijuice import PiJuice

server_port = 8485

enum_input_status = {
  "NOT_PRESENT": 0,
  "BAD": 1,
  "WEAK": 2,
  "PRESENT": 3
}
enum_battery_status = {
  "NORMAL": 0,
  "CHARGING_FROM_IN": 1,
  "CHARGING_FROM_5V_IO": 2,
  "NOT_PRESENT": 3
}

pijuice = PiJuice(1, 0x14)

def getData():
  status = pijuice.status.GetStatus()['data']
  charge = pijuice.status.GetChargeLevel()['data']
  print(f"Status:\n{status}\nCharge: {charge}")
  if status is not None and charge is not None:
    json_dict = status
    json_dict['battery_status'] = enum_battery_status[status['battery']]
    json_dict['power_input_status'] = enum_input_status[status['powerInput']]
    json_dict['5v_power_input_status'] = enum_input_status[status['powerInput5vIo']]
    json_dict['last_updated'] = time()
    json_dict['bat_charge'] = charge
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

httpd = HTTPServer(('',server_port), S)
print(f"Starting web server on {server_port}")
print(f"Testing sensors{dumps(getData())}")
httpd.serve_forever()
