import pandas as pd
import matplotlib.pyplot as plt
import statistics
import seaborn as sns
import math
import numpy as np

data = pd.read_csv('Experiments/Time/leader_time_2_.csv')

# first = data.loc[(data['zoom_level'] == 1) & (data['example'] == 'average') & (data['number_of_samples'] == 2150) &
#                  (round(data['leader_threshold'], 2) == 0.2)]
# second = data.loc[(data['zoom_level'] == 2) & (data['example'] == 'average') & (data['number_of_samples'] == 4244) &
#                  (round(data['leader_threshold'], 2) == 0.2)]
# third = data.loc[(data['zoom_level'] == 3) & (data['example'] == 'average') & (data['number_of_samples'] == 3461) &
#                  (round(data['leader_threshold'], 2) == 0.2)]

#first_left = data.loc[(data['zoom_level'] == 1) & (data['example'] == 'average') & (data['alternative'] == 'left')]
                      # & (round(data['leader_threshold'], 2) == 0.2) & (round(data['subleader_threshold'], 2) == 0.10)]
#first_right = data.loc[(data['zoom_level'] == 1) & (data['example'] == 'average') & (data['alternative'] == 'right')]
                       # & (round(data['leader_threshold'], 2) == 0.2) & (round(data['subleader_threshold'], 2) == 0.10)]
#second_left = data.loc[(data['zoom_level'] == 2) & (data['example'] == 'average') & (data['alternative'] == 'left')]
                       # & (round(data['leader_threshold'], 2) == 0.2) & (round(data['subleader_threshold'], 2) == 0.10)]
#second_right = data.loc[(data['zoom_level'] == 2) & (data['example'] == 'average') & (data['alternative'] == 'right')]
                        # & (round(data['leader_threshold'], 2) == 0.2) & (round(data['subleader_threshold'], 2) == 0.10)]
#third_left = data.loc[(data['zoom_level'] == 3) & (data['example'] == 'average') & (data['alternative'] == 'left')]
                      # & (round(data['leader_threshold'], 2) == 0.2) & (round(data['subleader_threshold'], 2) == 0.10)]
#third_right = data.loc[(data['zoom_level'] == 3) & (data['example'] == 'average') & (data['alternative'] == 'right')]
                       # & (round(data['leader_threshold'], 2) == 0.2) & (round(data['subleader_threshold'], 2) == 0.10)]

first_left = data.loc[(data['zoom_level'] == 1) & (data['alternative'] == 'left') &
                      (round(data['leader_threshold'], 2) == 0.3) & (round(data['subleader_threshold'], 2) == 0.15)]
first_right = data.loc[(data['zoom_level'] == 1) & (data['alternative'] == 'right') &
                      (round(data['leader_threshold'], 2) == 0.3) & (round(data['subleader_threshold'], 2) == 0.15)]
second_left = data.loc[(data['zoom_level'] == 2) & (data['alternative'] == 'left') &
                      (round(data['leader_threshold'], 2) == 0.3) & (round(data['subleader_threshold'], 2) == 0.15)]
second_right = data.loc[(data['zoom_level'] == 2) & (data['alternative'] == 'right') &
                      (round(data['leader_threshold'], 2) == 0.3) & (round(data['subleader_threshold'], 2) == 0.15)]
third_left = data.loc[(data['zoom_level'] == 3) & (data['alternative'] == 'left') &
                      (round(data['leader_threshold'], 2) == 0.3) & (round(data['subleader_threshold'], 2) == 0.15)]
third_right = data.loc[(data['zoom_level'] == 3) & (data['alternative'] == 'right') &
                      (round(data['leader_threshold'], 2) == 0.3) & (round(data['subleader_threshold'], 2) == 0.15)]

first_avg_left = pd.DataFrame({'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
                               'leader_threshold': [], 'subleader_threshold': [], 'avg_leader_time': [],
                               'leaders': [], 'subleaders': []})
first_avg_right = pd.DataFrame({'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
                                'leader_threshold': [], 'subleader_threshold': [], 'avg_leader_time': [],
                               'leaders': [], 'subleaders': []})
second_avg_left = pd.DataFrame({'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
                                'leader_threshold': [], 'subleader_threshold': [], 'avg_leader_time': [],
                               'leaders': [], 'subleaders': []})
second_avg_right = pd.DataFrame(
    {'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
     'leader_threshold': [], 'subleader_threshold': [], 'avg_leader_time': [], 'leaders': [], 'subleaders': []})
third_avg_left = pd.DataFrame({'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
                               'leader_threshold': [], 'subleader_threshold': [], 'avg_leader_time': [],
                               'leaders': [], 'subleaders': []})
third_avg_right = pd.DataFrame({'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
                                'leader_threshold': [], 'subleader_threshold': [], 'avg_leader_time': [],
                               'leaders': [], 'subleaders': []})

