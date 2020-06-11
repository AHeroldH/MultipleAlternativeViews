import pandas as pd
import matplotlib.pyplot as plt
import statistics
import numpy as np
import seaborn as sns

data = pd.read_csv('../Experiments/Time/multi_time_2.csv')

first_left = data.loc[(data['zoom_level'] == 1) & (data['alternative'] == 'left') & (data['example'] == 'average')]
first_right = data.loc[(data['zoom_level'] == 1) & (data['alternative'] == 'right') & (data['example'] == 'average')]
second_left = data.loc[(data['zoom_level'] == 2) & (data['alternative'] == 'left') & (data['example'] == 'average')]
second_right = data.loc[(data['zoom_level'] == 2) & (data['alternative'] == 'right') & (data['example'] == 'average')]
third_left = data.loc[(data['zoom_level'] == 3) & (data['alternative'] == 'left') & (data['example'] == 'average')]
third_right = data.loc[(data['zoom_level'] == 3) & (data['alternative'] == 'right') & (data['example'] == 'average')]

# first_left = data.loc[(data['zoom_level'] == 1) & (data['alternative'] == 'left')]
# first_right = data.loc[(data['zoom_level'] == 1) & (data['alternative'] == 'right')]
# second_left = data.loc[(data['zoom_level'] == 2) & (data['alternative'] == 'left')]
# second_right = data.loc[(data['zoom_level'] == 2) & (data['alternative'] == 'right')]
# third_left = data.loc[(data['zoom_level'] == 3) & (data['alternative'] == 'left')]
# third_right = data.loc[(data['zoom_level'] == 3) & (data['alternative'] == 'right')]

first_avg_left = pd.DataFrame({'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
                               'number_of_processors': []})
first_avg_right = pd.DataFrame({'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
                                'number_of_processors': []})
second_avg_left = pd.DataFrame({'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
                                'number_of_processors': []})
second_avg_right = pd.DataFrame({'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [],
                                 'number_of_samples': [], 'number_of_processors': []})
third_avg_left = pd.DataFrame({'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
                               'number_of_processors': []})
