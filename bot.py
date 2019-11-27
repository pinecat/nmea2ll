import RPi.GPIO as GPIO
import time
import json
from nmea2ll import parse_nmea_sentences

# open pathdata file for route
path_data = open('pathdata.json', 'r')

for data in path_data:
    ll = json.loads(data)
    lat
    long

    if ll.get('GLL'):
        print ll['GLL']

    if ll.get('GGA'):
        print ll['GGA']

    if ll.get('RMC'):
        print ll['RMC']

path_data.close()
