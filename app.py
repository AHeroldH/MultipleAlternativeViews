#!/usr/bin/env python3

import json
from flask import Flask
from flask import request
import pandas as pd
from flask_cors import CORS
import numpy as np
import os
import rpy2.robjects as robjects
import ast
from scipy.spatial import distance
import csv
from heapq import heappush, heappushpop
import threading
import time

app = Flask(__name__)
CORS(app)

path = '.'
df = pd.read_csv('movie-data.csv')  # "world_wide_gross_income", "avg_vote", "votes", "reviews_from_critics", "country",
# "duration", "genre", "year"
x = [1.0, 9.0]
y = [0.0, 1346913161.0]
xRange = x[1] - x[0]
yRange = y[1] - y[0]
no_of_zoom = 0

left_view_x = [1.0, 9.0]
left_view_y = [0.0, 1346913161.0]
center_view_x = [1.0, 9.0]
center_view_y = [0.0, 1346913161.0]
right_view_x = [1.0, 9.0]
right_view_y = [0.0, 1346913161.0]
first_zoom_scagnostics = {}
with open('first_zoom_scagnostics.csv', mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        first_zoom_scagnostics[str(row[0] + ", " + row[1] + ", " + row[2])] = [float(str(row[3])[1:]), float(row[4]),
                                                                               float(row[5]), float(row[6]),
                                                                               float(row[7]), float(row[8]),
                                                                               float(row[9]), float(row[10]),
                                                                               float(str(row[11])[0:len(str(row[11])) - 1])]
second_zoom_scagnostics = {}
with open('second_zoom_scagnostics.csv', mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        second_zoom_scagnostics[str(row[0] + ", " + row[1] + ", " + row[2])] = [float(str(row[3])[1:]), float(row[4]),
                                                                                float(row[5]), float(row[6]),
                                                                                float(row[7]), float(row[8]),
                                                                                float(row[9]), float(row[10]),
                                                                                float(str(row[11])[0:len(str(row[11])) - 1])]
third_zoom_scagnostics = {}
with open('third_zoom_scagnostics.csv', mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        third_zoom_scagnostics[str(row[0] + ", " + row[1] + ", " + row[2])] = [float(str(row[3])[1:]), float(row[4]),
                                                                               float(row[5]), float(row[6]),
                                                                               float(row[7]), float(row[8]),
                                                                               float(row[9]), float(row[10]),
                                                                               float(str(row[11])[0:len(str(row[11])) - 1])]
rowNo = 0
diff2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
diff3 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
diff1_scags = [0, 0, 0, 0, 0, 0, 0, 0, 0]
current_view_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
left_view = False
center_view = False
right_view = False


def scagnostics(x, y):
    all_scags = {}
    r_source = robjects.r['source']
    r_source(os.path.join(path, 'get_scag.R'))
    r_get_name = robjects.globalenv['scags']
    scags = r_get_name(robjects.FloatVector(x), robjects.FloatVector(y))

    comp_scags = scags[0]

    all_scags['outlying'] = comp_scags[0]
    all_scags['skewed'] = comp_scags[1]
    all_scags['clumpy'] = comp_scags[2]
    all_scags['sparse'] = comp_scags[3]
    all_scags['striated'] = comp_scags[4]
    all_scags['convex'] = comp_scags[5]
    all_scags['skinny'] = comp_scags[6]
    all_scags['stringy'] = comp_scags[7]
    all_scags['monotonic'] = comp_scags[8]
    return all_scags


@app.route('/get-data', methods=['GET', 'POST'])
def return_data():
    return df.to_csv()


@app.route('/get-coords')
def get_coords():
    global left_view
    global right_view

    left_view = False
    right_view = False

    global no_of_zoom
    no_of_zoom = int(request.args['zoomNo'])
    global x
    x_coord = float(request.args['x'])
    x = [x_coord - xRange / (no_of_zoom * 4), x_coord + xRange / (no_of_zoom * 4)]

    global y
    y_coord = float(request.args['y'])
    y = [y_coord - yRange / (no_of_zoom * 4), y_coord + yRange / (no_of_zoom * 4)]

    global current_view_scagnostics
    global current_view_list
    data_in_view = df.loc[(df["avg_vote"] >= x[0]) & (df["avg_vote"] <= x[1]) & (df["rlwide_gross_income"] >= y[0])
                          & (df["rlwide_gross_income"] <= y[1])]

    current_view_scagnostics = scagnostics(data_in_view["avg_vote"], data_in_view["rlwide_gross_income"])

    current_view_list = [current_view_scagnostics['outlying'], current_view_scagnostics['skewed'],
                         current_view_scagnostics['clumpy'], current_view_scagnostics['sparse'],
                         current_view_scagnostics['striated'], current_view_scagnostics['convex'],
                         current_view_scagnostics['skinny'], current_view_scagnostics['stringy'],
                         current_view_scagnostics['monotonic']]

    comparable_views = {}

    if no_of_zoom == 1:
        comparable_views = first_zoom_scagnostics
    elif no_of_zoom == 2:
        comparable_views = second_zoom_scagnostics
    elif no_of_zoom == 3:
        comparable_views = third_zoom_scagnostics

    key_list = list(comparable_views.keys())
    val_list = list(comparable_views.values())

    lock = threading.Lock()

    calc_thread = threading.Thread(target=calc_alternatives, args=(lock, comparable_views, key_list, val_list))

    calc_thread.start()

    return ""


def calc_alternatives(lock, comparable_views, key_list, val_list):

    lock.acquire()
    set_left_view(comparable_views, current_view_list, key_list, val_list)
    lock.release()

    while lock.locked():
        time.sleep(0.100)

    #lock.acquire()
    #set_centre_view(comparable_views, current_view_list, key_list, val_list)
    #lock.release()

    #while lock.locked():
    #    time.sleep(0.100)

    lock.acquire()
    set_right_view(comparable_views, current_view_list, key_list, val_list)
    lock.release()

    print("left_view_x: " + str(left_view_x))
    print("left_view_y: " + str(left_view_y))
    print("center_view_x: " + str(center_view_x))
    print("center_view_y: " + str(center_view_y))
    print("right_view_x: " + str(right_view_x))
    print("right_view_x: " + str(right_view_y))

def set_left_view(comparable_views, current_view_list, key_list, val_list):
    global left_view_x
    global left_view_y
    global diff1_scags
    global left_view

    left_view = False

    diff1 = 0
    for view, scags in comparable_views.items():

        # view_diff = diff_of_lists(scags, current_view_list)

        view_diff = distance.euclidean(np.asarray(scags), np.asarray(current_view_list))

        new_diff1 = max(diff1, view_diff)

        if new_diff1 == view_diff:
            diff1 = view_diff
            diff1_scags = scags
            left = view.split("; ")
            left_view_x = ast.literal_eval(left[0])
            left_view_y = ast.literal_eval(left[1])

    left_view = True


def set_centre_view(comparable_views, current_view_list, key_list, val_list):
    global diff2
    global center_view_x
    global center_view_y
    global center_view

    center_view = False

    diff_1_2 = 0
    heap = []
    three_best_diff2 = []

    for view, scags in comparable_views.items():

        window = view.split("; ")
        window_x = ast.literal_eval(window[0])
        window_y = ast.literal_eval(window[1])

        if (((left_view_x[0] - 1) <= window_x[0] <= (left_view_x[1] + 1)) and ((left_view_x[0] - 1) <= window_x[1] <=
           (left_view_x[1] + 1))): #and (((left_view_y[0] - (1346913161 / (5829 / 8))) <= window_y[0] <=
           #(left_view_y[1] + (1346913161 / (5829 / 8)))) and ((left_view_y[0] - (1346913161 / (5829 / 8))) <=
          # window_y[1] <= (left_view_y[1] + (1346913161 / (5829 / 8)))))):
            continue

        # view_diff = diff_of_lists(scags, current_view_list)

        view_diff = distance.euclidean(np.asarray(scags), np.asarray(current_view_list))

        if len(heap) < 10:
            heappush(heap, view_diff)
        else:
            heappushpop(heap, view_diff)
        if view_diff in heap:
            three_best_diff2.insert(heap.index(view_diff), scags)

    for ele in three_best_diff2:
        if distance.euclidean(np.asarray(ele), np.asarray(diff1_scags)) > diff_1_2:
            diff_1_2 = distance.euclidean(np.asarray(ele), np.asarray(diff1_scags))
            diff2 = ele

    view = key_list[val_list.index(diff2)]
    center = view.split("; ")
    center_view_x = ast.literal_eval(center[0])
    center_view_y = ast.literal_eval(center[1])
    center_view = True


def set_right_view(comparable_views, current_view_list, key_list, val_list):
    global right_view_x
    global right_view_y
    global diff2
    global right_view

    right_view = False

    diff_1_2 = 0
    heap = []
    three_best_diff2 = [0 for i in range(10)]
    view_list = [0 for i in range(10)]

    for view, scags in comparable_views.items():

        window = view.split("; ")
        window_x = ast.literal_eval(window[0])
        window_y = ast.literal_eval(window[1])

        if (((left_view_x[0] - 1.5) <= window_x[0] <= (left_view_x[1] + 1.5)) and ((left_view_x[0] - 1.5) <= window_x[1] <=
            (left_view_x[1] + 1.5))):  # and (((left_view_y[0] - (1346913161 / (5829 / 8))) <= window_y[0] <=
            # (left_view_y[1] + (1346913161 / (5829 / 8)))) and ((left_view_y[0] - (1346913161 / (5829 / 8))) <=
            # window_y[1] <= (left_view_y[1] + (1346913161 / (5829 / 8)))))):
            continue

        # view_diff = diff_of_lists(scags, current_view_list)

        view_diff = distance.euclidean(np.asarray(scags), np.asarray(current_view_list))

        if view_diff in heap:
            continue

        if len(heap) < 10:
            heappush(heap, view_diff)
        else:
            heappushpop(heap, view_diff)
        if view_diff in heap:
            three_best_diff2[heap.index(view_diff)] = scags
            view_list[heap.index(view_diff)] = view

    print(heap)

    for ele in three_best_diff2:
        if distance.euclidean(np.asarray(ele), np.asarray(diff1_scags)) > diff_1_2:
            diff_1_2 = distance.euclidean(np.asarray(ele), np.asarray(diff1_scags))
            diff2 = ele

    view = key_list[val_list.index(diff2)]
    #heap = []
    #three_best_diff3 = []
    #
    #for view, scags in comparable_views.items():
    #
    #    window = view.split("; ")
    #    window_x = ast.literal_eval(window[0])
    #    window_y = ast.literal_eval(window[1])
    #
    #    inside_left_view = (((left_view_x[0] - 1) <= window_x[0] <= (left_view_x[1] + 1)) and ((left_view_x[0] - 1) <= window_x[1] <=
    #       (left_view_x[1] + 1)))# and (((left_view_y[0] - (1346913161 / (5829 / 8))) <= window_y[0] <=
    #       #(left_view_y[1] + (1346913161 / (5829 / 8)))) and ((left_view_y[0] - (1346913161 / (5829 / 8))) <=
    #       #window_y[1] <= (left_view_y[1] + (1346913161 / (5829 / 8))))))
    #
    #    inside_center_view = (((center_view_x[0] - 1) <= window_x[0] <=
    #        (center_view_x[1] + 1)) and ((center_view_x[0] - 1) <= window_x[1] <= (center_view_x[1] + 1))) #and
    #        #(((center_view_y[0] - (1346913161 / (5829 / 8))) <= window_y[0] <= (center_view_y[1] +
    #        #(1346913161 / (5829 / 8)))) and ((center_view_y[0] - (1346913161 / (5829 /8))) <= window_y[1] <=
    #        #(center_view_y[1] + (1346913161 / (5829 / 8))))))
    #
    #    if  inside_left_view or inside_center_view:
    #        continue
    #
    #    # view_diff = diff_of_lists(scags, current_view_list)
    #
    #    view_diff = distance.euclidean(np.asarray(scags), np.asarray(current_view_list))
    #
    #    if len(heap) < 10:
    #        heappush(heap, view_diff)
    #    else:
    #        heappushpop(heap, view_diff)
    #    if view_diff in heap:
    #        three_best_diff3.insert(heap.index(view_diff), scags)
    #
    #mean_diff_1_2 = [0 for i in range(len(three_best_diff3))]
    #
    #for idx, ele in enumerate(three_best_diff3):
    #    diff_1_3 = distance.euclidean(np.asarray(ele), np.asarray(diff1_scags))
    #    diff_2_3 = distance.euclidean(np.asarray(ele), np.asarray(diff2))
    #    mean_diff_1_2[idx] = diff_1_3 + diff_2_3 / 2
    #
    #diff3 = three_best_diff3[mean_diff_1_2.index(max(mean_diff_1_2))]
    #view = key_list[val_list.index(diff3)]
    right = view.split("; ")
    right_view_x = ast.literal_eval(right[0])
    right_view_y = ast.literal_eval(right[1])
    right_view = True


def diff_of_lists(l1, l2):
    view_diff = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for idx in range(len(l1)):
        largest = max(l2[idx], l1[idx])
        smallest = min(l2[idx], l1[idx])

        view_diff[idx] = smallest - largest

    return view_diff


@app.route('/get-left', methods=['GET', 'POST'])
def return_left_data():
    global left_view
    while left_view == False:
        time.sleep(0.100)

    return (df.loc[(df["avg_vote"] >= left_view_x[0]) & (df["avg_vote"] <= left_view_x[1]) & (
            df["rlwide_gross_income"] >= left_view_y[0]) & (df["rlwide_gross_income"] <=
                                                                left_view_y[1])]).to_csv()


@app.route('/get-center', methods=['GET', 'POST'])
def return_center_data():
    global center_view
    while center_view == False:
        time.sleep(0.100)

    return df.loc[(df["avg_vote"] >= center_view_x[0]) & (df["avg_vote"] <= center_view_x[1]) & (
            df["rlwide_gross_income"] >= center_view_y[0]) & (df["rlwide_gross_income"] <=
                                                                  center_view_y[1])].to_csv()


@app.route('/get-right', methods=['GET', 'POST'])
def return_right_data():
    global right_view
    while right_view == False:
        time.sleep(0.100)

    return df.loc[(df["avg_vote"] >= right_view_x[0]) & (df["avg_vote"] <= right_view_x[1]) &
                  (df["rlwide_gross_income"] >= right_view_y[0]) & (df["rlwide_gross_income"] <=
                                                                        right_view_y[1])].to_csv()


@app.route('/get-left-scagnostics', methods=['GET', 'POST'])
def return_left_scagnostics():
    global left_view
    while left_view == False:
        time.sleep(0.100)
    left_scags = {"Outlying": diff1_scags[0], "Skewed": diff1_scags[1], "Clumpy": diff1_scags[2],
                  "Sparse": diff1_scags[3], "Striated": diff1_scags[4], "Convex": diff1_scags[5],
                  "Skinny": diff1_scags[6], "Stringy": diff1_scags[7], "Monotonic": diff1_scags[8]}
    return json.dumps(left_scags)


@app.route('/get-center-scagnostics', methods=['GET', 'POST'])
def return_center_scagnostics():
    global center_view
    while center_view == False:
        time.sleep(0.100)
    center_scags = {"Outlying": diff2[0], "Skewed": diff2[1], "Clumpy": diff2[2], "Sparse": diff2[3],
                    "Striated": diff2[4], "Convex": diff2[5], "Skinny": diff2[6], "Stringy": diff2[7],
                    "Monotonic": diff2[8]}
    return json.dumps(center_scags)


@app.route('/get-right-scagnostics', methods=['GET', 'POST'])
def return_right_scagnostics():
    global right_view
    while right_view == False:
        time.sleep(0.100)
    right_scags = {"Outlying": diff2[0], "Skewed": diff2[1], "Clumpy": diff2[2], "Sparse": diff2[3],
                   "Striated": diff2[4], "Convex": diff2[5], "Skinny": diff2[6], "Stringy": diff2[7],
                   "Monotonic": diff2[8]}
    return json.dumps(right_scags)


@app.route('/get-current-scagnostics', methods=['GET', 'POST'])
def return_current_scagnostics():
    right_scags = {"Outlying": current_view_list[0], "Skewed": current_view_list[1], "Clumpy": current_view_list[2],
                   "Sparse": current_view_list[3], "Striated": current_view_list[4], "Convex": current_view_list[5],
                   "Skinny": current_view_list[6], "Stringy": current_view_list[7], "Monotonic": current_view_list[8]}
    return json.dumps(right_scags)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
    #app.run()