first_left['leaders_subleaders'] = [row['leaders']+row['subleaders'] for i, row in first_left.iterrows()]
first_right['leaders_subleaders'] = [row['leaders']+row['subleaders'] for i, row in first_right.iterrows()]
second_left['leaders_subleaders'] = [row['leaders']+row['subleaders'] for i, row in second_left.iterrows()]
second_right['leaders_subleaders'] = [row['leaders']+row['subleaders'] for i, row in second_right.iterrows()]
third_left['leaders_subleaders'] = [row['leaders']+row['subleaders'] for i, row in third_left.iterrows()]
third_right['leaders_subleaders'] = [row['leaders']+row['subleaders'] for i, row in third_right.iterrows()]

first_left = first_left.sort_values(by=['number_of_samples'], ignore_index=True)
first_right = first_right.sort_values(by=['number_of_samples'], ignore_index=True)
second_left = second_left.sort_values(by=['number_of_samples'], ignore_index=True)
second_right = second_right.sort_values(by=['number_of_samples'], ignore_index=True)
third_left = third_left.sort_values(by=['number_of_samples'], ignore_index=True)
third_right = third_right.sort_values(by=['number_of_samples'], ignore_index=True)

index = 0
avg_index = 0

while index <= len(first_left) - 1:
    if index == len(first_left) - 1:
        first_avg_left.at[avg_index, 'zoom_level'] = first_left.at[index, 'zoom_level']
        first_avg_left.loc[avg_index, 'alternative'] = first_left.at[index, 'alternative']
        first_avg_left.at[avg_index, 'avg_time_in_seconds'] = first_left.at[index, 'avg_time_in_seconds']
        first_avg_left.at[avg_index, 'number_of_samples'] = first_left.at[index, 'number_of_samples']
        first_avg_left.at[avg_index, 'leader_threshold'] = round(first_left.at[index, 'leader_threshold'], 2)
        first_avg_left.at[avg_index, 'subleader_threshold'] = round(first_left.at[index, 'subleader_threshold'], 2)
        #first_avg_left.at[avg_index, 'avg_leader_time'] = first_left.at[index, 'avg_leader_time']
        first_avg_left.at[avg_index, 'leaders_subleaders'] = first_left.at[index, 'leaders_subleaders']
        first_avg_left.loc[avg_index, 'example'] = first_left.at[index, 'example']
        avg_index += 1
        index += 1
        continue
    diff = first_left.at[index + 1, 'number_of_samples'] - first_left.at[index, 'number_of_samples']
    if diff <= 10:
        first_avg_left.at[avg_index, 'zoom_level'] = first_left.at[index, 'zoom_level']
        first_avg_left.loc[avg_index, 'alternative'] = first_left.at[index, 'alternative']
        first_avg_left.at[avg_index, 'avg_time_in_seconds'] = statistics.mean(
            [first_left.at[index + 1, 'avg_time_in_seconds'], first_left.at[index, 'avg_time_in_seconds']])
        first_avg_left.at[avg_index, 'number_of_samples'] = statistics.mean(
            [first_left.at[index + 1, 'number_of_samples'], first_left.at[index, 'number_of_samples']])
        first_avg_left.at[avg_index, 'leader_threshold'] = round(first_left.at[index, 'leader_threshold'], 2)
        first_avg_left.at[avg_index, 'subleader_threshold'] = round(first_left.at[index, 'subleader_threshold'], 2)
        #first_avg_left.at[avg_index, 'avg_leader_time'] = statistics.mean(
        #    [float(first_left.at[index + 1, 'avg_leader_time']), float(first_left.at[index, 'avg_leader_time'])])
        first_avg_left.at[avg_index, 'leaders_subleaders'] = statistics.mean(
            [first_left.at[index + 1, 'leaders_subleaders'], first_left.at[index, 'leaders_subleaders']])
        first_avg_left.loc[avg_index, 'example'] = first_left.at[index, 'example']
        avg_index += 1
        index += 2
    else:
        first_avg_left.at[avg_index, 'zoom_level'] = first_left.at[index, 'zoom_level']
        first_avg_left.loc[avg_index, 'alternative'] = first_left.at[index, 'alternative']
        first_avg_left.at[avg_index, 'avg_time_in_seconds'] = first_left.at[index, 'avg_time_in_seconds']
        first_avg_left.at[avg_index, 'number_of_samples'] = first_left.at[index, 'number_of_samples']
        first_avg_left.at[avg_index, 'leader_threshold'] = round(first_left.at[index, 'leader_threshold'], 2)
        first_avg_left.at[avg_index, 'subleader_threshold'] = round(first_left.at[index, 'subleader_threshold'], 2)
        #first_avg_left.at[avg_index, 'avg_leader_time'] = first_left.at[index, 'avg_leader_time']
        first_avg_left.at[avg_index, 'leaders_subleaders'] = first_left.at[index, 'leaders_subleaders']
        first_avg_left.loc[avg_index, 'example'] = first_left.at[index, 'example']
        avg_index += 1
        index += 1

index = 0
avg_index = 0

