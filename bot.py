######################################################################
#   Name:   bot.py
#   Desc:   Code for navigation and control of E-Bot 9:
#               Deliver-E-Bot
#           This program part of The Elizabethtown RMI
#               (Robotics & Machine Intelligence) Club,
#               and the CS434 Green Robotics class
######################################################################

# imports #
import math                                 # used for sin(), cos(), atan2(), degrees()
import socket                               # used to open/connect to server sockets
import json                                 # used to parse json
import time                                 # used for sleep()
import threading                            # used to create threads
import RPi.GPIO as GPIO                     # used to control GPIO pins on the RasPi
from nmea2ll import parse_nmea_sentences    # used for parsing NMEA sentences

# constants #
HOST = '192.168.0.11'   # ip address of raspi with the GPS unit, which is serving the GPS data
PORT_LOCATION = 12345   # port for the service serving raw NMEA sentences (used primarily to get lat and long)
PORT_BEARING = 54321    # port for the service serving current bearing data of the GPS unit (i.e. compass direction)

# get_latlong_from_json
#   helper function for getting lat and long from json
def get_latlong_from_json(end_coords):
    '''
    get_latlong_from_json:
        parse out the lat and long from our json_element
    params:
        json - end_coords - the json element containing the lat/long data
    returns:
        string - lat - the latitude
        string - long - the longitude
    '''
    lat = 0
    long = 0
    if end_coords.get('GLL'):
        lat = end_coords['GLL']['lat']
        long = end_coords['GLL']['long']
    elif end_coords.get('GGA'):
        lat = end_coords['GGA']['lat']
        long = end_coords['GGA']['long']
    elif end_coords.get('RMC'):
        lat = end_coords['RMC']['lat']
        long = end_coords['RMC']['long']
    else:
        lat = ""
        long = ""
    return lat, long

# get_bearing
#   returns current bearing
def get_bearing():
    bearing_rmc = sock_location.recv(1024)
    while parse_nmea_sentences(bearing_rmc) == "":
        bearing_rmc = sock_location.recv(1024)
    bearing_rmc = parse_nmea_sentences(bearing_rmc)
    bearing_json = json.loads(bearing_rmc)
    print(bearing_json)
    cur_bearing = get_bearing_from_json(bearing_json)
    return cur_bearing

# get_bearing_from_json
#   gets the bearing from RMC json
def get_bearing_from_json(json):
    if json.get('RMC'):
        return json['RMC']['bearing']
    return -1

# de_dup
#   helper function for deduping lat long points from path_data
def de_dup((lat, long), coords):
    for (x, y) in coords:
        if x == lat and y == long:
            return coords
    coords.append((lat, long))
    return coords

# calculate_bearing
#   helper function to calculate the bearing needed to get to end_lat, end_long
def calculate_bearing(end_lat, end_long, cur_lat, cur_long):
    # convert lats and longs to floats
    end_lat = float(end_lat)
    end_long = float(end_long)
    cur_lat = float(cur_lat)
    cur_long = float(cur_long)
    
    #end_lat = math.radians(end_lat)
    #end_long = math.radians(end_long)
    #cur_lat = math.radians(cur_lat)
    #cur_long = math.radians(cur_long)
    
    r = 6371000
    a1 = math.radians(cur_lat)
    a2 = math.radians(cur_long)
    b1 = math.radians(end_lat - cur_lat)
    b2 = math.radians(end_long - cur_long)

    # calculate bearing and convert to degrees
    y = math.sin(b2 - b1) * math.cos(a2)
    x = (math.cos(a1) * math.sin(a2)) - (math.sin(a1) * math.cos(a2) * math.cos(b2 - b1))
    bearing = math.degrees(math.atan2(y, x))
    if (bearing < 0):
        bearing = bearing + 360
    return bearing

# right
#   turn right
def right():
    GPIO.output(22, GPIO.LOW)
    GPIO.output(27, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)

# left
#   turn left
def left():
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)

# forward
#   move forward
def forward():
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(26, GPIO.HIGH)

# open pathdata file for route #
# for now, this is just the route for brinser
path_data = open('pathdata-brinser.json', 'r')

# open data sockets #
# socket for lat/long and/or NMEA data
sock_location = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_location.connect((HOST, PORT_LOCATION))

# socket for heading/bearing data
sock_bearing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_bearing.connect((HOST, PORT_BEARING))

# initialize io pins #
GPIO.setmode(GPIO.BCM)      # set the pin mode

# rear motors
GPIO.setup(21, GPIO.OUT)    # rear motor 1
GPIO.setup(26, GPIO.OUT)    # rear motor 2
#pwm1 = GPIO.PWM(21, 100)    # pwm for rear motor 1
#pwm2 = GPIO.PWM(26, 100)    # pwm for rear motor 2

# turning
GPIO.setup(22, GPIO.OUT)    # high to turn left, low to turn right
GPIO.setup(27, GPIO.OUT)    # high to turn right, low to turn left

# read in all points from path_data and de_dup them #
coords = []
for json_element in path_data:
    end_coords = json.loads(json_element)
    end_lat, end_long = get_latlong_from_json(end_coords)
    coords = de_dup((end_lat, end_long), coords)

