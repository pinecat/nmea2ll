import RPi.GPIO as GPIO
import time
import json
from nmea2ll import parse_nmea_sentences

# open pathdata file for route
path_data = open('pathdata.json', 'r')

for data in path_data:
    loc = json.loads(data)
    print(loc)

path_data.close()
