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

def display(waypoints):
    """Function to print our waypoints list"""
    for i, e in enumerate(waypoints):
        if e['Speed'] >= 5:
            print 'Speed', e['Speed']
            print 'Timestamp', e['Timestamp']
            if 'Acceleration' in e:
                print 'Acceleration', e['Acceleration']

def calculate_acceleration(waypoints):
    """Function to calculate the acceleration for each point in our list"""
    waypoints_with_acceleration = []
    for i, e in enumerate(waypoints):
        if e['Speed'] >= 5:
            # print 'Speed', e['Speed']
            # print 'Timestamp', e['Timestamp']

            # Calculate the acceleration at that point
            # Since acceleration = dv/dt (differentiation of velocity w.r.t time)
            # We'll call the differentiate function.

            # Since we're using the enumerate function, e is equivalent to
            # waypoints[i]. Hence the earlier value would be waypoints[i-1]
            # and the next value would be waypoints[i+1].
            # We cannot get acceleration for either the starting or the ending point,
            # Depending on whether we use i-1 or i+1. Both should be good if the
            # timestamps are small enough.

            # For now we'll use [i-1], so the starting point will not have acceleration
            # defined.

            if i==0:
                continue

            previous_e = waypoints[i-1]
            # Save the acceleration inside the dict so that it can be accessed later.
            # outside this loop.
            # Hence using the original varuable instead of `e`
            e['Acceleration'] = differentiate(v2=e['Speed'],
                                              v1=previous_e['Speed'],
                                              t2=e['Timestamp'],
                                              t1=previous_e['Timestamp'])

            # print 'Acceleration', e['Acceleration']
            waypoints_with_acceleration.append(e)
    return waypoints_with_acceleration

def extract_good_points(waypoints):
    """Function to extract relevant points from a list of waypoints
    Parameters:
    1. acceleration_treshold - minimum acceleration for a point to be considered good
    2. time_buffer - the number of seconds of 'buffer' period for any new batch of good points
                     For example, if time_buffer = 1, any new batch (except for the first)
                     will start with a 1 second buffer of low acceleration JUST before the high
                     acceleration starts to make the video look natural.
    """
    acceleration_treshold = 0
    time_buffer = 1
    i = 1
    good_points = []
    batch_number = 0
    while i < len(waypoints):

        if waypoints[i]['Acceleration'] < acceleration_treshold:
            batch_number += 1
            # This means he's slowing down
            # We'll loop through the upcoming time slots
            # and take the last time_buffer seconds of slowing down/ constant speed.
            # Basically if it's
            # slowdown/slowdown/slowdown/slowdown/constant/constant/speedup/speedup
            # We'll only keep slowdown/constant/constant/speedup/speedup

            old_i = 0
            is_done = False
            while i < len(waypoints) and not is_done:
                if waypoints[i]['Acceleration'] > acceleration_treshold:
                    # This implies he's accelerating again.
                    # We take at max last 3 points of slow speed from now.
                    # This is the same as minimum of 3, total slow speed duration.
                    j = i - min(time_buffer, i - old_i)
                    while j <= i:
                        if len(good_points) == batch_number:
                            good_points.append([])
                        good_points[batch_number].append(waypoints[j])
                        j += 1
                    is_done = True
                i += 1

        # This means the driver is constant or accelerating
        # So we want this, it's a good point.
        if len(good_points) == batch_number:
            good_points.append([])
        good_points[batch_number].append(waypoints[i])
        i += 1
        # print i

    return good_points


if __name__ == '__main__':
    with open(data_file) as f:
        waypoints = json.load(f)

    sorted_waypoints = natsort.natsorted(waypoints, key=itemgetter(*['Timestamp']), reverse = False)
    waypoints_with_acceleration = calculate_acceleration(sorted_waypoints)
    # display(waypoints_with_acceleration)
    good_points = extract_good_points(waypoints_with_acceleration)
    # Remove empty batches if any
    good_points = [batch for batch in good_points if len(batch) > 0]

    # Printing, for now
    for i,batch in enumerate(good_points):
        if len(batch) == 0:
            continue
        print 'Batch Number %d' % (i+1)
        # Check if batch is empty for some reason
        print 'Start Time %f' % batch[0]['Timestamp']
        print 'End Time %f' % batch[-1]['Timestamp']
        display(batch)
        print '\n'

    # Get start,end tuple list
    # start_end_list = [(batch[0]['Timestamp'], batch[-1]['Timestamp']) for batch in good_points]
    start_end_list = []
    for batch in good_points:
        entry = {
            'start_time': batch[0]['Timestamp'],
            'end_time': batch[-1]['Timestamp'],
            'waypoints': batch
        }
        start_end_list.append(entry)
    print start_end_list

    #pprint.pprint(sorted_waypoints)
    visualize_type(sorted_waypoints)
