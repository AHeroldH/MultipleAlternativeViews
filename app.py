#!/usr/bin/env python3

import json
import multiprocessing
from flask import Flask
from flask import request
from flask import render_template
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
from functools import partial

app = Flask(__name__)
CORS(app)

path = '.'
df = pd.read_csv('movie-data.csv')
orig_x = [1.0, 9.0]
orig_y = [0.0, 1515047671.0]
x = [1.0, 9.0]
y = [0.0, 1515047671.0]
xRange = x[1] - x[0]
yRange = y[1] - y[0]
no_of_zoom = 0
left_view_x = [1.0, 9.0]
left_view_y = [0.0, 1515047671.0]
center_view_x = [1.0, 9.0]
center_view_y = [0.0, 1515047671.0]
right_view_x = [1.0, 9.0]
right_view_y = [0.0, 1515047671.0]
rowNo = 0
diff2 = 0
diff3 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
diff1_scags = [0, 0, 0, 0, 0, 0, 0, 0, 0]
current_view_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
left_view = False
center_view = False
right_view = False
current_scag = False
diff1_cluster_leader = ""
leader = False
multithread = False
manager = multiprocessing.Manager()
lock = manager.Lock()

first_zoom_scagnostics = {}
with open('Sample data sets/first_zoom_scagnostics.csv', mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        first_zoom_scagnostics[str(row[0] + ", " + row[1] + ", " + row[2])] = [float(str(row[3])[1:]), float(row[4]),
                                                                               float(row[5]), float(row[6]),
                                                                               float(row[7]), float(row[8]),
                                                                               float(row[9]), float(row[10]),
                                                                               float(str(row[11])[
                                                                                     0:len(str(row[11])) - 1])]
second_zoom_scagnostics = {}
with open('Sample data sets/second_zoom_scagnostics.csv', mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        second_zoom_scagnostics[str(row[0] + ", " + row[1] + ", " + row[2])] = [float(str(row[3])[1:]), float(row[4]),
                                                                                float(row[5]), float(row[6]),
                                                                                float(row[7]), float(row[8]),
                                                                                float(row[9]), float(row[10]),
                                                                                float(str(row[11])[
                                                                                      0:len(str(row[11])) - 1])]
third_zoom_scagnostics = {}
with open('Sample data sets/third_zoom_scagnostics.csv', mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        third_zoom_scagnostics[str(row[0] + ", " + row[1] + ", " + row[2])] = [float(str(row[3])[1:]), float(row[4]),
                                                                               float(row[5]), float(row[6]),
                                                                               float(row[7]), float(row[8]),
                                                                               float(row[9]), float(row[10]),
                                                                               float(str(row[11])[
                                                                                     0:len(str(row[11])) - 1])]


@app.route('/')
def index():
    global leader
    global multithread

    leader = False
    multithread = False
    return render_template('index.html')


@app.route('/leader')
def leader():
    global leader
    global multithread

    leader = True
    multithread = False
    return render_template('index.html')


@app.route('/multiprocs')
def multithread():
    global leader
    global multithread

    leader = False
    multithread = True
    return render_template('index.html')


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


@app.route('/log', methods=['GET', 'POST'])
def log():
    log_name = request.args['logName']
    new_line = request.args['newLine']

    with open('log_' + log_name + '.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_line])

    return ""


@app.route('/get-coords')
def get_coords():
    global left_view
    global right_view
    global current_scag
    global no_of_zoom
    global x
    global y
    global current_view_scagnostics
    global current_view_list

    left_view = False
    right_view = False
    current_scag = False

    no_of_zoom = int(request.args['zoomNo'])
    x_coord = ast.literal_eval(request.args['x'])
    y_coord = ast.literal_eval(request.args['y'])

    if no_of_zoom != 0:
        x = x_coord
    else:
        x = orig_x

    if no_of_zoom != 0:
        y = y_coord
    else:
        y = orig_y

    data_in_view = df.loc[(df["avg_vote"] >= x[0]) & (df["avg_vote"] <= x[1]) & (df["rlwide_gross_income"] >= y[0])
                          & (df["rlwide_gross_income"] <= y[1])]

    if data_in_view["avg_vote"].size <= 10 or data_in_view["rlwide_gross_income"].size <= 10:
        current_view_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    else:
        current_view_scagnostics = scagnostics(data_in_view["avg_vote"], data_in_view["rlwide_gross_income"])

        current_scag = True

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

    if leader:
        leader_set_left_view(current_view_list)
    else:
        naive_set_left_view(comparable_views, current_view_list, key_list, val_list)

    lock.release()

    while lock.locked():
        time.sleep(0.1)

    lock.acquire()

    if leader:
        leader_set_right_view(current_view_list)
    else:
        naive_set_right_view(comparable_views, current_view_list, key_list, val_list)

    lock.release()


def set_left_view_multi(comparable_views, current_view_list, spacing, left_result_scags):
    diff1 = 0
    diff1_scags = []

    comparable_views = dict(item for item in comparable_views)

    for view, scags in comparable_views.items():
        window = view.split("; ")
        window_x = ast.literal_eval(window[0])

        if (((x[0] - spacing) <= window_x[0] <= (x[1] + spacing)) and (
                (x[0] - spacing) <= window_x[1] <= (x[1] + spacing))):
            continue

        view_diff = (sum([(a - b) ** 2 for a, b in zip(scags, current_view_list)]))**(1/2)

        new_diff1 = max(diff1, view_diff)

        if new_diff1 == view_diff:
            diff1 = view_diff
            diff1_scags = scags

    if diff1_scags:
        left_result_scags.append(diff1_scags)


def naive_set_left_view(comparable_views, current_view_list, key_list, val_list):
    global left_view_x
    global left_view_y
    global diff1_scags
    global left_view

    left_view = False
    diff1 = 0


    if current_view_list == [0, 0, 0, 0, 0, 0, 0, 0, 0]:
        diff1_scags = current_view_list
        left_view_x = [0, 0]
        left_view_y = [0, 0]

        left_view = True

        return ""

    if no_of_zoom == 1:
        space = 1.0
    elif no_of_zoom == 2:
        space = 0.75
    else:
        space = 0.5

    if multithread:
        left_result_scags = manager.list()
        p = multiprocessing.Pool(4)

        comparable_list = list(comparable_views.items())
        chunks = [comparable_list[i:i + int(len(comparable_list) / 4)] for i in
                  range(0, len(comparable_list), int(len(comparable_list) / 4))]
        left_func = partial(set_left_view_multi, current_view_list=current_view_list, spacing=space,
                            left_result_scags=left_result_scags)
        p.map_async(left_func, chunks)
        p.close()
        p.join()

        best_diff = 0
        view = ""

        for i in range(len(left_result_scags)):
            diff = (sum([(a - b) ** 2 for a, b in zip(current_view_list, left_result_scags[i])]))**(1/2)
            if diff > best_diff:
                best_diff = diff
                view = key_list[val_list.index(left_result_scags[i])]
                diff1_scags = left_result_scags[i]

        left = view.split("; ")
        left_view_x = ast.literal_eval(left[0])
        left_view_y = ast.literal_eval(left[1])

    else:
        for view, scags in comparable_views.items():
            window = view.split("; ")
            window_x = ast.literal_eval(window[0])

            if (((x[0] - space) <= window_x[0] <= (x[1] + space)) and (
                    (x[0] - space) <= window_x[1] <= (x[1] + space))):
                continue

            view_diff = distance.euclidean(np.asarray(scags), np.asarray(current_view_list))

            new_diff1 = max(diff1, view_diff)

            if new_diff1 == view_diff:
                diff1 = view_diff
                diff1_scags = scags
                left = view.split("; ")
                left_view_x = ast.literal_eval(left[0])
                left_view_y = ast.literal_eval(left[1])

    left_view = True


def set_right_view_multi(comparable_views, current_view_list, key_list, val_list, spacing, right_result_scags):
    diff_1_2 = 0
    heap = []
    top_ten = [0 for i in range(10)]

    comparable_views = dict(item for item in comparable_views)

    for view, scags in comparable_views.items():
        window = view.split("; ")
        window_x = ast.literal_eval(window[0])

        if ((((left_view_x[0] - spacing) <= window_x[0] <= (left_view_x[1] + spacing)) and (
                (left_view_x[0] - spacing) <= window_x[1] <= (left_view_x[1] + spacing)))) or \
                (((x[0] - spacing) <= window_x[0] <= (x[1] + spacing))
                 and ((x[0] - spacing) <= window_x[1] <= (x[1] + spacing))):
            continue

        view_diff = (sum([(a - b) ** 2 for a, b in zip(scags, current_view_list)]))**(1/2)

        for ele in heap:
            if (ele - 0.05) <= view_diff <= (ele + 0.05):
                continue

        if len(heap) < 10:
            heappush(heap, view_diff)
        else:
            heappushpop(heap, view_diff)
        if view_diff in heap:
            top_ten[heap.index(view_diff)] = scags

    for ele in top_ten:
        if ele == 0:
            continue
        if (sum([(a - b) ** 2 for a, b in zip(ele, diff1_scags)]))**(1/2) > diff_1_2:
            diff_1_2 = (sum([(a - b) ** 2 for a, b in zip(ele, diff1_scags)]))**(1/2)
            diff2 = ele

    right_result_scags.append(diff2)


def naive_set_right_view(comparable_views, current_view_list, key_list, val_list):
    global right_view_x
    global right_view_y
    global diff2
    global right_view
    global diff_1_2
    global heap
    global top_ten
    global manager
    global lock

    right_view = False
    diff_1_2 = 0
    heap = []

    if current_view_list == [0, 0, 0, 0, 0, 0, 0, 0, 0]:
        diff2 = current_view_list
        right_view_x = [0, 0]
        right_view_y = [0, 0]

        right_view = True
        return ""

    if no_of_zoom == 1:
        space = 1.0
    elif no_of_zoom == 2:
        space = 0.75
    else:
        space = 0.5

    if multithread:
        right_result_scags = manager.list()
        p = multiprocessing.Pool(4)

        comparable_list = list(comparable_views.items())
        chunks = [comparable_list[i:i + int(len(comparable_list) / 4)] for i in
                  range(0, len(comparable_list), int(len(comparable_list) / 4))]
        right_func = partial(set_right_view_multi, current_view_list=current_view_list, key_list=key_list, val_list=val_list,
                             spacing=space, right_result_scags=right_result_scags)
        p.map_async(right_func, chunks)
        p.close()
        p.join()

        best_diff = 0
        view = ""

        for i in range(len(right_result_scags)):
            diff = (sum([(a - b) ** 2 for a, b in zip(current_view_list, right_result_scags[i])]))**(1/2)
            if diff > best_diff:
                best_diff = diff
                view = key_list[val_list.index(right_result_scags[i])]
                diff2 = right_result_scags[i]

        right = view.split("; ")
        right_view_x = ast.literal_eval(right[0])
        right_view_y = ast.literal_eval(right[1])

    else:
        diff_1_2 = 0
        heap = []
        top_ten = [0 for i in range(10)]
        view_list = [0 for i in range(10)]
        space = 0

        for view, scags in comparable_views.items():
            window = view.split("; ")
            window_x = ast.literal_eval(window[0])

            if ((((left_view_x[0] - space) <= window_x[0] <= (left_view_x[1] + space)) and
                 ((left_view_x[0] - space) <= window_x[1] <= (left_view_x[1] + space)))) or \
                    (((x[0] - space) <= window_x[0] <= (x[1] + space)) and
                     ((x[0] - space) <= window_x[1] <= (x[1] + space))):
                continue

            view_diff = distance.euclidean(np.asarray(scags), np.asarray(current_view_list))

            for ele in heap:
                if (ele - 0.05) <= view_diff <= (ele + 0.05):
                    continue

            if len(heap) < 10:
                heappush(heap, view_diff)
            else:
                heappushpop(heap, view_diff)
            if view_diff in heap:
                top_ten[heap.index(view_diff)] = scags
                view_list[heap.index(view_diff)] = view

        for ele in top_ten:
            if ele == 0:
                continue
            if distance.euclidean(np.asarray(ele), np.asarray(diff1_scags)) > diff_1_2:
                diff_1_2 = distance.euclidean(np.asarray(ele), np.asarray(diff1_scags))
                diff2 = ele

        if diff2 == 0 or len(heap) == 0:
            naive_set_right_view(comparable_views, current_view_list, key_list, val_list)

        view = key_list[val_list.index(diff2)]
        right = view.split("; ")
        right_view_x = ast.literal_eval(right[0])
        right_view_y = ast.literal_eval(right[1])

    right_view = True


def leader_set_left_view(current_view_list):
    global left_view_x
    global left_view_y
    global diff1_scags
    global left_view
    global diff1_cluster_leader

    diff1_leader = 0
    diff1 = 0

    left_view = False

    if current_view_list == [0, 0, 0, 0, 0, 0, 0, 0, 0]:
        diff1_scags = current_view_list
        left_view_x = [0, 0]
        left_view_y = [0, 0]

        left_view = True
        return ""

    if no_of_zoom == 1:
        comparable_leaders = first_cluster_leaders_views
        comparable_leaders_scags = first_cluster_leaders_scags
        comparable_subleaders = first_cluster_subleaders_views
        comparable_subleaders_scags = first_cluster_subleaders_scags
    elif no_of_zoom == 2:
        comparable_leaders = second_cluster_leaders_views
        comparable_leaders_scags = second_cluster_leaders_scags
        comparable_subleaders = second_cluster_subleaders_views
        comparable_subleaders_scags = second_cluster_subleaders_scags
    else:
        comparable_leaders = third_cluster_leaders_views
        comparable_leaders_scags = third_cluster_leaders_scags
        comparable_subleaders = third_cluster_subleaders_views
        comparable_subleaders_scags = third_cluster_subleaders_scags

    for leader in comparable_leaders.keys():

        view_diff = distance.euclidean(np.asarray(comparable_leaders_scags[leader]), np.asarray(current_view_list))

        diff1_leader = max(diff1_leader, view_diff)

        if diff1_leader == view_diff:
            diff1_cluster_leader = leader

    for subleader in comparable_subleaders[diff1_cluster_leader]:

        view_diff = distance.euclidean(np.asarray(comparable_subleaders_scags[subleader]),
                                       np.asarray(current_view_list))

        diff1 = max(diff1, view_diff)

        if diff1 == view_diff:
            diff1_scags = comparable_subleaders_scags[subleader]
            left = subleader.split("; ")
            left_view_x = ast.literal_eval(left[0])
            left_view_y = ast.literal_eval(left[1])

    left_view = True


def leader_set_right_view(current_view_list):
    global right_view_x
    global right_view_y
    global diff2
    global right_view

    diff2_leader = 0
    new_diff2 = 0

    right_view = False

    if current_view_list == [0, 0, 0, 0, 0, 0, 0, 0, 0]:
        diff2 = current_view_list
        right_view_x = [0, 0]
        right_view_y = [0, 0]

        right_view = True
        return ""

    if no_of_zoom == 1:
        comparable_leaders = first_cluster_leaders_views
        comparable_leaders_scags = first_cluster_leaders_scags
        comparable_subleaders = first_cluster_subleaders_views
        comparable_subleaders_scags = first_cluster_subleaders_scags
    elif no_of_zoom == 2:
        comparable_leaders = second_cluster_leaders_views
        comparable_leaders_scags = second_cluster_leaders_scags
        comparable_subleaders = second_cluster_subleaders_views
        comparable_subleaders_scags = second_cluster_subleaders_scags
    else:
        comparable_leaders = third_cluster_leaders_views
        comparable_leaders_scags = third_cluster_leaders_scags
        comparable_subleaders = third_cluster_subleaders_views
        comparable_subleaders_scags = third_cluster_subleaders_scags

    cluster_leader = ""

    for leader in comparable_leaders.keys():

        if leader == diff1_cluster_leader:
            continue

        view_diff = distance.euclidean(np.asarray(comparable_leaders_scags[leader]), np.asarray(current_view_list))

        diff2_leader = max(diff2_leader, view_diff)

        if diff2_leader == view_diff:
            cluster_leader = leader

    for subleader in comparable_subleaders[cluster_leader]:

        view_diff = distance.euclidean(np.asarray(comparable_subleaders_scags[subleader]),
                                       np.asarray(current_view_list))

        new_diff2 = max(new_diff2, view_diff)

        if new_diff2 == view_diff:
            diff2 = comparable_subleaders_scags[subleader]
            right = subleader.split("; ")
            right_view_x = ast.literal_eval(right[0])
            right_view_y = ast.literal_eval(right[1])

    right_view = True


def find_leader(comparable_views):
    cluster_leaders_views = {}
    cluster_leaders_scags = {}
    leader_list = []

    for view, scags in comparable_views.items():
        if len(leader_list) == 0:
            cluster_leaders_views[view] = []
            cluster_leaders_scags[view] = scags
            leader_list.append(view)
            continue

        in_cluster = False

        for leader in leader_list:
            leader_scag = cluster_leaders_scags[leader]
            similarity = distance.euclidean(leader_scag, scags)

            if similarity < 0.2:
                cluster_leaders_views[leader].append(view)
                in_cluster = True
                break

        if not in_cluster:
            cluster_leaders_views[view] = []
            cluster_leaders_scags[view] = scags
            leader_list.append(view)

    return cluster_leaders_views, cluster_leaders_scags


def find_subleaders(comparable_views):
    cluster_leader_views, cluster_leader_scags = find_leader(comparable_views)

    cluster_subleader_views = {}
    cluster_subleader_scags = {}
    subleader_list = []

    for leader, cluster in cluster_leader_views.items():

        if len(cluster) == 0:
            cluster_subleader_views[leader] = [leader]
            cluster_subleader_scags[leader] = comparable_views[leader]
            subleader_list.append(leader)
            continue

        cluster_subleader_views[leader] = [cluster[0]]
        cluster_subleader_scags[cluster[0]] = comparable_views[cluster[0]]
        subleader_list.append(cluster[0])

        for item in range(1, len(cluster)):
            in_cluster = False
            for subleader in subleader_list:
                subleader_scag = cluster_subleader_scags[subleader]
                similarity = distance.euclidean(subleader_scag, comparable_views[cluster[item]])

                if similarity < 0.1:
                    in_cluster = True
                    break

            if not in_cluster:
                cluster_subleader_views[leader].append(cluster[item])
                cluster_subleader_scags[cluster[item]] = comparable_views[cluster[item]]
                subleader_list.append(cluster[item])

    return cluster_leader_views, cluster_leader_scags, cluster_subleader_views, cluster_subleader_scags


first_cluster_leaders_views, first_cluster_leaders_scags, first_cluster_subleaders_views, \
first_cluster_subleaders_scags = find_subleaders(first_zoom_scagnostics)
second_cluster_leaders_views, second_cluster_leaders_scags, second_cluster_subleaders_views, \
second_cluster_subleaders_scags = find_subleaders(second_zoom_scagnostics)
third_cluster_leaders_views, third_cluster_leaders_scags, third_cluster_subleaders_views, \
third_cluster_subleaders_scags = find_subleaders(third_zoom_scagnostics)


@app.route('/get-left', methods=['GET', 'POST'])
def return_left_data():
    global left_view
    while left_view == False:
        time.sleep(0.100)

    return (df.loc[(df["avg_vote"] >= left_view_x[0]) & (df["avg_vote"] <= left_view_x[1]) & (
            df["rlwide_gross_income"] >= left_view_y[0]) & (df["rlwide_gross_income"] <=
                                                            left_view_y[1])]).to_csv()


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
    while left_view == False:
        time.sleep(0.100)
    left_scags = {"Outlying": diff1_scags[0], "Skewed": diff1_scags[1], "Clumpy": diff1_scags[2],
                  "Sparse": diff1_scags[3], "Striated": diff1_scags[4], "Convex": diff1_scags[5],
                  "Skinny": diff1_scags[6], "Stringy": diff1_scags[7], "Monotonic": diff1_scags[8]}
    return json.dumps(left_scags)

@app.route('/get-right-scagnostics', methods=['GET', 'POST'])
def return_right_scagnostics():
    while right_view == False:
        time.sleep(0.100)
    right_scags = {"Outlying": diff2[0], "Skewed": diff2[1], "Clumpy": diff2[2], "Sparse": diff2[3],
                   "Striated": diff2[4], "Convex": diff2[5], "Skinny": diff2[6], "Stringy": diff2[7],
                   "Monotonic": diff2[8]}
    return json.dumps(right_scags)


@app.route('/get-current-scagnostics', methods=['GET', 'POST'])
def return_current_scagnostics():
    while current_scag == False:
        time.sleep(0.100)
    right_scags = {"Outlying": current_view_list[0], "Skewed": current_view_list[1], "Clumpy": current_view_list[2],
                   "Sparse": current_view_list[3], "Striated": current_view_list[4], "Convex": current_view_list[5],
                   "Skinny": current_view_list[6], "Stringy": current_view_list[7], "Monotonic": current_view_list[8]}
    return json.dumps(right_scags)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
    #app.run()