while index <= len(first_right) - 1:
    if index == len(first_right) - 1:
        first_avg_right.at[avg_index, 'zoom_level'] = first_right.at[index, 'zoom_level']
        first_avg_right.loc[avg_index, 'alternative'] = first_right.at[index, 'alternative']
        first_avg_right.at[avg_index, 'avg_time_in_seconds'] = first_right.at[index, 'avg_time_in_seconds']
        first_avg_right.at[avg_index, 'number_of_samples'] = first_right.at[index, 'number_of_samples']
        first_avg_right.at[avg_index, 'leader_threshold'] = round(first_right.at[index, 'leader_threshold'], 2)
        first_avg_right.at[avg_index, 'subleader_threshold'] = round(first_right.at[index, 'subleader_threshold'], 2)
        #first_avg_right.at[avg_index, 'avg_leader_time'] = first_right.at[index, 'avg_leader_time']
        first_avg_right.at[avg_index, 'leaders_subleaders'] = first_right.at[index, 'leaders_subleaders']
        first_avg_right.loc[avg_index, 'example'] = first_right.at[index, 'example']
        avg_index += 1
        index += 1
        continue
    diff = first_right.at[index + 1, 'number_of_samples'] - first_right.at[index, 'number_of_samples']
    if diff <= 10:
        first_avg_right.at[avg_index, 'zoom_level'] = first_right.at[index, 'zoom_level']
        first_avg_right.loc[avg_index, 'alternative'] = first_right.at[index, 'alternative']
        first_avg_right.at[avg_index, 'avg_time_in_seconds'] = statistics.mean(
            [first_right.at[index + 1, 'avg_time_in_seconds'], first_right.at[index, 'avg_time_in_seconds']])
        first_avg_right.at[avg_index, 'number_of_samples'] = statistics.mean(
            [first_right.at[index + 1, 'number_of_samples'], first_right.at[index, 'number_of_samples']])
        first_avg_right.at[avg_index, 'leader_threshold'] = round(first_right.at[index, 'leader_threshold'], 2)
        first_avg_right.at[avg_index, 'subleader_threshold'] = round(first_right.at[index, 'subleader_threshold'], 2)
        #first_avg_right.at[avg_index, 'avg_leader_time'] = statistics.mean(
        #    [first_right.at[index + 1, 'avg_leader_time'], first_right.at[index, 'avg_leader_time']])
        first_avg_right.at[avg_index, 'leaders_subleaders'] = statistics.mean(
            [first_right.at[index + 1, 'leaders_subleaders'], first_right.at[index, 'leaders_subleaders']])
        first_avg_right.loc[avg_index, 'example'] = first_right.at[index, 'example']
        avg_index += 1
        index += 2
    else:
        first_avg_right.at[avg_index, 'zoom_level'] = first_right.at[index, 'zoom_level']
        first_avg_right.loc[avg_index, 'alternative'] = first_right.at[index, 'alternative']
        first_avg_right.at[avg_index, 'avg_time_in_seconds'] = first_right.at[index, 'avg_time_in_seconds']
        first_avg_right.at[avg_index, 'number_of_samples'] = first_right.at[index, 'number_of_samples']
        first_avg_right.at[avg_index, 'leader_threshold'] = round(first_right.at[index, 'leader_threshold'], 2)
        first_avg_right.at[avg_index, 'subleader_threshold'] = round(first_right.at[index, 'subleader_threshold'], 2)
        #first_avg_right.at[avg_index, 'avg_leader_time'] = first_right.at[index, 'avg_leader_time']
        first_avg_right.at[avg_index, 'leaders_subleaders'] = first_right.at[index, 'leaders_subleaders']
        first_avg_right.loc[avg_index, 'example'] = first_right.at[index, 'example']
        avg_index += 1
        index += 1

index = 0
avg_index = 0

