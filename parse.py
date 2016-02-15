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
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter



#path to gps data file in json format.
data_file = "waypoints.json"


def speed_ans(self, data_file):
    pass



def visualize_type(output):
    """Visualize data by category in a bar graph"""

    #This returns a dict where it sums the total per Category.
    counter = Counter(item["Speed"] for item in output)

    # Set the labels which are based on the keys of our counter.
    labels = counter.keys()

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

def differentiate(v1, v2, t1, t2):
    """Method to differentiate velocity and get acceleration.
    Uses the approximation:
    dy/dx = (y2-y1)/(x2-x1) if x1 is almost equal to x2.
    """
    dx = v2-v1
    dt = t2-t1
    return dx/dt

if __name__ == '__main__':
    with open(data_file) as f:
        waypoints = json.load(f)

    sorted_waypoints = natsort.natsorted(waypoints, key=itemgetter(*['Speed']), reverse = True)
    #pprint.pprint(sorted_waypoints)

    print len(sorted_waypoints)
    for i, e in enumerate(sorted_waypoints):
        # for k, v in e.items():
        #     if (k == 'Speed' and v >= 5): #Set the threshold to 5 mps for speed anything less will be ignored.
        #         print k, v
        #         for k, v in e.items():
        #             if (k == 'Timestamp'):
        #                 print k, v
        if e['Speed'] >= 5:
            print 'Speed', e['Speed']
            print 'Timestamp', e['Timestamp']

        # Calculate the acceleration at that point
        # Since acceleration = dv/dt (differentiation of velocity w.r.t time)
        # We'll call the differentiate function.

        # Since we're using the enumerate function, e is equivalent to
        # sorted_waypoints[i]. Hence the earlier value would be sorted_waypoints[i-1]
        # and the next value would be sorted_waypoints[i+1].
        # We cannot get acceleration for either the starting or the ending point,
        # Depending on whether we use i-1 or i+1. Both should be good if the
        # timestamps are small enough.

        # For now we'll use [i-1], so the starting point will not have acceleration
        # defined.

        if i==0:
            continue

        previous_e = sorted_waypoints[i-1]
        e['Acceleration'] = differentiate(v2=e['Speed'],
                                          v1=previous_e['Speed'],
                                          t2=e['Timestamp'],
                                          t1=previous_e['Timestamp'])

        print 'Acceleration', e['Acceleration']


    visualize_type(sorted_waypoints)
