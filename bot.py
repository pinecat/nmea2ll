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
        lat = end_coords['GLL']['lat']
        long = end_coords['GLL']['long']
    elif end_coords.get('RMC'):
        lat = end_coords['GLL']['lat']
        long = end_coords['GLL']['long']
    else:
        lat = ""
        long = ""
    return lat, long

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

# main prog loop #
#   start reading in the coordinates from the path_data file.
#   run through each line, and parse out the next coordinate.
#   then, determine what our current lat and long is.  use
#   our current lat and long and the lat and long from the
#   path data to calculate the bearing needed to reach the
#   next coordinate.  start moving the bot forward, and then
#   use the turning and GPS data from the sock_bearing
#   socket to align ourselves with the calculated bearing.
#   check to see if we've reached that point: if we have,
#   then grab the next coordinate from the path_data file,
#   otherwise keep moving and adjusting bearing as needed.
for json_element in path_data:
    end_coords = json.loads(json_element)
    end_lat, end_long = get_latlong_from_json(end_coords)
