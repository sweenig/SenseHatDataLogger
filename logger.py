import argparse, json
parser = argparse.ArgumentParser(prog="Weather Station")
parser.add_argument('--version', action='version', version='%(prog)s 2.0')
parser.add_argument("username", help="Username on Adafruit.io", type=str)
parser.add_argument("key", help="AIO Key on Adafruit.io", type=str)
parser.add_argument("location", help="Location code", type=str, default="", nargs='?')
parser.add_argument("--notempH", help="Disable collection of the temperature via the humidity sensor", action="store_true")
parser.add_argument("--notempP", help="Disable collection of the temperature via the pressure sensor", action="store_true")
parser.add_argument("--nohumidity", help="Disable collection of the humidity.", action="store_true")
parser.add_argument("--nopressure", help="Disable collection of the pressure.", action="store_true")
parser.add_argument("-u","--unitofmeasure", help="Which unit to calculate temperature in (F or C)", choices=["F","C"], default="F")
parser.add_argument("-r","--rate", help="Number of seconds between data point collection.",default=300, type=int)
parser.add_argument("--noserver", help="Disable built in web server. If omitted, data will be served in json format on port 8000.", action="store_true")
args = parser.parse_args()
convert_to_F = True if args.unitofmeasure == "F" else False
if args.notempH and args.notempP and args.nohumidity and args.nopressure:
  print("No metrics configured for collection")
  parser.print_help()
  quit()

from time import sleep
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

##### Setup Adafruit_IO Client #####
from Adafruit_IO import Client, Feed
aio = Client(args.username, args.key)
feed_keys = [feed.key for feed in aio.feeds()]
if (not args.notempH or not args.notempP) and not args.location + 'temp-h' in feed_keys:
  aio.create_feed(Feed(name=args.location + 'temp-h'))
if not args.notempP and not args.location + 'temp-p' in feed_keys:
  aio.create_feed(Feed(name=args.location + 'temp-p'))
if not args.nohumidity and not args.location + 'humidity' in feed_keys:
  aio.create_feed(Feed(name=args.location + 'humidity'))
if not args.nopressure and not args.location + 'pressure' in feed_keys:
  aio.create_feed(Feed(name=args.location + 'pressure'))

##### Setup SenseHat #####
from sense_hat import SenseHat
sense = SenseHat() #create the sense hat object
##### Functions #####
def ctof(temp):
  return round((temp * 9 / 5) + 32,2)
json_output = {}
while True:
  if not args.notempH:
    temp = sense.get_temperature_from_humidity()
    if convert_to_F: temp = ctof(temp)
    aio.send('temp-h',temp)
    json_output['temp'] = temp
  if not args.notempP:
    temp = sense.get_temperature_from_pressure()
    if convert_to_F: temp = ctof(temp)
    aio.send('temp-p',temp)
  if not args.nohumidity:
    humidity = round(sense.get_humidity(),2)
    aio.send('humidity',humidity)
    json_output['humidity'] = humidity
  if not args.nopressure:
    pressure = round(sense.get_pressure()/1.3332239,2)
    aio.send('pressure',pressure)
    json_output['pressure'] = pressure
  if not args.noserver:
    with open(dir_path + "/index.html", "w") as f: f.write(json.dumps(json_output) + "\n")
  sleep(args.rate) #wait before getting the next data point