while index <= len(second_left) - 1:
    if index == len(second_left) - 1:
        second_avg_left.at[avg_index, 'zoom_level'] = second_left.at[index, 'zoom_level']
        second_avg_left.loc[avg_index, 'alternative'] = second_left.at[index, 'alternative']
        second_avg_left.at[avg_index, 'avg_time_in_seconds'] = second_left.at[index, 'avg_time_in_seconds']
        second_avg_left.at[avg_index, 'number_of_samples'] = second_left.at[index, 'number_of_samples']
        second_avg_left.at[avg_index, 'leader_threshold'] = round(second_left.at[index, 'leader_threshold'], 2)
        second_avg_left.at[avg_index, 'subleader_threshold'] = round(second_left.at[index, 'subleader_threshold'], 2)
        #second_avg_left.at[avg_index, 'avg_leader_time'] = second_left.at[index, 'avg_leader_time']
        second_avg_left.at[avg_index, 'leaders_subleaders'] = second_left.at[index, 'leaders_subleaders']
        second_avg_left.loc[avg_index, 'example'] = second_left.at[index, 'example']
        avg_index += 1
        index += 1
        continue
    diff = second_left.at[index + 1, 'number_of_samples'] - second_left.at[index, 'number_of_samples']
    if diff <= 10:
        second_avg_left.at[avg_index, 'zoom_level'] = second_left.at[index, 'zoom_level']
        second_avg_left.loc[avg_index, 'alternative'] = second_left.at[index, 'alternative']
        second_avg_left.at[avg_index, 'avg_time_in_seconds'] = statistics.mean(
            [second_left.at[index + 1, 'avg_time_in_seconds'], second_left.at[index, 'avg_time_in_seconds']])
        second_avg_left.at[avg_index, 'number_of_samples'] = statistics.mean(
            [second_left.at[index + 1, 'number_of_samples'], second_left.at[index, 'number_of_samples']])
        second_avg_left.at[avg_index, 'leader_threshold'] = round(second_left.at[index, 'leader_threshold'], 2)
        second_avg_left.at[avg_index, 'subleader_threshold'] = round(second_left.at[index, 'subleader_threshold'], 2)
        #second_avg_left.at[avg_index, 'avg_leader_time'] = statistics.mean(
        #    [second_left.at[index + 1, 'avg_leader_time'], second_left.at[index, 'avg_leader_time']])
        second_avg_left.at[avg_index, 'leaders_subleaders'] = statistics.mean(
            [second_left.at[index + 1, 'leaders_subleaders'], second_left.at[index, 'leaders_subleaders']])
        second_avg_left.loc[avg_index, 'example'] = second_left.at[index, 'example']
        avg_index += 1
        index += 2
    else:
        second_avg_left.at[avg_index, 'zoom_level'] = second_left.at[index, 'zoom_level']
        second_avg_left.loc[avg_index, 'alternative'] = second_left.at[index, 'alternative']
        second_avg_left.at[avg_index, 'avg_time_in_seconds'] = second_left.at[index, 'avg_time_in_seconds']
        second_avg_left.at[avg_index, 'number_of_samples'] = second_left.at[index, 'number_of_samples']
        second_avg_left.at[avg_index, 'leader_threshold'] = round(second_left.at[index, 'leader_threshold'], 2)
        second_avg_left.at[avg_index, 'subleader_threshold'] = round(second_left.at[index, 'subleader_threshold'], 2)
        #second_avg_left.at[avg_index, 'avg_leader_time'] = second_left.at[index, 'avg_leader_time']
        second_avg_left.at[avg_index, 'leaders_subleaders'] = second_left.at[index, 'leaders_subleaders']
        second_avg_left.loc[avg_index, 'example'] = second_left.at[index, 'example']
        avg_index += 1
        index += 1

index = 0
avg_index = 0

while index <= len(second_right) - 1:
    if index == len(second_right) - 1:
        second_avg_right.at[avg_index, 'zoom_level'] = second_right.at[index, 'zoom_level']
        second_avg_right.loc[avg_index, 'alternative'] = second_right.at[index, 'alternative']
        second_avg_right.at[avg_index, 'avg_time_in_seconds'] = second_right.at[index, 'avg_time_in_seconds']
        second_avg_right.at[avg_index, 'number_of_samples'] = second_right.at[index, 'number_of_samples']
        second_avg_right.at[avg_index, 'leader_threshold'] = round(second_right.at[index, 'leader_threshold'], 2)
        second_avg_right.at[avg_index, 'subleader_threshold'] = round(second_right.at[index, 'subleader_threshold'], 2)
        #second_avg_right.at[avg_index, 'avg_leader_time'] = second_right.at[index, 'avg_leader_time']
        second_avg_right.at[avg_index, 'leaders_subleaders'] = second_right.at[index, 'leaders_subleaders']
        second_avg_right.loc[avg_index, 'example'] = second_right.at[index, 'example']
        avg_index += 1
        index += 1
        continue
    diff = second_right.at[index + 1, 'number_of_samples'] - second_right.at[index, 'number_of_samples']
    if diff <= 10:
        second_avg_right.at[avg_index, 'zoom_level'] = second_right.at[index, 'zoom_level']
        second_avg_right.loc[avg_index, 'alternative'] = second_right.at[index, 'alternative']
        second_avg_right.at[avg_index, 'avg_time_in_seconds'] = statistics.mean(
            [second_right.at[index + 1, 'avg_time_in_seconds'], second_right.at[index, 'avg_time_in_seconds']])
        second_avg_right.at[avg_index, 'number_of_samples'] = statistics.mean(
            [second_right.at[index + 1, 'number_of_samples'], second_right.at[index, 'number_of_samples']])
        second_avg_right.at[avg_index, 'leader_threshold'] = round(second_right.at[index, 'leader_threshold'], 2)
        second_avg_right.at[avg_index, 'subleader_threshold'] = round(second_right.at[index, 'subleader_threshold'], 2)
        #second_avg_right.at[avg_index, 'avg_leader_time'] = statistics.mean(
        #    [second_right.at[index + 1, 'avg_leader_time'], second_right.at[index, 'avg_leader_time']])
        second_avg_right.at[avg_index, 'leaders_subleaders'] = statistics.mean(
            [second_right.at[index + 1, 'leaders_subleaders'], second_right.at[index, 'leaders_subleaders']])
        second_avg_right.loc[avg_index, 'example'] = second_right.at[index, 'example']
        avg_index += 1
        index += 2
    else:
        second_avg_right.at[avg_index, 'zoom_level'] = second_right.at[index, 'zoom_level']
        second_avg_right.loc[avg_index, 'alternative'] = second_right.at[index, 'alternative']
        second_avg_right.at[avg_index, 'avg_time_in_seconds'] = second_right.at[index, 'avg_time_in_seconds']
        second_avg_right.at[avg_index, 'number_of_samples'] = second_right.at[index, 'number_of_samples']
        second_avg_right.at[avg_index, 'leader_threshold'] = round(second_right.at[index, 'leader_threshold'], 2)
        second_avg_right.at[avg_index, 'subleader_threshold'] = round(second_right.at[index, 'subleader_threshold'], 2)
        #second_avg_right.at[avg_index, 'avg_leader_time'] = second_right.at[index, 'avg_leader_time']
        second_avg_right.at[avg_index, 'leaders_subleaders'] = second_right.at[index, 'leaders_subleaders']
        second_avg_right.loc[avg_index, 'example'] = second_right.at[index, 'example']
        avg_index += 1
        index += 1

