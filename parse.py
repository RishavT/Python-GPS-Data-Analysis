#!/usr/bin/env python

"""
Analyse GPS data from a JSON file for speed spikes.
Pass the time stamps as an argument to another shell script for video processing

"""

import json
import datetime
import pprint
from operator import itemgetter
import natsort

data_file = "waypoints.json" #path to gps data file in json format.

with open(data_file) as json_file:
    json_data = json.load(json_file)
    #pprint.pprint(json_data)


def speed_ans(self, data_file):
	pass

# Example list an dict
dict = json_data
# Sort the dict
output = sorted(dict, key=itemgetter(*['Speed']))
natsort.natsorted(dict, key=itemgetter(*['Speed']))

pprint.pprint(output)