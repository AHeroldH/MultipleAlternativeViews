import pandas as pd
import numpy as np
import os
import rpy2.robjects as robjects

path = '.'
df = pd.read_csv('movie-data.csv')  # "world_wide_gross_income", "avg_vote", "votes", "reviews_from_critics", "country",
# "duration", "genre", "year"
x = [1.0, 9.0]
y = [0.0, 1346913161.0]
xRange = x[1] - x[0]
yRange = y[1] - y[0]


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


def compute_scags(zoom_level):
    x_start = x[0]
    y_start = y[0]
    x_end = x[1]
    y_end = y[1]
    xspacing = 0.0
    yspacing = 0.0
    scale = 0
    dict = {}

    if zoom_level == 1:
        scale = 2
        x_end = x[0] + (xRange - (xRange / scale) + 0.1)
        y_end = y[0] + (yRange - (yRange / scale) + 0.1)
        xspacing = 0.5
        yspacing = round(y[1]/(5829*4))
    elif zoom_level == 2:
        scale = 4
        x_end = x[0] + (xRange - (xRange / scale) + 0.1)
        y_end = y[0] + (yRange - (yRange / scale) + 0.1)
        xspacing = 0.25
        yspacing = round(y[1] / (5829*8))
    elif zoom_level == 3:
        scale = 8
        x_end = x[0] + (xRange - (xRange / scale) + 0.1)
        y_end = y[0] + (yRange - (yRange / scale) + 0.1)
        xspacing = 0.13
        yspacing = round(y[1] / (5829 * 16))

    for x_entry in np.arange(x_start, x_end, xspacing):
        for y_entry in np.arange(y_start, y_end, yspacing):
            data_in_view = df.loc[
                (df["avg_vote"] >= x_entry) & (df["avg_vote"] <= (x_entry + xRange / scale)) &
                (df["rlwide_gross_income"] >= y_entry) & (df["rlwide_gross_income"] <=
                                                          (y_entry + yRange / scale))]

            if data_in_view["avg_vote"].size <= 30 or data_in_view["rlwide_gross_income"].size <= 30:
                continue

            view_scags = scagnostics(data_in_view["avg_vote"], data_in_view["rlwide_gross_income"])

            dict["[" + str(x_entry) + ", " + str((x_entry + xRange / scale)) + "]; ["
                 + str(y_entry) + ", " + str((y_entry + yRange / scale)) + "]"] = \
                [view_scags['outlying'],
                 view_scags['skewed'],
                 view_scags['clumpy'],
                 view_scags['sparse'],
                 view_scags['striated'],
                 view_scags['convex'],
                 view_scags['skinny'],
                 view_scags['stringy'],
                 view_scags['monotonic']]

            if zoom_level == 1:
                with open('first_zoom_scagnostics.csv', 'w') as f:
                    for key in dict.keys():
                        f.write("%s,%s\n" % (key, dict[key]))
            elif zoom_level == 2:
                with open('second_zoom_scagnostics.csv', 'w') as f:
                    for key in dict.keys():
                        f.write("%s,%s\n" % (key, dict[key]))
            elif zoom_level == 3:
                with open('third_zoom_scagnostics.csv', 'w') as f:
                    for key in dict.keys():
                        f.write("%s,%s\n" % (key, dict[key]))
    return ""


if __name__ == '__main__':
    compute_scags(2)