index = 0
avg_index = 0

while index <= len(third_left) - 1:
    if index == len(third_left) - 1:
        third_avg_left.at[avg_index, 'zoom_level'] = third_left.at[index, 'zoom_level']
        third_avg_left.loc[avg_index, 'alternative'] = third_left.at[index, 'alternative']
        third_avg_left.at[avg_index, 'avg_time_in_seconds'] = third_left.at[index, 'avg_time_in_seconds']
        third_avg_left.at[avg_index, 'number_of_samples'] = third_left.at[index, 'number_of_samples']
        third_avg_left.at[avg_index, 'leader_threshold'] = round(third_left.at[index, 'leader_threshold'], 2)
        third_avg_left.at[avg_index, 'subleader_threshold'] = round(third_left.at[index, 'subleader_threshold'], 2)
        #third_avg_left.at[avg_index, 'avg_leader_time'] = third_left.at[index, 'avg_leader_time']
        third_avg_left.at[avg_index, 'leaders_subleaders'] = third_left.at[index, 'leaders_subleaders']
        third_avg_left.loc[avg_index, 'example'] = third_left.at[index, 'example']
        avg_index += 1
        index += 1
        continue
    diff = third_left.at[index + 1, 'number_of_samples'] - third_left.at[index, 'number_of_samples']
    if diff <= 10:
        third_avg_left.at[avg_index, 'zoom_level'] = third_left.at[index, 'zoom_level']
        third_avg_left.loc[avg_index, 'alternative'] = third_left.at[index, 'alternative']
        third_avg_left.at[avg_index, 'avg_time_in_seconds'] = statistics.mean(
            [third_left.at[index + 1, 'avg_time_in_seconds'], third_left.at[index, 'avg_time_in_seconds']])
        third_avg_left.at[avg_index, 'number_of_samples'] = statistics.mean(
            [third_left.at[index + 1, 'number_of_samples'], third_left.at[index, 'number_of_samples']])
        third_avg_left.at[avg_index, 'leader_threshold'] = round(third_left.at[index, 'leader_threshold'], 2)
        third_avg_left.at[avg_index, 'subleader_threshold'] = round(third_left.at[index, 'subleader_threshold'], 2)
        #third_avg_left.at[avg_index, 'avg_leader_time'] = statistics.mean(
        #    [third_left.at[index + 1, 'avg_leader_time'], third_left.at[index, 'avg_leader_time']])
        third_avg_left.at[avg_index, 'leaders_subleaders'] = statistics.mean(
            [third_left.at[index + 1, 'leaders_subleaders'], third_left.at[index, 'leaders_subleaders']])
        third_avg_left.loc[avg_index, 'example'] = third_left.at[index, 'example']
        avg_index += 1
        index += 2
    else:
        third_avg_left.at[avg_index, 'zoom_level'] = third_left.at[index, 'zoom_level']
        third_avg_left.loc[avg_index, 'alternative'] = third_left.at[index, 'alternative']
        third_avg_left.at[avg_index, 'avg_time_in_seconds'] = third_left.at[index, 'avg_time_in_seconds']
        third_avg_left.at[avg_index, 'number_of_samples'] = third_left.at[index, 'number_of_samples']
        third_avg_left.at[avg_index, 'leader_threshold'] = round(third_left.at[index, 'leader_threshold'], 2)
        third_avg_left.at[avg_index, 'subleader_threshold'] = round(third_left.at[index, 'subleader_threshold'], 2)
        #third_avg_left.at[avg_index, 'avg_leader_time'] = third_left.at[index, 'avg_leader_time']
        third_avg_left.at[avg_index, 'leaders_subleaders'] = third_left.at[index, 'leaders_subleaders']
        third_avg_left.loc[avg_index, 'example'] = third_left.at[index, 'example']
        avg_index += 1
        index += 1

index = 0
avg_index = 0

