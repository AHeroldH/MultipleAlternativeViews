import ast
from scipy.spatial import distance
import numpy as np
import csv
import pandas as pd
import os
import rpy2.robjects as robjects
import timeit
from heapq import heappushpop, heappush
from functools import partial

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


def naive_set_left_view(comparable_views, current_view_list, no_of_zoom, x, y):
    global diff1_scags
    global left_view_x
    global left_view_y

    diff1 = 0

    if no_of_zoom == 1:
        space = 1.0
    elif no_of_zoom == 2:
        space = 0.75
    else:
        space = 0.5

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


def naive_set_right_view(comparable_views, current_view_list, key_list, val_list, no_of_zoom, x, y):
    if no_of_zoom == 1:
        space = 1.0
    elif no_of_zoom == 2:
        space = 0.75
    else:
        space = 0.5

    diff2 = 0
    diff_1_2 = 0
    heap = []
    three_best_diff2 = [0 for i in range(10)]
    view_list = [0 for i in range(10)]
    space = 0

    for view, scags in comparable_views.items():

        window = view.split("; ")
        window_x = ast.literal_eval(window[0])
        window_y = ast.literal_eval(window[1])

        if ((((left_view_x[0] - space) <= window_x[0] <= (left_view_x[1] + space)) and ((left_view_x[0] - space) <=
           window_x[1] <= (left_view_x[1] + space)))) or (((x[0] - space) <= window_x[0] <= (x[1] + space)) and ((x[0]
           - space) <= window_x[1] <= (x[1] + space))):
            continue

        view_diff = distance.sqeuclidean(np.asarray(scags), np.asarray(current_view_list))

        for ele in heap:
            if (ele - 0.05) <= view_diff <= (ele + 0.05):
                continue

        if len(heap) < 10:
            heappush(heap, view_diff)
        else:
            heappushpop(heap, view_diff)
        if view_diff in heap:
            three_best_diff2[heap.index(view_diff)] = scags
            view_list[heap.index(view_diff)] = view

    for ele in three_best_diff2:
        if ele == 0:
            continue
        if distance.euclidean(np.asarray(ele), np.asarray(diff1_scags)) > diff_1_2:
            diff_1_2 = distance.sqeuclidean(np.asarray(ele), np.asarray(diff1_scags))
            diff2 = ele

    view = key_list[val_list.index(diff2)]
    right = view.split("; ")
    right_view_x = ast.literal_eval(right[0])
    right_view_y = ast.literal_eval(right[1])


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


def run_example(example, comparable_views, key_list, val_list, no_of_zoom):
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

    left_t = timeit.Timer(lambda: naive_set_left_view(comparable_views, example_list, no_of_zoom, example_x, example_y))

    time_left = left_t.timeit(number=100)
    avg_time_left = time_left / 100

    right_t = timeit.Timer(lambda: naive_set_right_view(comparable_views, example_list, key_list, val_list, no_of_zoom,
                                                        example_x, example_y))

    time_right = right_t.timeit(number=100)
    avg_time_right = time_right / 100

    return avg_time_left, avg_time_right, example_x, example_y


if __name__ == '__main__':
    no_of_zoom = 3
    for sample_set in os.listdir('../Sample data sets/third_zoom_data/full_data'):
        comparable_views = {}
        with open('third_zoom_data/full_data/' + sample_set, mode='r') as infile:
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

        avg_first_time_left, avg_first_time_right, first_example_x, first_example_y = run_example('first',
        comparable_views, key_list, val_list, no_of_zoom)

        avg_second_time_left, avg_second_time_right, second_example_x, second_example_y = run_example('second',
        comparable_views, key_list, val_list, no_of_zoom)

        avg_third_time_left, avg_third_time_right, third_example_x, third_example_y = run_example('third',
        comparable_views, key_list, val_list, no_of_zoom)

        avg_fourth_time_left, avg_fourth_time_right, fourth_example_x, fourth_example_y = run_example('fourth',
        comparable_views, key_list, val_list, no_of_zoom)

        avg_fifth_time_left, avg_fifth_time_right, fifth_example_x, fifth_example_y = run_example('fifth',
        comparable_views, key_list, val_list, no_of_zoom)

        avg_left = (avg_first_time_left + avg_second_time_left + avg_third_time_left + avg_fourth_time_left +
                    avg_fifth_time_left) / 5

        avg_right = (avg_first_time_right + avg_second_time_right + avg_third_time_right + avg_fourth_time_right +
                     avg_fifth_time_right) / 5

        row_count = len(pd.read_csv('third_zoom_data/full_data/' + sample_set))

        with open('Time/naive_time_2.csv', 'a') as f:
            f.write("%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_first_time_left, row_count, "[" +
                                          str(first_example_x[0]) + "; " + str(first_example_x[1]) + "]; [" +
                                          str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_first_time_right, row_count, "[" +
                                          str(first_example_x[0]) + "; " + str(first_example_x[1]) + "]; [" +
                                          str(first_example_y[0]) + "; "+ str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_second_time_left, row_count, "[" +
                                          str(first_example_x[0]) + "; " + str(first_example_x[1]) + "]; [" +
                                          str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_second_time_right, row_count, "[" +
                                          str(first_example_x[0]) + "; " + str(first_example_x[1]) + "]; [" +
                                          str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_third_time_left, row_count, "[" +
                                          str(first_example_x[0]) + "; " + str(first_example_x[1]) + "]; [" +
                                          str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_third_time_right, row_count, "[" +
                                          str(first_example_x[0]) + "; " + str(first_example_x[1]) + "]; [" +
                                          str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_fourth_time_left, row_count, "[" +
                                          str(first_example_x[0]) + "; " + str(first_example_x[1]) + "]; [" +
                                          str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_fourth_time_right, row_count, "[" +
                                          str(first_example_x[0]) + "; " + str(first_example_x[1]) + "]; [" +
                                          str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_fifth_time_left, row_count, "[" +
                                          str(first_example_x[0]) + "; " + str(first_example_x[1]) + "]; [" +
                                          str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_fifth_time_right, row_count, "[" +
                                          str(first_example_x[0]) + "; " + str(first_example_x[1]) + "]; [" +
                                          str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_left, row_count, "average"))
            f.write("%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_right, row_count, "average"))

        print("done with: " + sample_set)
