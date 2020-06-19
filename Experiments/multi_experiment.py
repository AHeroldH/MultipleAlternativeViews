import ast
from scipy.spatial import distance
import numpy as np
import csv
import pandas as pd
import os
import rpy2.robjects as robjects
import timeit
from heapq import heappushpop, heappush
import multiprocessing
import time
from functools import partial
import math

df = pd.read_csv('../movie-data.csv')
x = [1.0, 9.0]
y = [0.0, 1515047671.0]
path = '..'
diff1_scags = []
left_view_x = []
left_view_y = []


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


manager = multiprocessing.Manager()
lock = manager.Lock()


def set_left_view_multi(comparable_views, current_view_list, no_of_zoom, x, left_result_scags):
    diff1 = 0
    diff1_scags = current_view_list

    if no_of_zoom == 1:
        spacing = 0.5
    elif no_of_zoom == 2:
        spacing = 0.25
    else:
        spacing = 0.13

    comparable_views = dict(item for item in comparable_views)

    for view, scags in comparable_views.items():
        window = view.split("; ")
        window_x = ast.literal_eval(window[0])
        window_y = ast.literal_eval(window[1])

        if (((x[0] - spacing) <= window_x[0] <= (x[1] + spacing)) and (
                (x[0] - spacing) <= window_x[1] <= (x[1] + spacing))):
            continue

        view_diff = (sum([(a-b)** 2 for a,b in zip(scags, current_view_list)]))**(1/2)

        new_diff1 = max(diff1, view_diff)

        if new_diff1 == view_diff:
            diff1 = view_diff
            diff1_scags = scags
            left = view.split("; ")
            left_view_x = ast.literal_eval(left[0])
            left_view_y = ast.literal_eval(left[1])

    left_result_scags.append(diff1_scags)


def set_right_view_multi(comparable_views, current_view_list, key_list, val_list, no_of_zoom, x, right_result_scags):
    diff2 = current_view_list
    diff_1_2 = 0
    heap = []
    top_ten = [0 for i in range(10)]

    if no_of_zoom == 1:
        spacing = 0.5
    elif no_of_zoom == 2:
        spacing = 0.25
    else:
        spacing = 0.13

    comparable_views = dict(item for item in comparable_views)

    for view, scags in comparable_views.items():
        smaller_diff = False
        window = view.split("; ")
        window_x = ast.literal_eval(window[0])
        window_y = ast.literal_eval(window[1])

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


def get_example(x, y):
    example = df.loc[(df["avg_vote"] >= x[0]) & (df["avg_vote"] <= x[1]) & (df["rlwide_gross_income"] >= y[0])
                     & (df["rlwide_gross_income"] <= y[1])]

    example_scagnostics = scagnostics(example["avg_vote"], example["rlwide_gross_income"])

    example_list = [example_scagnostics['outlying'], example_scagnostics['skewed'],
                    example_scagnostics['clumpy'], example_scagnostics['sparse'],
                    example_scagnostics['striated'], example_scagnostics['convex'],
                    example_scagnostics['skinny'], example_scagnostics['stringy'],
                    example_scagnostics['monotonic']]

    return example_list


def start_left(procs, comparable_views, example_list, key_list, val_list, no_of_zoom, example_x):
    global left_view_x
    global diff1_scags
    left_result_scags = manager.list()
    p = multiprocessing.pool.ThreadPool(procs)

    comparable_list = list(comparable_views.items())
    chunks = [comparable_list[i:i + int(len(comparable_list) / procs)] for i in
              range(0, len(comparable_list), int(len(comparable_list) / procs))]
    left_func = partial(set_left_view_multi, current_view_list=example_list, no_of_zoom=no_of_zoom, x=example_x,
                        left_result_scags=left_result_scags)
    p.map_async(left_func, chunks)
    p.close()
    p.join()
    best_diff = 0
    view = ""

    for i in range(len(left_result_scags)):
        diff = (sum([(a - b) ** 2 for a, b in zip(example_list, left_result_scags[i])]))**(1/2)
        if diff > best_diff:
            best_diff = diff
            view = key_list[val_list.index(left_result_scags[i])]
            diff1_scags = left_result_scags[i]
    left = view.split("; ")
    left_view_x = ast.literal_eval(left[0])

    return left