third_avg_right = pd.DataFrame({'zoom_level': [], 'alternative': [], 'avg_time_in_seconds': [], 'number_of_samples': [],
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
        first_avg_left.at[avg_index, 'number_of_processors'] = first_left.at[index, 'number_of_processors']
        first_avg_left.loc[avg_index, 'example'] = first_left.at[index, 'example']
        avg_index += 1
        index += 1
        continue
    diff = first_left.at[index + 1, 'number_of_samples'] - first_left.at[index, 'number_of_samples']
    if diff <= 100 and (first_left.at[index, 'number_of_processors'] == first_left.at[index+1, 'number_of_processors']) \
            and (first_left.at[index, 'example'] == first_left.at[index + 1, 'example']):
        first_avg_left.at[avg_index, 'zoom_level'] = first_left.at[index, 'zoom_level']
        first_avg_left.loc[avg_index, 'alternative'] = first_left.at[index, 'alternative']
        first_avg_left.at[avg_index, 'avg_time_in_seconds'] = statistics.mean(
            [first_left.at[index + 1, 'avg_time_in_seconds'], first_left.at[index, 'avg_time_in_seconds']])
        first_avg_left.at[avg_index, 'number_of_samples'] = statistics.mean(
            [first_left.at[index + 1, 'number_of_samples'], first_left.at[index, 'number_of_samples']])
        first_avg_left.at[avg_index, 'number_of_processors'] = first_left.at[index, 'number_of_processors']
        first_avg_left.loc[avg_index, 'example'] = first_left.at[index, 'example']
        avg_index += 1
        index += 2
    else:
        first_avg_left.at[avg_index, 'zoom_level'] = first_left.at[index, 'zoom_level']
        first_avg_left.loc[avg_index, 'alternative'] = first_left.at[index, 'alternative']
        first_avg_left.at[avg_index, 'avg_time_in_seconds'] = first_left.at[index, 'avg_time_in_seconds']
        first_avg_left.at[avg_index, 'number_of_samples'] = first_left.at[index, 'number_of_samples']
        first_avg_left.at[avg_index, 'number_of_processors'] = first_left.at[index, 'number_of_processors']
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
        first_avg_right.at[avg_index, 'number_of_processors'] = first_right.at[index, 'number_of_processors']
        first_avg_right.loc[avg_index, 'example'] = first_right.at[index, 'example']
        avg_index += 1
        index += 1
        continue
    diff = first_right.at[index + 1, 'number_of_samples'] - first_right.at[index, 'number_of_samples']
    if diff <= 100 and (first_right.at[index, 'number_of_processors'] == first_right.at[index+1, 'number_of_processors']) \
            and (first_right.at[index, 'example'] == first_right.at[index + 1, 'example']):
        first_avg_right.at[avg_index, 'zoom_level'] = first_right.at[index, 'zoom_level']
        first_avg_right.loc[avg_index, 'alternative'] = first_right.at[index, 'alternative']
        first_avg_right.at[avg_index, 'avg_time_in_seconds'] = statistics.mean(
            [first_right.at[index + 1, 'avg_time_in_seconds'], first_right.at[index, 'avg_time_in_seconds']])
        first_avg_right.at[avg_index, 'number_of_samples'] = statistics.mean(
            [first_right.at[index + 1, 'number_of_samples'], first_right.at[index, 'number_of_samples']])
        first_avg_right.at[avg_index, 'number_of_processors'] = first_right.at[index, 'number_of_processors']
        first_avg_right.loc[avg_index, 'example'] = first_right.at[index, 'example']
        avg_index += 1
        index += 2
    else:
        first_avg_right.at[avg_index, 'zoom_level'] = first_right.at[index, 'zoom_level']
        first_avg_right.loc[avg_index, 'alternative'] = first_right.at[index, 'alternative']
        first_avg_right.at[avg_index, 'avg_time_in_seconds'] = first_right.at[index, 'avg_time_in_seconds']
        first_avg_right.at[avg_index, 'number_of_samples'] = first_right.at[index, 'number_of_samples']
        first_avg_right.at[avg_index, 'number_of_processors'] = first_right.at[index, 'number_of_processors']
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
        second_avg_left.at[avg_index, 'number_of_processors'] = second_left.at[index, 'number_of_processors']
        second_avg_left.loc[avg_index, 'example'] = second_left.at[index, 'example']
        avg_index += 1
        index += 1
        continue
    diff = second_left.at[index + 1, 'number_of_samples'] - second_left.at[index, 'number_of_samples']
    if diff <= 100 and (second_left.at[index, 'number_of_processors'] == second_left.at[index+1, 'number_of_processors']) \
            and (second_left.at[index, 'example'] == second_left.at[index + 1, 'example']):
        second_avg_left.at[avg_index, 'zoom_level'] = second_left.at[index, 'zoom_level']
        second_avg_left.loc[avg_index, 'alternative'] = second_left.at[index, 'alternative']
        second_avg_left.at[avg_index, 'avg_time_in_seconds'] = statistics.mean(
            [second_left.at[index + 1, 'avg_time_in_seconds'], second_left.at[index, 'avg_time_in_seconds']])
        second_avg_left.at[avg_index, 'number_of_samples'] = statistics.mean(
            [second_left.at[index + 1, 'number_of_samples'], second_left.at[index, 'number_of_samples']])
        second_avg_left.at[avg_index, 'number_of_processors'] = second_left.at[index, 'number_of_processors']
        second_avg_left.loc[avg_index, 'example'] = second_left.at[index, 'example']
        avg_index += 1
        index += 2
    else:
        second_avg_left.at[avg_index, 'zoom_level'] = second_left.at[index, 'zoom_level']
        second_avg_left.loc[avg_index, 'alternative'] = second_left.at[index, 'alternative']
        second_avg_left.at[avg_index, 'avg_time_in_seconds'] = second_left.at[index, 'avg_time_in_seconds']
        second_avg_left.at[avg_index, 'number_of_samples'] = second_left.at[index, 'number_of_samples']
        second_avg_left.at[avg_index, 'number_of_processors'] = second_left.at[index, 'number_of_processors']
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
        second_avg_right.at[avg_index, 'number_of_processors'] = second_right.at[index, 'number_of_processors']
        second_avg_right.loc[avg_index, 'example'] = second_right.at[index, 'example']
        avg_index += 1
        index += 1
        continue
    diff = second_right.at[index + 1, 'number_of_samples'] - second_right.at[index, 'number_of_samples']
    if diff <= 100 and (second_right.at[index, 'number_of_processors'] == second_right.at[index+1, 'number_of_processors'])\
            and (second_right.at[index, 'example'] == second_right.at[index + 1, 'example']):
        second_avg_right.at[avg_index, 'zoom_level'] = second_right.at[index, 'zoom_level']
        second_avg_right.loc[avg_index, 'alternative'] = second_right.at[index, 'alternative']
        second_avg_right.at[avg_index, 'avg_time_in_seconds'] = statistics.mean(
            [second_right.at[index + 1, 'avg_time_in_seconds'], second_right.at[index, 'avg_time_in_seconds']])
        second_avg_right.at[avg_index, 'number_of_samples'] = statistics.mean(
            [second_right.at[index + 1, 'number_of_samples'], second_right.at[index, 'number_of_samples']])
        second_avg_right.at[avg_index, 'number_of_processors'] = second_right.at[index, 'number_of_processors']
        second_avg_right.loc[avg_index, 'example'] = second_right.at[index, 'example']
        avg_index += 1
        index += 2
    else:
        second_avg_right.at[avg_index, 'zoom_level'] = second_right.at[index, 'zoom_level']
        second_avg_right.loc[avg_index, 'alternative'] = second_right.at[index, 'alternative']
        second_avg_right.at[avg_index, 'avg_time_in_seconds'] = second_right.at[index, 'avg_time_in_seconds']
        second_avg_right.at[avg_index, 'number_of_samples'] = second_right.at[index, 'number_of_samples']
        second_avg_right.at[avg_index, 'number_of_processors'] = second_right.at[index, 'number_of_processors']
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
        third_avg_left.at[avg_index, 'number_of_processors'] = third_left.at[index, 'number_of_processors']
        third_avg_left.loc[avg_index, 'example'] = third_left.at[index, 'example']
        avg_index += 1
        index += 1
        continue
    diff = third_left.at[index + 1, 'number_of_samples'] - third_left.at[index, 'number_of_samples']
    if diff <= 100 and (third_left.at[index, 'number_of_processors'] == third_left.at[index+1, 'number_of_processors'])\
            and (third_left.at[index, 'example'] == third_left.at[index + 1, 'example']):
        third_avg_left.at[avg_index, 'zoom_level'] = third_left.at[index, 'zoom_level']
        third_avg_left.loc[avg_index, 'alternative'] = third_left.at[index, 'alternative']
        third_avg_left.at[avg_index, 'avg_time_in_seconds'] = statistics.mean(
            [third_left.at[index + 1, 'avg_time_in_seconds'], third_left.at[index, 'avg_time_in_seconds']])
        third_avg_left.at[avg_index, 'number_of_samples'] = statistics.mean(
            [third_left.at[index + 1, 'number_of_samples'], third_left.at[index, 'number_of_samples']])
        third_avg_left.at[avg_index, 'number_of_processors'] = third_left.at[index, 'number_of_processors']
        third_avg_left.loc[avg_index, 'example'] = third_left.at[index, 'example']
        avg_index += 1
        index += 2
    else:
        third_avg_left.at[avg_index, 'zoom_level'] = third_left.at[index, 'zoom_level']
        third_avg_left.loc[avg_index, 'alternative'] = third_left.at[index, 'alternative']
        third_avg_left.at[avg_index, 'avg_time_in_seconds'] = third_left.at[index, 'avg_time_in_seconds']
        third_avg_left.at[avg_index, 'number_of_samples'] = third_left.at[index, 'number_of_samples']
        third_avg_left.at[avg_index, 'number_of_processors'] = third_left.at[index, 'number_of_processors']
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
        third_avg_right.at[avg_index, 'number_of_processors'] = third_right.at[index, 'number_of_processors']
        third_avg_right.loc[avg_index, 'example'] = third_right.at[index, 'example']
        avg_index += 1
        index += 1
        continue
    diff = third_right.at[index + 1, 'number_of_samples'] - third_right.at[index, 'number_of_samples']
    if diff <= 100 and (third_right.at[index, 'number_of_processors'] == third_right.at[index+1, 'number_of_processors'])\
            and (third_right.at[index, 'example'] == third_right.at[index + 1, 'example']):
        third_avg_right.at[avg_index, 'zoom_level'] = third_right.at[index, 'zoom_level']
        third_avg_right.loc[avg_index, 'alternative'] = third_right.at[index, 'alternative']
        third_avg_right.at[avg_index, 'avg_time_in_seconds'] = statistics.mean(
            [third_right.at[index + 1, 'avg_time_in_seconds'], third_right.at[index, 'avg_time_in_seconds']])
        third_avg_right.at[avg_index, 'number_of_samples'] = statistics.mean(
            [third_right.at[index + 1, 'number_of_samples'], third_right.at[index, 'number_of_samples']])
        third_avg_right.at[avg_index, 'number_of_processors'] = third_right.at[index, 'number_of_processors']
        third_avg_right.loc[avg_index, 'example'] = third_right.at[index, 'example']
        avg_index += 1
        index += 2
    else:
        third_avg_right.at[avg_index, 'zoom_level'] = third_right.at[index, 'zoom_level']
        third_avg_right.loc[avg_index, 'alternative'] = third_right.at[index, 'alternative']
        third_avg_right.at[avg_index, 'avg_time_in_seconds'] = third_right.at[index, 'avg_time_in_seconds']
        third_avg_right.at[avg_index, 'number_of_samples'] = third_right.at[index, 'number_of_samples']
        third_avg_right.at[avg_index, 'number_of_processors'] = third_right.at[index, 'number_of_processors']
        third_avg_right.loc[avg_index, 'example'] = third_right.at[index, 'example']
        avg_index += 1
        index += 1

sns.set()

first_left_low = first_avg_left.loc[first_avg_left['number_of_processors'] == 2]
first_left_med = first_avg_left.loc[first_avg_left['number_of_processors'] == 3]
first_left_high = first_avg_left.loc[first_avg_left['number_of_processors'] == 4]
first_right_low = first_avg_right.loc[first_avg_right['number_of_processors'] == 2]
first_right_med = first_avg_right.loc[first_avg_right['number_of_processors'] == 3]
first_right_high = first_avg_right.loc[first_avg_right['number_of_processors'] == 4]
second_left_low = second_avg_left.loc[second_avg_left['number_of_processors'] == 2]
second_left_med = second_avg_left.loc[second_avg_left['number_of_processors'] == 3]
second_left_high = second_avg_left.loc[second_avg_left['number_of_processors'] == 4]
second_right_low = second_avg_right.loc[second_avg_right['number_of_processors'] == 2]
second_right_med = second_avg_right.loc[second_avg_right['number_of_processors'] == 3]
second_right_high = second_avg_right.loc[second_avg_right['number_of_processors'] == 4]
third_left_low = third_avg_left.loc[third_avg_left['number_of_processors'] == 2]
third_left_med = third_avg_left.loc[third_avg_left['number_of_processors'] == 3]
third_left_high = third_avg_left.loc[third_avg_left['number_of_processors'] == 4]
third_right_low = third_avg_right.loc[third_avg_right['number_of_processors'] == 2]
third_right_med = third_avg_right.loc[third_avg_right['number_of_processors'] == 3]
third_right_high = third_avg_right.loc[third_avg_right['number_of_processors'] == 4]

# combined = pd.concat([first_avg_left, first_avg_right, second_avg_left, second_avg_right, third_avg_left, third_avg_right],
#            ignore_index=True)
#
# data['complexity'] = [(row['avg_time_in_seconds']*1000000)/row['number_of_samples'] for i, row in data.iterrows()]
#
# sns.set()
# ax = plt.gca()
# data.plot(kind='scatter', x='number_of_samples', y='complexity', color='blue', ax=ax)
# ax.axhline(y=100, label="c", color="green")
# ax.axvline(x=2500, label="$n_0$", color="red")
# plt.xlabel('Number of samples')
# plt.ylabel('Time in microseconds / number of samples')
# handles, labels = ax.get_legend_handles_labels()
# plt.legend(handles=handles[0:], labels=labels)

fig, axs = plt.subplots(3, 1)
fig.set_figheight(11)
fig.set_figwidth(7)
fig.tight_layout(pad=3.0)
first_left_low.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[0], label='2 processors - left')
first_left_med.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[0], label='3 processors - left')
first_left_high.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[0], label='4 processors - left')
first_right_low.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[0], label='2 processors - right')
first_right_med.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[0], label='3 processors - right')
first_right_high.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='brown', ax=axs[0], label='4 processors - right')
axs[0].set_title('First zoom')
axs[0].set_xlabel('Number of samples')
axs[0].set_ylabel('Time in seconds')

