import pandas as pd
import matplotlib.pyplot as plt
import statistics
import seaborn as sns
import math
import numpy as np

leader = pd.read_csv('../Experiments/Time/leader_time_2.csv')
naive = pd.read_csv('../Experiments/Time/naive_time_2.csv')
procs = pd.read_csv('../Experiments/Time/multi_time_2.csv')
threads = pd.read_csv('../Experiments/Time/thread_time_2.csv')

first_leader_left = leader.loc[(leader['zoom_level'] == 1) & (leader['example'] == 'average') &
                               (round(leader['leader_threshold'], 2) == 0.2) &
                               (round(leader['subleader_threshold'], 2) == 0.1) & (leader['alternative'] == 'left')]
first_leader_right = leader.loc[(leader['zoom_level'] == 1) & (leader['example'] == 'average') &
                                (round(leader['leader_threshold'], 2) == 0.2) &
                                (round(leader['subleader_threshold'], 2) == 0.1) & (leader['alternative'] == 'right')]
second_leader_left = leader.loc[(leader['zoom_level'] == 2) & (leader['example'] == 'average') &
                                (round(leader['leader_threshold'], 2) == 0.2) &
                                (round(leader['subleader_threshold'], 2) == 0.1) & (leader['alternative'] == 'left')]
second_leader_right = leader.loc[(leader['zoom_level'] == 2) & (leader['example'] == 'average') &
                                 (round(leader['leader_threshold'], 2) == 0.2) &
                                 (round(leader['subleader_threshold'], 2) == 0.1) & (leader['alternative'] == 'right')]
third_leader_left = leader.loc[(leader['zoom_level'] == 3) & (leader['example'] == 'average') &
                               (round(leader['leader_threshold'], 2) == 0.2) &
                               (round(leader['subleader_threshold'], 2) == 0.1) & (leader['alternative'] == 'left')]
third_leader_right = leader.loc[(leader['zoom_level'] == 3) & (leader['example'] == 'average') &
                                (round(leader['leader_threshold'], 2) == 0.2) &
                                (round(leader['subleader_threshold'], 2) == 0.1) & (leader['alternative'] == 'left')]

first_naive_left = naive.loc[
    (naive['zoom_level'] == 1) & (naive['example'] == 'average') & (naive['alternative'] == 'left')]
first_naive_right = naive.loc[
    (naive['zoom_level'] == 1) & (naive['example'] == 'average') & (naive['alternative'] == 'right')]
second_naive_left = naive.loc[
    (naive['zoom_level'] == 2) & (naive['example'] == 'average') & (naive['alternative'] == 'left')]
second_naive_right = naive.loc[
    (naive['zoom_level'] == 2) & (naive['example'] == 'average') & (naive['alternative'] == 'right')]
third_naive_left = naive.loc[
    (naive['zoom_level'] == 3) & (naive['example'] == 'average') & (naive['alternative'] == 'left')]
third_naive_right = naive.loc[
    (naive['zoom_level'] == 3) & (naive['example'] == 'average') & (naive['alternative'] == 'right')]

first_procs_left = procs.loc[(procs['zoom_level'] == 1) & (procs['example'] == 'average') &
                             (procs['alternative'] == 'left') & (procs['number_of_processors'] == 4)]
first_procs_right = procs.loc[(procs['zoom_level'] == 1) & (procs['example'] == 'average') &
                              (procs['alternative'] == 'right') & (procs['number_of_processors'] == 4)]
second_procs_left = procs.loc[(procs['zoom_level'] == 2) & (procs['example'] == 'average') &
                              (procs['alternative'] == 'left') & (procs['number_of_processors'] == 4)]
second_procs_right = procs.loc[(procs['zoom_level'] == 2) & (procs['example'] == 'average') &
                               (procs['alternative'] == 'right') & (procs['number_of_processors'] == 4)]
third_procs_left = procs.loc[(procs['zoom_level'] == 3) & (procs['example'] == 'average') &
                             (procs['alternative'] == 'left') & (procs['number_of_processors'] == 4)]
third_procs_right = procs.loc[(procs['zoom_level'] == 3) & (procs['example'] == 'average') &
                              (procs['alternative'] == 'right') & (procs['number_of_processors'] == 4)]

first_threads_left = threads.loc[(threads['zoom_level'] == 1) & (threads['example'] == 'average') &
                                 (threads['alternative'] == 'left') & (threads['number_of_processors'] == 2)]
first_threads_right = threads.loc[(threads['zoom_level'] == 1) & (threads['example'] == 'average') &
                                  (threads['alternative'] == 'right') & (threads['number_of_processors'] == 2)]