def start_right(procs, comparable_views, example_list, key_list, val_list, no_of_zoom, example_x):
    right_result_scags = manager.list()
    p = multiprocessing.pool.ThreadPool(procs)

    comparable_list = list(comparable_views.items())
    chunks = [comparable_list[i:i + int(len(comparable_list) / procs)] for i in
              range(0, len(comparable_list), int(len(comparable_list) / procs))]
    right_func = partial(set_right_view_multi, current_view_list=example_list, key_list=key_list, val_list=val_list,
                        no_of_zoom=no_of_zoom, x=example_x, right_result_scags=right_result_scags)
    p.map_async(right_func, chunks)
    p.close()
    p.join()

    best_diff = 0
    view = ""

    for i in range(len(right_result_scags)):
        diff = (sum([(a - b) ** 2 for a, b in zip(example_list, right_result_scags[i])]))**(1/2)
        if diff > best_diff:
            best_diff = diff
            view = key_list[val_list.index(right_result_scags[i])]

    return view


def run_example(example, comparable_views, key_list, val_list, no_of_zoom, procs):
    example_x = []
    example_y = []
    example_list = []

    if example == 'first':
        if no_of_zoom == 1:
            example_x = [5.0, 9.0]
            example_y = [757523835.5, 1515047671.0]
            example_list = get_example(example_x, example_y)
        elif no_of_zoom == 2:
            example_x = [5.5, 7.5]
            example_y = [700000000, 1078761917.5]
            example_list = get_example(example_x, example_y)
        elif no_of_zoom == 3:
            example_x = [3.0, 4.0]
            example_y = [0.0, 189380958.88]
            example_list = get_example(example_x, example_y)
    elif example == 'second':
        if no_of_zoom == 1:
            example_x = [5.0, 9.0]
            example_y = [0.0, 757523835.5]
            example_list = get_example(example_x, example_y)
        elif no_of_zoom == 2:
            example_x = [4.0, 6.0]
            example_y = [0.0, 378761917.75]
            example_list = get_example(example_x, example_y)
        elif no_of_zoom == 3:
            example_x = [6.5, 7.5]
            example_y = [600000000, 789380958.88]
            example_list = get_example(example_x, example_y)
    elif example == 'third':
        if no_of_zoom == 1:
            example_x = [2.0, 6.0]
            example_y = [0.0, 757523835.5]
            example_list = get_example(example_x, example_y)
        elif no_of_zoom == 2:
            example_x = [6.0, 8.0]
            example_y = [300000000, 678761917.75]
            example_list = get_example(example_x, example_y)
        elif no_of_zoom == 3:
            example_x = [6.0, 7.0]
            example_y = [0.0, 189380958.88]
            example_list = get_example(example_x, example_y)
    elif example == 'fourth':
        if no_of_zoom == 1:
            example_x = [3.0, 7.0]
            example_y = [300000000, 1057523835.5]
            example_list = get_example(example_x, example_y)
        elif no_of_zoom == 2:
            example_x = [7.0, 9.0]
            example_y = [200000000, 578761917.75]
            example_list = get_example(example_x, example_y)
        elif no_of_zoom == 3:
            example_x = [7.0, 8.0]
            example_y = [200000000, 389380958.88]
            example_list = get_example(example_x, example_y)
    elif example == 'fifth':
        if no_of_zoom == 1:
            example_x = [4.5, 8.5]
            example_y = [300000000, 1057523835.5]
            example_list = get_example(example_x, example_y)
        elif no_of_zoom == 2:
            example_x = [3.0, 5.0]
            example_y = [0.0, 378761917.75]
            example_list = get_example(example_x, example_y)
        elif no_of_zoom == 3:
            example_x = [8.0, 9.0]
            example_y = [0.0, 189380958.88]
            example_list = get_example(example_x, example_y)

    left_t = timeit.Timer(lambda: start_left(procs, comparable_views, example_list, key_list,
                                             val_list, no_of_zoom, example_x))
    time_left = left_t.timeit(number=100)
    avg_time_left = time_left / 100

    right_t = timeit.Timer(lambda: start_right(procs, comparable_views, example_list, key_list,
                                               val_list, no_of_zoom, example_x))
    time_right = right_t.timeit(number=100)
    avg_time_right = time_right / 100

    return avg_time_left, avg_time_right, example_x, example_y