second_left_low.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[1], label='2 processors - left')
second_left_med.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[1], label='3 processors - left')
second_left_high.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[1], label='4 processors - left')
second_right_low.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[1], label='2 processors - right')
second_right_med.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[1], label='3 processors - right')
second_right_high.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='brown', ax=axs[1], label='4 processors - right')
axs[1].set_title('Second zoom')
axs[1].set_xlabel('Number of samples')
axs[1].set_ylabel('Time in seconds')

third_left_low.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[2], label='2 processors - left')
third_left_med.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[2], label='3 processors - left')
third_left_high.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[2], label='4 processors - left')
third_right_low.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[2], label='2 processors - right')
third_right_med.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[2], label='3 processors - right')
third_right_high.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='brown', ax=axs[2], label='4 processors - right')
axs[2].set_title('Third zoom')
axs[2].set_xlabel('Number of samples')
axs[2].set_ylabel('Time in seconds')

# fig, axs = plt.subplots(1, 2)
# fig.set_figwidth(11)
# first_left_low.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[0], label='First zoom')
# second_left_low.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[0], label='Second zoom')
# third_left_low.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[0], label='Third zoom')
# axs[0].set_title('Left alternative')
# axs[0].set_xlabel('Number of samples')
# axs[0].set_ylabel('Time in seconds')
#
# first_right_low.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[1], label='First zoom')
# second_right_low.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[1], label='Second zoom')
# third_right_low.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[1], label='Third zoom')
# axs[1].set_title('Right alternative')
# axs[1].set_xlabel('Number of samples')
# axs[1].set_ylabel('Time in seconds')