while index <= len(third_right) - 1:
    if index == len(third_right) - 1:
        third_avg_right.at[avg_index, 'zoom_level'] = third_right.at[index, 'zoom_level']
        third_avg_right.loc[avg_index, 'alternative'] = third_right.at[index, 'alternative']
        third_avg_right.at[avg_index, 'avg_time_in_seconds'] = third_right.at[index, 'avg_time_in_seconds']
        third_avg_right.at[avg_index, 'number_of_samples'] = third_right.at[index, 'number_of_samples']
        third_avg_right.at[avg_index, 'leader_threshold'] = round(third_right.at[index, 'leader_threshold'], 2)
        third_avg_right.at[avg_index, 'subleader_threshold'] = round(third_right.at[index, 'subleader_threshold'], 2)
        #third_avg_right.at[avg_index, 'avg_leader_time'] = third_right.at[index, 'avg_leader_time']
        third_avg_right.at[avg_index, 'leaders_subleaders'] = third_right.at[index, 'leaders_subleaders']
        third_avg_right.loc[avg_index, 'example'] = third_right.at[index, 'example']
        avg_index += 1
        index += 1
        continue
    diff = third_right.at[index + 1, 'number_of_samples'] - third_right.at[index, 'number_of_samples']
    if diff <= 10:
        third_avg_right.at[avg_index, 'zoom_level'] = third_right.at[index, 'zoom_level']
        third_avg_right.loc[avg_index, 'alternative'] = third_right.at[index, 'alternative']
        third_avg_right.at[avg_index, 'avg_time_in_seconds'] = statistics.mean(
            [third_right.at[index + 1, 'avg_time_in_seconds'], third_right.at[index, 'avg_time_in_seconds']])
        third_avg_right.at[avg_index, 'number_of_samples'] = statistics.mean(
            [third_right.at[index + 1, 'number_of_samples'], third_right.at[index, 'number_of_samples']])
        third_avg_right.at[avg_index, 'leader_threshold'] = round(third_right.at[index, 'leader_threshold'], 2)
        third_avg_right.at[avg_index, 'subleader_threshold'] = round(third_right.at[index, 'subleader_threshold'], 2)
        #third_avg_right.at[avg_index, 'avg_leader_time'] = statistics.mean(
        #    [third_right.at[index + 1, 'avg_leader_time'], third_right.at[index, 'avg_leader_time']])
        third_avg_right.at[avg_index, 'leaders_subleaders'] = statistics.mean(
            [third_right.at[index + 1, 'leaders_subleaders'], third_right.at[index, 'leaders_subleaders']])
        third_avg_right.loc[avg_index, 'example'] = third_right.at[index, 'example']
        avg_index += 1
        index += 2
    else:
        third_avg_right.at[avg_index, 'zoom_level'] = third_right.at[index, 'zoom_level']
        third_avg_right.loc[avg_index, 'alternative'] = third_right.at[index, 'alternative']
        third_avg_right.at[avg_index, 'avg_time_in_seconds'] = third_right.at[index, 'avg_time_in_seconds']
        third_avg_right.at[avg_index, 'number_of_samples'] = third_right.at[index, 'number_of_samples']
        third_avg_right.at[avg_index, 'leader_threshold'] = round(third_right.at[index, 'leader_threshold'], 2)
        third_avg_right.at[avg_index, 'subleader_threshold'] = round(third_right.at[index, 'subleader_threshold'], 2)
        #third_avg_right.at[avg_index, 'avg_leader_time'] = third_right.at[index, 'avg_leader_time']
        third_avg_right.at[avg_index, 'leaders_subleaders'] = third_right.at[index, 'leaders_subleaders']
        third_avg_right.loc[avg_index, 'example'] = third_right.at[index, 'example']
        avg_index += 1
        index += 1

# combined = pd.concat([first_avg_left, second_avg_left, third_avg_left],
#            ignore_index=True)
#
# dummy = np.linspace(1,20000,100)
# y = [np.log(x) for x in np.nditer(dummy)]
#
# data['complexity'] = [(row['avg_time_in_seconds']*1000000)/(row['leaders']*math.log2(row['leaders'])) for i, row in data.iterrows()]
# data['complexity2'] = [row['leaders']*math.log2(row['leaders']) if row['leaders'] > 1 else row['number_of_samples'] for i, row in data.iterrows()]
# sns.set()
# ax = plt.gca()
# data.plot(kind='scatter', x='complexity2', y='complexity', ax=ax)

# first_left['complexity'] = [(row['avg_time_in_seconds']*1000000000)/(row['number_of_samples']*9) for i, row in first_left.iterrows()]
# second_left['complexity'] = [(row['avg_time_in_seconds']*1000000000)/(row['number_of_samples']*9) for i, row in second_left.iterrows()]
# third_left['complexity'] = [(row['avg_time_in_seconds']*1000000000)/(row['number_of_samples']*9) for i, row in third_left.iterrows()]
#
# first.plot(kind='line', x='subleader_threshold', y='subleaders', color='blue', ax=ax, label='First zoom')
# second.plot(kind='line', x='subleader_threshold', y='subleaders', color='green', ax=ax, label='Second zoom')
# third.plot(kind='line', x='subleader_threshold', y='subleaders', color='red', ax=ax, label='Third zoom')

