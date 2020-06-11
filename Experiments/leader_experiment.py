import ast
from scipy.spatial import distance
import numpy as np
import csv
import pandas as pd
import os
import rpy2.robjects as robjects
import timeit

df = pd.read_csv('../movie-data.csv')
x = [1.0, 9.0]
y = [0.0, 1515047671.0]
path = '..'
diff1_scags = []
left_view_x = []
left_view_y = []
cluster_leaders_views = {}
cluster_leaders_scags = {}
cluster_subleaders_views = {}
cluster_subleaders_scags = {}
diff1_cluster_leader = ''

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


def leader_set_left_view(current_view_list):
    global diff1_cluster_leader

    diff1_leader = 0
    diff1 = 0
    diff1_cluster_leader = ''

    comparable_leaders = cluster_leaders_views
    comparable_leaders_scags = cluster_leaders_scags
    comparable_subleaders = cluster_subleaders_views
    comparable_subleaders_scags = cluster_subleaders_scags

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
    diff2_leader = 0
    new_diff2 = 0

    comparable_leaders = cluster_leaders_views
    comparable_leaders_scags = cluster_leaders_scags
    comparable_subleaders = cluster_subleaders_views
    comparable_subleaders_scags = cluster_subleaders_scags

    cluster_leader = ""

    #print("left cluster leader " + str(diff1_cluster_leader))

    for leader in comparable_leaders.keys():

        if leader == diff1_cluster_leader:
            continue

        view_diff = distance.euclidean(np.asarray(comparable_leaders_scags[leader]), np.asarray(current_view_list))

        diff2_leader = max(diff2_leader, view_diff)

        if diff2_leader == view_diff:
            cluster_leader = leader

    #print("right cluster leader " + str(cluster_leader))

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


def find_leader(comparable_views, leader_threshold):
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

            if similarity < leader_threshold:
                cluster_leaders_views[leader].append(view)
                in_cluster = True
                break

        if not in_cluster:
            cluster_leaders_views[view] = []
            cluster_leaders_scags[view] = scags
            leader_list.append(view)
            #print("leader: " + str(len(leader_list)))

    return cluster_leaders_views, cluster_leaders_scags


def find_subleaders(comparable_views, leader_threshold, subleader_threshold):
    cluster_leader_views, cluster_leader_scags = find_leader(comparable_views, leader_threshold)

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

                if similarity < subleader_threshold:
                    #cluster_subleader_views[subleader].append(cluster[item])
                    in_cluster = True
                    break

            if not in_cluster:
                cluster_subleader_views[leader].append(cluster[item])
                cluster_subleader_scags[cluster[item]] = comparable_views[cluster[item]]
                subleader_list.append(cluster[item])
                #print("subleader: " + str(len(subleader_list)))

    return cluster_leader_views, cluster_leader_scags, cluster_subleader_views, cluster_subleader_scags


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


def run_example(example, no_of_zoom):
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


    left_t = timeit.Timer(lambda: leader_set_left_view(example_list))
    time_left = left_t.timeit(number=100)
    avg_time_left = time_left / 100

    # right_t = timeit.Timer(lambda: leader_set_right_view(example_list))
    # time_right = right_t.timeit(number=100)
    # avg_time_right = time_right / 100

    return avg_time_left, example_x, example_y