# first_left_first = first_avg_left.loc[first_avg_left['example'] == '[5.0; 9.0]; [757523835.5; 1515047671.0]']
# first_left_second = first_avg_left.loc[first_avg_left['example'] == '[5.0; 9.0]; [0.0; 757523835.5]']
# first_left_third = first_avg_left.loc[first_avg_left['example'] == '[2.0; 6.0]; [0.0; 757523835.5]']
# first_left_fourth = first_avg_left.loc[first_avg_left['example'] == '[3.0; 7.0]; [300000000; 1057523835.5]']
# first_left_fifth = first_avg_left.loc[first_avg_left['example'] == '[4.5; 8.5]; [300000000; 1057523835.5]']
# first_right_first = first_avg_right.loc[first_avg_right['example'] == '[5.0; 9.0]; [757523835.5; 1515047671.0]']
# first_right_second = first_avg_right.loc[first_avg_right['example'] == '[5.0; 9.0]; [0.0; 757523835.5]']
# first_right_third = first_avg_right.loc[first_avg_right['example'] == '[2.0; 6.0]; [0.0; 757523835.5]']
# first_right_fourth = first_avg_right.loc[first_avg_right['example'] == '[3.0; 7.0]; [300000000; 1057523835.5]']
# first_right_fifth = first_avg_right.loc[first_avg_right['example'] == '[4.5; 8.5]; [300000000; 1057523835.5]']
# second_left_first = second_avg_left.loc[second_avg_left['example'] == '[5.5; 7.5]; [700000000; 1078761917.5]']
# second_left_second = second_avg_left.loc[second_avg_left['example'] == '[4.0; 6.0]; [0.0; 378761917.75]']
# second_left_third = second_avg_left.loc[second_avg_left['example'] == '[6.0; 8.0]; [300000000; 678761917.75]']
# second_left_fourth = second_avg_left.loc[second_avg_left['example'] == '[7.0; 9.0]; [200000000; 578761917.75]']
# second_left_fifth = second_avg_left.loc[second_avg_left['example'] == '[3.0; 5.0]; [0.0; 378761917.75]']
# second_right_first = second_avg_right.loc[second_avg_right['example'] == '[5.5; 7.5]; [700000000; 1078761917.5]']
# second_right_second = second_avg_right.loc[second_avg_right['example'] == '[4.0; 6.0]; [0.0; 378761917.75]']
# second_right_third = second_avg_right.loc[second_avg_right['example'] == '[6.0; 8.0]; [300000000; 678761917.75]']
# second_right_fourth = second_avg_right.loc[second_avg_right['example'] == '[7.0; 9.0]; [200000000; 578761917.75]']
# second_right_fifth = second_avg_right.loc[second_avg_right['example'] == '[3.0; 5.0]; [0.0; 378761917.75]']
# third_left_first = third_avg_left.loc[third_avg_left['example'] == '[3.0; 4.0]; [0.0; 189380958.88]']
# third_left_second = third_avg_left.loc[third_avg_left['example'] == '[6.5; 7.5]; [600000000; 789380958.88]']
# third_left_third = third_avg_left.loc[third_avg_left['example'] == '[6.0; 7.0]; [0.0; 189380958.88]']
# third_left_fourth = third_avg_left.loc[third_avg_left['example'] == '[7.0; 8.0]; [200000000; 389380958.88]']
# third_left_fifth = third_avg_left.loc[third_avg_left['example'] == '[8.0; 9.0]; [0.0; 189380958.88]']
# third_right_first = third_avg_right.loc[third_avg_right['example'] == '[3.0; 4.0]; [0.0; 189380958.88]']
# third_right_second = third_avg_right.loc[third_avg_right['example'] == '[6.5; 7.5]; [600000000; 789380958.88]']
# third_right_third = third_avg_right.loc[third_avg_right['example'] == '[6.0; 7.0]; [0.0; 189380958.88]']
# third_right_fourth = third_avg_right.loc[third_avg_right['example'] == '[7.0; 8.0]; [200000000; 389380958.88]']
# third_right_fifth = third_avg_right.loc[third_avg_right['example'] == '[8.0; 9.0]; [0.0; 189380958.88]']
#
# fig, axs = plt.subplots(3, 2)
# fig.set_figheight(11)
# fig.set_figwidth(10)
# fig.tight_layout(pad=3.0)
# i = np.unravel_index(0, axs.shape)
# first_left_first.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[i],
#                       label='First example')
# first_left_second.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[i],
#                        label='Second example')
# first_left_third.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[i],
#                       label='Third example')
# first_left_fourth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[i],
#                        label='Fourth example')
# first_left_fifth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[i],
#                       label='Fifth example')
# axs[i].set_title('First zoom - Left Alternative')
# axs[i].set_xlabel('Number of samples')
# axs[i].set_ylabel('Time in seconds')
#
# i = np.unravel_index(2, axs.shape)
# second_left_first.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[i],
#                        label='First example')
# second_left_second.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[i],
#                         label='Second example')
# second_left_third.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[i],
#                        label='Third example')
# second_left_fourth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[i],
#                         label='Fourth example')
# second_left_fifth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[i],
#                        label='Fifth example')
# axs[i].set_title('Second zoom - Left Alternative')
# axs[i].set_xlabel('Number of samples')
# axs[i].set_ylabel('Time in seconds')
#
# i = np.unravel_index(4, axs.shape)
# third_left_first.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[i],
#                       label='First example')
# third_left_second.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[i],
#                        label='Second example')
# third_left_third.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[i],
#                       label='Third example')
# third_left_fourth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[i],
#                        label='Fourth example')
# third_left_fifth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[i],
#                       label='Fifth example')
# axs[i].set_title('Third zoom - Left Alternative')
# axs[i].set_xlabel('Number of samples')
# axs[i].set_ylabel('Time in seconds')
#
# i = np.unravel_index(1, axs.shape)
# first_right_first.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[i],
#                        label='First example')
# first_right_second.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[i],
#                         label='Second example')
# first_right_third.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[i],
#                        label='Third example')
# first_right_fourth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[i],
#                         label='Fourth example')
# first_right_fifth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[i],
#                        label='Fifth example')
# axs[i].set_title('First zoom - Right Alternative')
# axs[i].set_xlabel('Number of samples')
# axs[i].set_ylabel('Time in seconds')
#
# i = np.unravel_index(3, axs.shape)
# second_right_first.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[i],
#                         label='First example')
# second_right_second.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[i],
#                          label='Second example')
# second_right_third.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[i],
#                         label='Third example')
# second_right_fourth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[i],
#                          label='Fourth example')
# second_right_fifth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[i],
#                         label='Fifth example')
# axs[i].set_title('Second zoom - Right Alternative')
# axs[i].set_xlabel('Number of samples')
# axs[i].set_ylabel('Time in seconds')
#
# i = np.unravel_index(5, axs.shape)
# third_right_first.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='blue', ax=axs[i],
#                        label='First example')
# third_right_second.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='green', ax=axs[i],
#                         label='Second example')
# third_right_third.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='red', ax=axs[i],
#                        label='Third example')
# third_right_fourth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='purple', ax=axs[i],
#                         label='Fourth example')
# third_right_fifth.plot(kind='line', x='number_of_samples', y='avg_time_in_seconds', color='black', ax=axs[i],
#                        label='Fifth example')
# axs[i].set_title('Third zoom - Right Alternative')
# axs[i].set_xlabel('Number of samples')
# axs[i].set_ylabel('Time in seconds')

# axs[0].get_legend().remove()
# axs[1].get_legend().remove()
# axs[2].get_legend().remove()
# handles, labels = [(a) for a, b, c in zip(axs[0].get_legend_handles_labels(), axs[1].get_legend_handles_labels(), axs[2].get_legend_handles_labels())]
# fig.legend(handles, labels, loc=(0.7, 0.4))
plt.savefig('multi_procs_individual_comparison.png')
plt.show()
