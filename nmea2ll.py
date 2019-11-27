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
def parse_nmea_sentences(nmea_sentence_type, sentence):
    sentences = {
        "GLL": parse_gll, # "GLL: Geographic Position - Latitude/Longitude"
        "GGA": parse_gga, # "GGA: Global Positioning System Fix Data"
        "RMC": parse_rmc  # "RMC: Recommended Minimum Navigation Information"
    }
    func = sentences.get(nmea_sentence_type, parse_others)
    return func(sentence)

# parse_gll
#   parse lat and long from GLL sentence
def parse_gll(sentence):
    data = sentence.split(',')          # split data into a list
    lat = data[1] + data[2]             # get lat data at correct position in list
    long = data[3] + data[4]            # get long data at correct position in list
    lat = lat.replace('.', '')          # remove decimal point from incorrect location in lat
    long = long.replace('.','')         # remove decimal point from incorrect location in long
    lat = lat[:2] + '.' + lat[2:]       # add decimal point back to correct location in lat
    long = long[:3] + '.' + long[3:]    # add decimal point back to correct location in long
    location = "{ \"GLL\": { \"lat\": \"" + lat + "\", \"long\": \"" + long + "\" } }"  # lat and long put into structured JSON
    return location                     # return the location

# parse_gga
#   parse lat and long from GGA sentence
def parse_gga(sentence):
    data = sentence.split(',')          # split data into a list
    lat = data[2] + data[3]             # get lat data at correct position in list
    long = data[4] + data[5]            # get long data at correct position in list
    lat = lat.replace('.', '')          # remove decimal point from incorrect location in lat
    long = long.replace('.','')         # remove decimal point from incorrect location in long
    lat = lat[:2] + '.' + lat[2:]       # add decimal point back to correct location in lat
    long = long[:3] + '.' + long[3:]    # add decimal point back to correct location in long
    location = "{ \"GGA\": { \"lat\": \"" + lat + "\", \"long\": \"" + long + "\" } }"  # lat and long put into structured JSON
    return location                     # return the location

# parse_rmc
#   parse lat and long from RMC sentence
def parse_rmc(sentence):
    data = sentence.split(',')          # split data into a list
    lat = data[3] + data[4]             # get lat data at correct position in list
    long = data[5] + data[6]            # get long data at correct position in list
    lat = lat.replace('.', '')          # remove decimal point from incorrect location in lat
    long = long.replace('.','')         # remove decimal point from incorrect location in long
    lat = lat[:2] + '.' + lat[2:]       # add decimal point back to correct location in lat
    long = long[:3] + '.' + long[3:]    # add decimal point back to correct location in long
    location = "{ \"RMC\": { \"lat\": \"" + lat + "\", \"long\": \"" + long + "\" } }"  # lat and long put into structured JSON
    return location                     # return the location

# parse_others
#   do nothing for all other sentence types
def parse_others(sentence):
    return ""

# open the nmea data file for reading
nmea_data = open("20191121-18-44-20.nmea", "r")

# loop through each line in the nmea data file
#   (each line will be 1 nmea sentence)
for sentence in nmea_data:
    if sentence[0] == "$":                                          # only check nmea statement if sentence begins with a '$'
        nmea_sentence_type = sentence[3:6]                          # use substring to get the sentence type
        loc = parse_nmea_sentences(nmea_sentence_type, sentence)    # will return location if sentence type is correct (i.e. GLL, GGA, or RMC)
        if not loc == "":                                           # if the location is not empty...
            print(loc)                                              # print the location

# close the nmea data file now that we are finished with it
nmea_data.close()