def run_experiment(no_of_zoom):
    global cluster_leaders_views
    global cluster_leaders_scags
    global cluster_subleaders_views
    global cluster_subleaders_scags

    if no_of_zoom == 1:
        directory = "first_zoom_data/"
    elif no_of_zoom == 2:
        directory = "second_zoom_data/"
    else:
        directory = "third_zoom_data/"

    for sample_set in os.listdir(directory + 'full_data'):
        comparable_views = {}
        if sample_set == ".DS_Store":
            continue
        with open(directory + 'full_data/' + sample_set, mode='r') as infile:
            reader = csv.reader(infile)

            for row in reader:
                comparable_views[str(row[0] + ", " + row[1] + ", " + row[2])] = [float(str(row[3])[1:]),
                                                                                 float(row[4]), float(row[5]),
                                                                                 float(row[6]), float(row[7]),
                                                                                 float(row[8]), float(row[9]),
                                                                                 float(row[10]),
                                                                                 float(str(row[11])[
                                                                                       0:len(str(row[11])) - 1])]

        # for leader_threshold in np.arange(0.1, 1.0, 0.1):
        #     cluster_leaders_views, cluster_leaders_scags, cluster_subleaders_views, cluster_subleaders_scags = \
        #         find_subleaders(comparable_views, leader_threshold, 0.05)
        #
        #     if len(cluster_leaders_views) <= 1:
        #         continue

        leader_threshold = 0.001
        subleader_threshold = 0.00095

        leader_t = timeit.Timer(
            lambda: find_subleaders(comparable_views, leader_threshold, subleader_threshold))

        time_leader = leader_t.timeit(number=30)
        avg_time_leader = time_leader / 30

        cluster_leaders_views, cluster_leaders_scags, cluster_subleaders_views, cluster_subleaders_scags = \
            find_subleaders(comparable_views, leader_threshold, subleader_threshold)

        row_count = len(pd.read_csv(directory + 'full_data/' + sample_set))

        avg_first_time_left, first_example_x, first_example_y = run_example('first',no_of_zoom)

        avg_second_time_left, second_example_x, second_example_y = run_example('second',no_of_zoom)

        avg_third_time_left, third_example_x, third_example_y = run_example('third', no_of_zoom)

        avg_fourth_time_left, fourth_example_x, fourth_example_y = run_example('fourth',no_of_zoom)

        avg_fifth_time_left, fifth_example_x, fifth_example_y = run_example('fifth',no_of_zoom)

        avg_left = (avg_first_time_left + avg_second_time_left + avg_third_time_left + avg_fourth_time_left +
                    avg_fifth_time_left) / 5

        # avg_right = (avg_first_time_right + avg_second_time_right + avg_third_time_right + avg_fourth_time_right +
        #                         avg_fifth_time_right) / 5

        all_subleaders = 0
        for subleaders in cluster_subleaders_views.values():
            all_subleaders += len(subleaders)

        with open('Time/leader_time_worst.csv', 'a') as f:
            f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_first_time_left, row_count,
            leader_threshold, subleader_threshold, avg_time_leader, len(cluster_leaders_views),
            all_subleaders, "[" + str(first_example_x[0]) + "; " + str(first_example_x[1]) +
            "]; [" + str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            # f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_first_time_right, row_count,
            # leader_threshold, subleader_threshold, avg_time_leader, len(cluster_leaders_views),
            # all_subleaders, "[" + str(first_example_x[0]) + "; " + str(first_example_x[1]) +
            # "]; [" + str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_second_time_left, row_count,
            leader_threshold, subleader_threshold, avg_time_leader,len(cluster_leaders_views),
            all_subleaders, "[" + str(first_example_x[0]) + "; " + str(first_example_x[1]) +
            "]; [" + str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            # f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_second_time_right, row_count,
            # leader_threshold, subleader_threshold, avg_time_leader, len(cluster_leaders_views),
            # all_subleaders, "[" + str(first_example_x[0]) + "; " + str(first_example_x[1]) +
            # "]; [" + str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_third_time_left, row_count,
            leader_threshold, subleader_threshold, avg_time_leader, len(cluster_leaders_views),
            all_subleaders,"[" + str(first_example_x[0]) + "; " + str(first_example_x[1]) +
            "]; [" + str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            # f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_third_time_right, row_count,
            # leader_threshold, subleader_threshold, avg_time_leader, len(cluster_leaders_views),
            # all_subleaders, "[" + str(first_example_x[0]) + "; " + str(first_example_x[1]) +
            # "]; [" + str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_fourth_time_left, row_count,
            leader_threshold, subleader_threshold, avg_time_leader, len(cluster_leaders_views),
            all_subleaders, "[" + str(first_example_x[0]) + "; " + str(first_example_x[1]) +
            "]; [" + str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            # f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_fourth_time_right, row_count,
            # leader_threshold, subleader_threshold, avg_time_leader, len(cluster_leaders_views),
            # all_subleaders, "[" + str(first_example_x[0]) + "; " + str(first_example_x[1]) +
            # "]; [" + str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_fifth_time_left, row_count,
            leader_threshold, subleader_threshold, avg_time_leader, len(cluster_leaders_views),
            all_subleaders, "[" + str(first_example_x[0]) + "; " + str(first_example_x[1]) +
            "]; [" + str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            # f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_fifth_time_right, row_count,
            # leader_threshold, subleader_threshold, avg_time_leader, len(cluster_leaders_views),
            # all_subleaders, "[" + str(first_example_x[0]) + "; " + str(first_example_x[1]) +
            # "]; [" + str(first_example_y[0]) + "; " + str(first_example_y[1]) + "]"))
            f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'left', avg_left, row_count,
            leader_threshold,subleader_threshold, avg_time_leader, len(cluster_leaders_views),
            all_subleaders, "average"))
            # f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (no_of_zoom, 'right', avg_right, row_count,
            # leader_threshold, subleader_threshold, avg_time_leader, len(cluster_leaders_views),
            # all_subleaders, "average"))

        print("done with: " + sample_set)


if __name__ == '__main__':
    run_experiment(2)
    run_experiment(3)
