######################################################################
#   Name:   nmea2ll.py
#   Desc:   Parse latitude and longitude from raw NMEA sentences
#           Parses data from GGA, GLL, and RMC type sentences
#           This program used as parsing test, and as such,
#               reads it's nmea sentences from a file
#           The final program will get the sentences from a
#               socket connection
#   Author: Rory Dudley (pinecat)
######################################################################

# define dictionary and helper function for valid sentence types
#   (i.e. sentence types with lat and long data)
def parse_nmea_sentences(sentence):
    '''
    parse_nmea_sentences:
        helper function with defines dictionary for valid sentence types
    params:
        string - sentence - the NMEA sentence from the GPS module
    returns:
        on_valid_sentence_type:
            func - location - the latitude and longitude from the NMEA sentence
        on_invalid_sentence_type:
            func - - the empty string ("")
    '''
    sentences = {
        "GLL": parse_gll, # "GLL: Geographic Position - Latitude/Longitude"
        "GGA": parse_gga, # "GGA: Global Positioning System Fix Data"
        "RMC": parse_rmc  # "RMC: Recommended Minimum Navigation Information"
    }
    nmea_sentence_type = sentence[3:6]
    func = sentences.get(nmea_sentence_type, parse_others)
    return func(sentence)

# parse_gll
#   parse lat and long from GLL sentence
def parse_gll(sentence):
    data = sentence.split(',')          # split data into a list
    lat = data[1]                       # get lat data at correct position in list
    long = data[3]                      # get long data at correct position in list
    lat_dir = data[2]                   # get N, S
    long_dir = data[4]                  # get E, W
    lat_deg = float(lat[:2])            # parse degrees from latitude
    lat_min = float(lat[2:])            # parse minutes from latitude
    long_deg = float(long[:3])          # parse degrees from longitude
    long_min = float(long[3:])          # parse minutes from longitude
    lat = lat_deg + (lat_min/60.0)      # convert to decimal representation of lat
    long = long_deg + (long_min/60.0)   # convert to decimal representation of long

    # make sure decimal representation is correct depending on N, S, E, W
    if lat_dir == 'S':
        lat = lat * -1
    if long_dir == 'W':
        long = long * -1

    location = "{ \"GLL\": { \"lat\": \"" + str(lat) + "\", \"long\": \"" + str(long) + "\" } }"  # lat and long put into structured JSON
    return location                     # return the location

# parse_gga
#   parse lat and long from GGA sentence
def parse_gga(sentence):
    data = sentence.split(',')          # split data into a list
    lat = data[2]                       # get lat data at correct position in list
    long = data[4]                      # get long data at correct position in list
    lat_dir = data[3]                   # get lat data at correct position in list
    long_dir = data[5]                  # get long data at correct position in list
    lat_deg = float(lat[:2])            # parse degrees from latitude
    lat_min = float(lat[2:])            # parse minutes from latitude
    long_deg = float(long[:3])          # parse degrees from longitude
    long_min = float(long[3:])          # parse minutes from longitude
    lat = lat_deg + (lat_min/60.0)      # convert to decimal representation of lat
    long = long_deg + (long_min/60.0)   # convert to decimal representation of long

    # make sure decimal representation is correct depending on N, S, E, W
    if lat_dir == 'S':
        lat = lat * -1
    if long_dir == 'W':
        long = long * -1

    location = "{ \"GGA\": { \"lat\": \"" + str(lat) + "\", \"long\": \"" + str(long) + "\" } }"  # lat and long put into structured JSON
    return location                     # return the location

# parse_rmc
#   parse lat and long from RMC sentence
def parse_rmc(sentence):
    data = sentence.split(',')          # split data into a list
    lat = data[3]                       # get lat data at correct position in list
    long = data[5]                      # get long data at correct position in list
    lat_dir = data[4]                   # get lat data at correct position in list
    long_dir = data[6]                  # get long data at correct position in list
    bearing = data[8]                   # get bearing
    lat_deg = 0
    lat_min = 0
    long_deg = 0
    long_min = 0
    if lat_dir != "":
        lat_deg = float(lat[:2])            # parse degrees from latitude
        lat_min = float(lat[2:])            # parse minutes from latitude
    if long_dir != "":
        long_deg = float(long[:3])          # parse degrees from longitude
        long_min = float(long[3:])          # parse minutes from longitude
    lat = lat_deg + (lat_min/60.0)      # convert to decimal representation of lat
    long = long_deg + (long_min/60.0)   # convert to decimal representation of long

    # make sure decimal representation is correct depending on N, S, E, W
    if lat_dir == 'S':
        lat = lat * -1
    if long_dir == 'W':
        long = long * -1

    location = "{ \"RMC\": { \"lat\": \"" + str(lat) + "\", \"long\": \"" + str(long) + "\", \"bearing\": \"" + str(bearing) + "\" } }"  # lat and long put into structured JSON
    return location                     # return the location

# parse_others
#   do nothing for all other sentence types
def parse_others(sentence):
    return ""

# open the nmea data file for reading
#nmea_data = open("20191121-18-44-20.nmea", "r")

# loop through each line in the nmea data file
#   (each line will be 1 nmea sentence)
#for sentence in nmea_data:
#    if sentence[0] == "$":                                          # only check nmea statement if sentence begins with a '$'
#        nmea_sentence_type = sentence[3:6]                          # use substring to get the sentence type
#        loc = parse_nmea_sentences(nmea_sentence_type, sentence)    # will return location if sentence type is correct (i.e. GLL, GGA, or RMC)
#        if not loc == "":                                           # if the location is not empty...
#            print(loc)                                              # print the location

# close the nmea data file now that we are finished with it
#nmea_data.close()