second_threads_left = threads.loc[(threads['zoom_level'] == 2) & (threads['example'] == 'average') &
                                  (threads['alternative'] == 'left') & (threads['number_of_processors'] == 2)]
second_threads_right = threads.loc[(threads['zoom_level'] == 2) & (threads['example'] == 'average') &
                                   (threads['alternative'] == 'right') & (threads['number_of_processors'] == 2)]
third_threads_left = threads.loc[(threads['zoom_level'] == 3) & (threads['example'] == 'average') &
                                 (threads['alternative'] == 'left') & (threads['number_of_processors'] == 2)]
third_threads_right = threads.loc[(threads['zoom_level'] == 3) & (threads['example'] == 'average') &
                                  (threads['alternative'] == 'right') & (threads['number_of_processors'] == 2)]


def get_average(first_left, first_right, second_left, second_right, third_left, third_right):
    first_avg_left = pd.DataFrame(
        {'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
         'number_of_processors': []})
    first_avg_right = pd.DataFrame(
        {'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
         'number_of_processors': []})
    second_avg_left = pd.DataFrame(
        {'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
         'number_of_processors': []})
    second_avg_right = pd.DataFrame({'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [],
                                     'number_of_samples': [], 'number_of_processors': []})
    third_avg_left = pd.DataFrame(
        {'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
         'number_of_processors': []})
    third_avg_right = pd.DataFrame(
        {'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
         'number_of_processors': []})

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
            first_avg_left.loc[avg_index, 'example'] = first_left.at[index, 'example']
            avg_index += 1
            index += 2
        else:
            first_avg_left.at[avg_index, 'zoom_level'] = first_left.at[index, 'zoom_level']
            first_avg_left.loc[avg_index, 'alternative'] = first_left.at[index, 'alternative']
            first_avg_left.at[avg_index, 'avg_time_in_seconds'] = first_left.at[index, 'avg_time_in_seconds']
            first_avg_left.at[avg_index, 'number_of_samples'] = first_left.at[index, 'number_of_samples']
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
            first_avg_right.loc[avg_index, 'example'] = first_right.at[index, 'example']
            avg_index += 1
            index += 2
        else:
            first_avg_right.at[avg_index, 'zoom_level'] = first_right.at[index, 'zoom_level']
            first_avg_right.loc[avg_index, 'alternative'] = first_right.at[index, 'alternative']
            first_avg_right.at[avg_index, 'avg_time_in_seconds'] = first_right.at[index, 'avg_time_in_seconds']
            first_avg_right.at[avg_index, 'number_of_samples'] = first_right.at[index, 'number_of_samples']
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
            second_avg_left.loc[avg_index, 'example'] = second_left.at[index, 'example']
            avg_index += 1
            index += 2
        else:
            second_avg_left.at[avg_index, 'zoom_level'] = second_left.at[index, 'zoom_level']
            second_avg_left.loc[avg_index, 'alternative'] = second_left.at[index, 'alternative']
            second_avg_left.at[avg_index, 'avg_time_in_seconds'] = second_left.at[index, 'avg_time_in_seconds']
            second_avg_left.at[avg_index, 'number_of_samples'] = second_left.at[index, 'number_of_samples']
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
            second_avg_right.loc[avg_index, 'example'] = second_right.at[index, 'example']
            avg_index += 1
            index += 2
        else:
            second_avg_right.at[avg_index, 'zoom_level'] = second_right.at[index, 'zoom_level']
            second_avg_right.loc[avg_index, 'alternative'] = second_right.at[index, 'alternative']
            second_avg_right.at[avg_index, 'avg_time_in_seconds'] = second_right.at[index, 'avg_time_in_seconds']
            second_avg_right.at[avg_index, 'number_of_samples'] = second_right.at[index, 'number_of_samples']
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
            third_avg_left.loc[avg_index, 'example'] = third_left.at[index, 'example']
            avg_index += 1
            index += 2
        else:
            third_avg_left.at[avg_index, 'zoom_level'] = third_left.at[index, 'zoom_level']
            third_avg_left.loc[avg_index, 'alternative'] = third_left.at[index, 'alternative']
            third_avg_left.at[avg_index, 'avg_time_in_seconds'] = third_left.at[index, 'avg_time_in_seconds']
            third_avg_left.at[avg_index, 'number_of_samples'] = third_left.at[index, 'number_of_samples']
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
            third_avg_right.loc[avg_index, 'example'] = third_right.at[index, 'example']
            avg_index += 1
            index += 2
        else:
            third_avg_right.at[avg_index, 'zoom_level'] = third_right.at[index, 'zoom_level']
            third_avg_right.loc[avg_index, 'alternative'] = third_right.at[index, 'alternative']
            third_avg_right.at[avg_index, 'avg_time_in_seconds'] = third_right.at[index, 'avg_time_in_seconds']
            third_avg_right.at[avg_index, 'number_of_samples'] = third_right.at[index, 'number_of_samples']
            third_avg_right.loc[avg_index, 'example'] = third_right.at[index, 'example']
            avg_index += 1
            index += 1

    return first_avg_left, first_avg_right, second_avg_left, second_avg_right, third_avg_left, third_avg_right