# second_1_05 = second_avg_left.loc[(second_avg_left['leader_threshold'] == 0.5) & (second_avg_left['subleader_threshold']
#                                                                                   == 0.05)]
# second_2_05 = second_avg_left.loc[(second_avg_left['leader_threshold'] == 0.5) & (second_avg_left['subleader_threshold']
#                                                                                   == 0.15)]
# second_3_05 = second_avg_left.loc[(second_avg_left['leader_threshold'] == 0.5) & (second_avg_left['subleader_threshold']
#                                                                                   == 0.25)]
# second_4_05 = second_avg_left.loc[(second_avg_left['leader_threshold'] == 0.5) & (second_avg_left['subleader_threshold']
#                                                                                   == 0.35)]
# second_5_05 = second_avg_left.loc[(second_avg_left['leader_threshold'] == 0.5) & (second_avg_left['subleader_threshold']
#                                                                                   == 0.45)]
#
# sns.set()
# ax = plt.gca()
# second_1_05.plot(kind='line', x='leaders_subleaders', y='avg_time_in_seconds', color='blue', ax=ax, label='Leader: 0.1, subleader: 0.5')
# second_2_05.plot(kind='line', x='leaders_subleaders', y='avg_time_in_seconds', color='green', ax=ax, label='Leader: 0.2, subleader: 0.5')
# second_3_05.plot(kind='line', x='leaders_subleaders', y='avg_time_in_seconds', color='red', ax=ax, label='Leader: 0.3, subleader: 0.5')
# second_4_05.plot(kind='line', x='leaders_subleaders', y='avg_time_in_seconds', color='purple', ax=ax, label='Leader: 0.4, subleader: 0.5')
# second_5_05.plot(kind='line', x='leaders_subleaders', y='avg_time_in_seconds', color='black', ax=ax, label='Leader: 0.5, subleader: 0.5')
# plt.xlabel('Number of leaders and subleaders')
# plt.ylabel('Time in seconds')

# sns.set()
#
# # fig, axs = plt.subplots(1, 2)
# # fig.set_figwidth(14)
#
# ax = plt.gca()
# #first_left.plot(kind='scatter', x='number_of_samples', y='avg_leader_time', color='blue', ax=ax)
# #second_left.plot(kind='scatter', x='number_of_samples', y='avg_leader_time', color='green', ax=ax)
# third_left.plot(kind='scatter', x='number_of_samples', y='avg_leader_time', color='red', ax=ax)
#
# plt.xlabel('Number of samples')
# plt.ylabel('Time in seconds')

# axs[0].set_title('Left alternative')
# axs[0].set_xlabel('Number of leaders and subleaders')
# axs[0].set_ylabel('Time in seconds')

# first_avg_right.plot(kind='line', x='leaders_subleaders', y='avg_time_in_seconds', color='blue', ax=axs[1],
#                      label='First zoom')
# second_avg_right.plot(kind='line', x='leaders_subleaders', y='avg_time_in_seconds', color='green', ax=axs[1],
#                       label='Second zoom')
# third_avg_right.plot(kind='line', x='leaders_subleaders', y='avg_time_in_seconds', color='red', ax=axs[1],
#                      label='Third zoom')
# axs[1].set_title('Right alternative')
# axs[1].set_xlabel('Number of leaders and subleaders')
# axs[1].set_ylabel('Time in seconds')

first_left_first = first_avg_left.loc[first_avg_left['example'] == '[5.0;  9.0];  [757523835.5;  1515047671.0]']
first_left_second = first_avg_left.loc[first_avg_left['example'] == '[5.0;  9.0];  [0.0;  757523835.5]']
first_left_third = first_avg_left.loc[first_avg_left['example'] == '[2.0;  6.0];  [0.0;  757523835.5]']
first_left_fourth = first_avg_left.loc[first_avg_left['example'] == '[3.0;  7.0];  [300000000;  1057523835.5]']
first_left_fifth = first_avg_left.loc[first_avg_left['example'] == '[4.5;  8.5];  [300000000;  1057523835.5]']
first_right_first = first_avg_right.loc[first_avg_right['example'] == '[5.0;  9.0];  [757523835.5;  1515047671.0]']
first_right_second = first_avg_right.loc[first_avg_right['example'] == '[5.0;  9.0];  [0.0;  757523835.5]']
first_right_third = first_avg_right.loc[first_avg_right['example'] == '[2.0;  6.0];  [0.0;  757523835.5]']
first_right_fourth = first_avg_right.loc[first_avg_right['example'] == '[3.0;  7.0];  [300000000;  1057523835.5]']
first_right_fifth = first_avg_right.loc[first_avg_right['example'] == '[4.5;  8.5];  [300000000;  1057523835.5]']
second_left_first = second_avg_left.loc[second_avg_left['example'] == '[5.5;  7.5];  [700000000;  1078761917.5]']
second_left_second = second_avg_left.loc[second_avg_left['example'] == '[4.0;  6.0];  [0.0;  378761917.75]']
second_left_third = second_avg_left.loc[second_avg_left['example'] == '[6.0;  8.0];  [300000000;  678761917.75]']
second_left_fourth = second_avg_left.loc[second_avg_left['example'] == '[7.0;  9.0];  [200000000;  578761917.75]']
second_left_fifth = second_avg_left.loc[second_avg_left['example'] == '[3.0;  5.0];  [0.0;  378761917.75]']
second_right_first = second_avg_right.loc[second_avg_right['example'] == '[5.5;  7.5];  [700000000;  1078761917.5]']
second_right_second = second_avg_right.loc[second_avg_right['example'] == '[4.0;  6.0];  [0.0;  378761917.75]']
second_right_third = second_avg_right.loc[second_avg_right['example'] == '[6.0;  8.0];  [300000000;  678761917.75]']
second_right_fourth = second_avg_right.loc[second_avg_right['example'] == '[7.0;  9.0];  [200000000;  578761917.75]']
second_right_fifth = second_avg_right.loc[second_avg_right['example'] == '[3.0;  5.0];  [0.0;  378761917.75]']
third_left_first = third_avg_left.loc[third_avg_left['example'] == '[3.0;  4.0];  [0.0;  189380958.88]']
third_left_second = third_avg_left.loc[third_avg_left['example'] == '[6.5;  7.5];  [600000000;  789380958.88]']
third_left_third = third_avg_left.loc[third_avg_left['example'] == '[6.0;  7.0];  [0.0;  189380958.88]']
third_left_fourth = third_avg_left.loc[third_avg_left['example'] == '[7.0;  8.0];  [200000000;  389380958.88]']
third_left_fifth = third_avg_left.loc[third_avg_left['example'] == '[8.0;  9.0];  [0.0;  189380958.88]']
third_right_first = third_avg_right.loc[third_avg_right['example'] == '[3.0;  4.0];  [0.0;  189380958.88]']
third_right_second = third_avg_right.loc[third_avg_right['example'] == '[6.5;  7.5];  [600000000;  789380958.88]']
third_right_third = third_avg_right.loc[third_avg_right['example'] == '[6.0;  7.0];  [0.0;  189380958.88]']
third_right_fourth = third_avg_right.loc[third_avg_right['example'] == '[7.0;  8.0];  [200000000;  389380958.88]']
third_right_fifth = third_avg_right.loc[third_avg_right['example'] == '[8.0;  9.0];  [0.0;  189380958.88]']

