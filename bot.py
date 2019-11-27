import RPi.GPIO as GPIO
import time
import json
import math
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
    path_ll = json.loads(data)
    lat = 0
    long = 0

    if path_ll.get('GLL'):
        lat = path_ll['GLL']['lat']
        long = path_ll['GLL']['long']

    if path_ll.get('GGA'):
        lat = path_ll['GGA']['lat']
        long = path_ll['GGA']['long']

    if path_ll.get('RMC'):
        lat = path_ll['RMC']['lat']
        long = path_ll['RMC']['long']

    nmea_data = ll_sock.recv(1024)
    nmea_sentence_type = data[3:6]
#    while nmea_sentence_type != 'GLL' and nmea_sentence_type != 'GGA' and nmea_sentence_type != 'RMC':
#        nmea_data = ll_sock.recv(1024)
#        nmea_sentence_type = data[3:6]

    loc = parse_nmea_sentences(nmea_sentence_type, nmea_data)
    cur_lat = 0;
    cur_long = 0
    if loc != "":
        if loc.get('GLL'):
            cur_lat = loc['GLL']['lat']
            cur_long = loc['GLL']['long']

        if loc.get('GGA'):
            cur_lat = loc['GGA']['lat']
            cur_long = loc['GGA']['long']

        if loc.get('RMC'):
            cur_lat = loc['RMC']['lat']
            cur_long = loc['RMC']['long']

    y = math.sin(long - cur_long) * math.cos(lat)
    x = (math.cos(cur_lat) * math.sin(lat)) - (math.sin(cur_lat) * math.cos(lat) * math.cos(long - cur_long))
    bearing = math.degrees(math.atan2(y, x))
    print(bearing)
    

path_data.close()