# main prog loop #
#   determine what our current lat and long is.  use
#   our current lat and long and the lat and long from the
#   path data to calculate the bearing needed to reach the
#   next coordinate.  start moving the bot forward, and then
#   use the turning and GPS data from the sock_bearing
#   socket to align ourselves with the calculated bearing.
#   check to see if we've reached that point: if we have,
#   then grab the next coordinate from the path_data file,
#   otherwise keep moving and adjusting bearing as needed.

# start back motors
#motor_thread = threading.Thread(target = forward)
#motor_thread.start()
#pwm1.start(80)
#pwm2.start(80)
GPIO.output(21, GPIO.HIGH)


cur_bearing = -1.0
coords[100] = (40.1489685, -76.5915081667)
i = 100
#j = 2
while i < len(coords):
    # get good gps data
    current_location = sock_location.recv(1024)
    while parse_nmea_sentences(current_location) == "":
        current_location = sock_location.recv(1024)
    current_location = parse_nmea_sentences(current_location)

    # parse out our current lat and long
    cur_coords = json.loads(current_location)
    cur_lat, cur_long = get_latlong_from_json(cur_coords)
    cur_lat = float(cur_lat)
    cur_long = float(cur_long)

    # calculate margins to check current lat and long against from coords
    wanted_lat, wanted_long = coords[i]
    wanted_lat = float(wanted_lat)
    wanted_long = float(wanted_long)
    lo_lat_margin = wanted_lat - 0.00003
    hi_lat_margin = wanted_lat + 0.00003
    lo_long_margin = wanted_long - 0.000003
    hi_long_margin = wanted_long + 0.000003

    # get our current bearing
    mb_cur_bearing = get_bearing()
    if mb_cur_bearing != "":
        mb_cur_bearing = float(mb_cur_bearing)
    	if mb_cur_bearing != -1:
            cur_bearing = mb_cur_bearing

    #while cur_bearing == 0:
    #    bearing_rmc = sock_location.recv(1024)
    #    while parse_nmea_sentences(bearing_rmc) == "":
    #        bearing_rmc = sock_location.recv(1024)
    #    bearing_rmc = parse_nmea_sentences(bearing_rmc)
    #    bearing_json = json.loads(bearing_rmc)
    #    cur_bearing = get_bearing(bearing_json)
    
    #cur_bearing = sock_bearing.recv(1024)
    #cur_bearing = cur_bearing.split('\n')[0]
    #cur_bearing = float(cur_bearing)
    #print(cur_bearing)
    
    # calculate bearing
    wanted_bearing = calculate_bearing(wanted_lat, wanted_long, cur_lat, cur_long)
    lo_wanted_bearing_margin = wanted_bearing - 1
    hi_wanted_bearing_margin = wanted_bearing + 1
    if lo_wanted_bearing_margin < 0:
        lo_wanted_bearing_margin = lo_wanted_bearing_margin + 360
    if hi_wanted_bearing_margin > 360:
        hi_wanted_bearing_margin = hi_wanted_bearing_margin - 360
    
    # calculate absolute degree of change
    #abs_bearing_chg_deg = cur_bearing - wanted_bearing
    #if abs_bearing_chg_deg < 0:
    #    abs_bearing_chg_deg = abs_bearing_chg_deg + 360

    #if j % 2 == 0:
    #    cur_bearing = 90.0
    #else:
    #    cur_bearing = 270.0
    #j = j + 1
    
    # calculate which way to turn, negative values indicate to turn left
    cur_bearing_rad = math.radians(cur_bearing)
    wanted_bearing_rad = math.radians(wanted_bearing)

    # actual
    hx = math.sin(cur_bearing_rad)
    hy = math.cos(cur_bearing_rad)

    # antipode
    ax = math.sin(cur_bearing_rad + math.radians(180))
    ay = math.cos(cur_bearing_rad + math.radians(180))

    # desired
    dx = math.sin(wanted_bearing_rad)
    dy = math.cos(wanted_bearing_rad)

    # distance
    dist = ((dx - ax) * (hy - ay)) - ((dy - ay) * (hx - ax))
    print('Distance: ' + str(dist))

    turn_right = False
    if dx == ax and dy == ay:
        turn_right = True
        right()
    elif dist > 0:
        turn_right = True
        right()
    elif dist < 0:
        turn_right = False
        left()
    
    # check if we are at the wanted lat, long
    if cur_lat > lo_lat_margin and cur_lat < hi_lat_margin:
        if cur_long > lo_long_margin and cur_long < hi_long_margin:
            i = i + 10 # increment i (spot in our coords array)
    print('cur_lat: ' + str(cur_lat) + ', cur_long: ' + str(cur_long))
    print('cur_bearing: ' + str(cur_bearing))
    print('wanted_bearing: ' + str(wanted_bearing))
    print('lo_lat_margin: ' + str(lo_lat_margin) + ', hi_lat_margin: ' + str(hi_lat_margin))
    print('lo_long_margin: ' + str(lo_long_margin) + ', hi_long_margin: ' + str(hi_long_margin))
    print('i: ' + str(i))

GPIO.output(21, GPIO.LOW)
GPIO.output(26, GPIO.LOW)

# clean shutdown all our sockets and IO before close
sock_location.close()
sock_bearing.close()
GPIO.output(21, GPIO.LOW)
GPIO.output(26, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
GPIO.cleanup()