naive_first_avg_left, naive_first_avg_right, naive_second_avg_left, naive_second_avg_right, naive_third_avg_left, \
naive_third_avg_right = get_average(first_naive_left, first_naive_right, second_naive_left, second_naive_right,
                                    third_naive_left, third_naive_right)

procs_first_avg_left, procs_first_avg_right, procs_second_avg_left, procs_second_avg_right, procs_third_avg_left, \
procs_third_avg_right = get_average(first_procs_left, first_procs_right, second_procs_left, second_procs_right,
                                    third_procs_left, third_procs_right)

threads_first_avg_left, threads_first_avg_right, threads_second_avg_left, threads_second_avg_right, threads_third_avg_left, \
threads_third_avg_right = get_average(first_threads_left, first_threads_right, second_threads_left, second_threads_right,
                                    third_threads_left, third_threads_right)

sns.set()

fig, axs = plt.subplots(3, 1)
fig.set_figheight(11)
fig.set_figwidth(7)
fig.tight_layout(pad=3.0)
first_leader_left.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[0],
                       label='Leader-Subleader')
naive_first_avg_left.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[0],
                      label='Naive')
procs_first_avg_left.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='orange', ax=axs[0],
                      label='Multiple processors')
threads_first_avg_left.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[0],
                        label='Multiple threads')
axs[0].set_title('First zoom')
axs[0].set_xlabel('Number of samples')
axs[0].set_ylabel('Time in seconds')

second_leader_left.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[1],
                        label='Leader-Subleader')
naive_second_avg_left.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[1],
                       label='Naive')
procs_second_avg_left.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='orange', ax=axs[1],
                       label='Multiple processors')
threads_second_avg_left.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[1],
                         label='Multiple threads')
axs[1].set_title('Second zoom')
axs[1].set_xlabel('Number of samples')
axs[1].set_ylabel('Time in seconds')

third_leader_left.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[2],
                       label='Leader-Subleader')
naive_third_avg_left.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[2],
                      label='Naive')
procs_third_avg_left.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='orange', ax=axs[2],
                      label='Multiple processors')
threads_third_avg_left.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[2],
                        label='Multiple threads')
axs[2].set_title('Third zoom')
axs[2].set_xlabel('Number of samples')
axs[2].set_ylabel('Time in seconds')

# fig, axs = plt.subplots(3, 1)
# fig.set_figheight(11)
# fig.set_figwidth(7)
# fig.tight_layout(pad=3.0)
# first_leader_right.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[0],
#                        label='Leader-Subleader')
# naive_first_avg_right.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[0],
#                       label='Naive')
# procs_first_avg_right.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='orange', ax=axs[0],
#                       label='Multiple processors')
# threads_first_avg_right.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[0],
#                         label='Multiple threads')
# axs[0].set_title('First zoom')
# axs[0].set_xlabel('Number of samples')
# axs[0].set_ylabel('Time in seconds')
#
# second_leader_right.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[1],
#                         label='Leader-Subleader')
# naive_second_avg_right.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[1],
#                        label='Naive')
# procs_second_avg_right.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='orange', ax=axs[1],
#                        label='Multiple processors')
# threads_second_avg_right.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[1],
#                          label='Multiple threads')
# axs[1].set_title('Second zoom')
# axs[1].set_xlabel('Number of samples')
# axs[1].set_ylabel('Time in seconds')
#
# third_leader_right.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[2],
#                        label='Leader-Subleader')
# naive_third_avg_right.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[2],
#                       label='Naive')
# procs_third_avg_right.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='orange', ax=axs[2],
#                       label='Multiple processors')
# threads_third_avg_right.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[2],
#                         label='Multiple threads')
# axs[2].set_title('Third zoom')
# axs[2].set_xlabel('Number of samples')
# axs[2].set_ylabel('Time in seconds')

plt.savefig('comparison_left.png')
plt.show()
