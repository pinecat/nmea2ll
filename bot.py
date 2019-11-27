import RPi.GPIO as GPIO
import time
import json
from nmea2ll import parse_nmea_sentences

HOST = '192.168.0.11'
PORT_LL = 12345
PORT_HEADING = 54321

# open pathdata file for route
path_data = open('pathdata.json', 'r')

# open data sockets
ll_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ll_sock.connect((HOST, PORT_LL))
heading_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
heading_sock.connect((HOST, PORT_HEADING))

for data in path_data:
    ll = json.loads(data)
    lat = 0
    long = 0

    if ll.get('GLL'):
        lat = ll['GLL']['lat']
        long = ll['GLL']['long']

    if ll.get('GGA'):
        lat = ll['GGA']['lat']
        long = ll['GGA']['long']

    if ll.get('RMC'):
        lat = ll['RMC']['lat']
        long = ll['RMC']['long']

    

path_data.close()