def run_experiment(no_of_zoom):
    dir = ""
    if no_of_zoom == 1:
        dir = "first_zoom_data"
    elif no_of_zoom == 2:
        dir = "../Sample data sets/second_zoom_data"
    else:
        dir = "../Sample data sets/third_zoom_data"
    for sample_set in os.listdir(dir + '/full_data'):
        if sample_set == '.DS_Store':
            continue
        comparable_views = {}
        with open(dir + '/full_data/' + sample_set, mode='r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                comparable_views[str(row[0] + ", " + row[1] + ", " + row[2])] = [float(str(row[3])[1:]),
                                                                                 float(row[4]), float(row[5]),
                                                                                 float(row[6]), float(row[7]),
                                                                                 float(row[8]), float(row[9]),
                                                                                 float(row[10]),
                                                                                 float(str(row[11])[
                                                                                       0:len(str(row[11])) - 1])]

        key_list = list(comparable_views.keys())
        val_list = list(comparable_views.values())

        for procs in range(2, 9, 2):
            avg_first_time_left, avg_first_time_right, first_example_x, first_example_y = run_example('first',
                                                                                                      comparable_views,
                                                                                                      key_list,
                                                                                                      val_list,
                                                                                                      no_of_zoom, procs)
            print("first done")

            avg_second_time_left, avg_second_time_right, second_example_x, second_example_y = run_example('second',
                                                                                                          comparable_views,
                                                                                                          key_list,
                                                                                                          val_list,
                                                                                                          no_of_zoom,
                                                                                                          procs)

            print("second done")

            avg_third_time_left, avg_third_time_right, third_example_x, third_example_y = run_example('third',
                                                                                                      comparable_views,
                                                                                                      key_list,
                                                                                                      val_list,
                                                                                                      no_of_zoom, procs)

            print("third done")

            avg_fourth_time_left, avg_fourth_time_right, fourth_example_x, fourth_example_y = run_example('fourth',
                                                                                                          comparable_views,
                                                                                                          key_list,
                                                                                                          val_list,
                                                                                                          no_of_zoom,
                                                                                                          procs)

            print("fourth done")

            avg_fifth_time_left, avg_fifth_time_right, fifth_example_x, fifth_example_y = run_example('fifth',
                                                                                                      comparable_views,
                                                                                                      key_list,
                                                                                                      val_list,
                                                                                                      no_of_zoom, procs)

            print("fifth done")

            avg_left = (avg_first_time_left + avg_second_time_left + avg_third_time_left + avg_fourth_time_left +
                        avg_fifth_time_left) / 5

            avg_right = (avg_first_time_right + avg_second_time_right + avg_third_time_right + avg_fourth_time_right +
                         avg_fifth_time_right) / 5

            row_count = len(pd.read_csv(dir + '/full_data/' + sample_set))

            with open('Time/thread_time_2.csv', 'a') as f:
                f.write("%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_first_time_left, row_count, procs, "[" +
                                                 str(first_example_x[0]) + "; " + str(first_example_x[1]) + "]; [" +
                                                 str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
                f.write("%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_first_time_right, row_count, procs, "[" +
                                                 str(first_example_x[0]) + "; " + str(first_example_x[1]) + "]; [" +
                                                 str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
                f.write("%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_second_time_left, row_count, procs, "[" +
                                                 str(second_example_x[0]) + "; " + str(second_example_x[1]) + "]; [" +
                                                 str(second_example_y[0]) + "; " + str(second_example_y[1]) + "]"))
                f.write("%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_second_time_right, row_count, procs, "[" +
                                                 str(second_example_x[0]) + "; " + str(second_example_x[1]) + "]; [" +
                                                 str(second_example_y[0]) + "; " + str(second_example_y[1]) + "]"))
                f.write("%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_third_time_left, row_count, procs, "[" +
                                                 str(third_example_x[0]) + "; " + str(third_example_x[1]) + "]; [" +
                                                 str(third_example_y[0]) + "; " + str(third_example_y[1]) + "]"))
                f.write("%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_third_time_right, row_count, procs, "[" +
                                                 str(third_example_x[0]) + "; " + str(third_example_x[1]) + "]; [" +
                                                 str(third_example_y[0]) + "; " + str(third_example_y[1]) + "]"))
                f.write("%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_fourth_time_left, row_count, procs, "[" +
                                                 str(fourth_example_x[0]) + "; " + str(fourth_example_x[1]) + "]; [" +
                                                 str(fourth_example_y[0]) + "; " + str(fourth_example_y[1]) + "]"))
                f.write("%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_fourth_time_right, row_count, procs, "[" +
                                                 str(fourth_example_x[0]) + "; " + str(fourth_example_x[1]) + "]; [" +
                                                 str(fourth_example_y[0]) + "; " + str(fourth_example_y[1]) + "]"))
                f.write("%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_fifth_time_left, row_count, procs, "[" +
                                                 str(fifth_example_x[0]) + "; " + str(fifth_example_x[1]) + "]; [" +
                                                 str(fifth_example_y[0]) + "; " + str(fifth_example_y[1]) + "]"))
                f.write("%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_fifth_time_right, row_count, procs, "[" +
                                                 str(fifth_example_x[0]) + "; " + str(fifth_example_x[1]) + "]; [" +
                                                 str(fifth_example_y[0]) + "; " + str(fifth_example_y[1]) + "]"))
                f.write("%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_left, row_count, procs, "average"))
                f.write("%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_right, row_count, procs, "average"))

        print("done with: " + sample_set)


if __name__ == '__main__':
    run_experiment(1)
    run_experiment(2)
    run_experiment(3)
