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
dict_file = json_data
# Sort the dict
#sorted(dict_file, key=itemgetter(*['Speed']), reverse = True)
output = natsort.natsorted(dict_file, key=itemgetter(*['Speed']), reverse = True)

pprint.pprint(output)

def visualize_type(output):
    """Visualize data by category in a bar graph"""

    #This returns a dict where it sums the total per Category.
    counter = Counter(item["Speed"] for item in output)

    # Set the labels which are based on the keys of our counter.
    labels = tuple(counter.key("Speed"))

    # Set where the labels hit the x-axis
    xlocations = np.arange(len(labels)) + 0.5

    # Width of each bar
    width = 0.5

    # Assign data to a bar plot
    plt.bar(xlocations, counter.values(), width=width)

    # Assign labels and tick location to x- and y-axis
    plt.xticks(xlocations + width / 2, labels, rotation=90)
    plt.yticks(range(0, max(counter.values()), 5))

    # Give some more room so the labels aren't cut off in the graph
    plt.subplots_adjust(bottom=0.4)

    # Make the overall graph/figure larger
    plt.rcParams['figure.figsize'] = 12, 8

    # Save the graph!
    plt.savefig("Graph.png")

    plt.clf()