sns.set()

fig, axs = plt.subplots(3, 2)
fig.set_figheight(11)
fig.set_figwidth(10)
fig.tight_layout(pad=3.0)
i = np.unravel_index(0, axs.shape)
first_left_first.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[i],
                      label='First example')
first_left_second.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[i],
                       label='Second example')
first_left_third.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[i],
                      label='Third example')
first_left_fourth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[i],
                       label='Fourth example')
first_left_fifth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[i],
                      label='Fifth example')
axs[i].set_title('First zoom - Left Alternative')
axs[i].set_xlabel('Number of samples')
axs[i].set_ylabel('Time in seconds')

i = np.unravel_index(2, axs.shape)
second_left_first.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[i],
                       label='First example')
second_left_second.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[i],
                        label='Second example')
second_left_third.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[i],
                       label='Third example')
second_left_fourth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[i],
                        label='Fourth example')
second_left_fifth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[i],
                       label='Fifth example')
axs[i].set_title('Second zoom - Left Alternative')
axs[i].set_xlabel('Number of samples')
axs[i].set_ylabel('Time in seconds')

i = np.unravel_index(4, axs.shape)
third_left_first.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[i],
                      label='First example')
third_left_second.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[i],
                       label='Second example')
third_left_third.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[i],
                      label='Third example')
third_left_fourth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[i],
                       label='Fourth example')
third_left_fifth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[i],
                      label='Fifth example')
axs[i].set_title('Third zoom - Left Alternative')
axs[i].set_xlabel('Number of samples')
axs[i].set_ylabel('Time in seconds')

i = np.unravel_index(1, axs.shape)
first_right_first.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[i],
                       label='First example')
first_right_second.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[i],
                        label='Second example')
first_right_third.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[i],
                       label='Third example')
first_right_fourth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[i],
                        label='Fourth example')
first_right_fifth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[i],
                       label='Fifth example')
axs[i].set_title('First zoom - Right Alternative')
axs[i].set_xlabel('Number of samples')
axs[i].set_ylabel('Time in seconds')

i = np.unravel_index(3, axs.shape)
second_right_first.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[i],
                        label='First example')
second_right_second.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[i],
                         label='Second example')
second_right_third.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[i],
                        label='Third example')
second_right_fourth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[i],
                         label='Fourth example')
second_right_fifth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[i],
                        label='Fifth example')
axs[i].set_title('Second zoom - Right Alternative')
axs[i].set_xlabel('Number of samples')
axs[i].set_ylabel('Time in seconds')

i = np.unravel_index(5, axs.shape)
third_right_first.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[i],
                       label='First example')
third_right_second.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[i],
                        label='Second example')
third_right_third.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[i],
                       label='Third example')
third_right_fourth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[i],
                        label='Fourth example')
third_right_fifth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[i],
                       label='Fifth example')
axs[i].set_title('Third zoom - Right Alternative')
axs[i].set_xlabel('Number of samples')
axs[i].set_ylabel('Time in seconds')

# sns.set()
# ax = plt.gca()
#
# combined.plot(kind='scatter', x='number_of_samples', y='complexity', color='blue', ax=ax)
#ax.axhline(y=1, color='green', label='$c$')
# ax.axhline(y=35, color='purple', label='$c_2$')
#ax.axvline(x=40000, color='red', label='$n_0$')
#
#plt.ylabel('Time in microseconds / leaders * log(leaders)')
#plt.xlabel('Leaders * log(leaders)')
#handles, labels = ax.get_legend_handles_labels()
#plt.legend(handles=handles[0:], labels=labels)
plt.savefig('leader_example_comparison_3_15.png')
plt.show()
