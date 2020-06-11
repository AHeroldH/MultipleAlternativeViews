import pandas as pd
import matplotlib.pyplot as plt
import statistics
import seaborn as sns

random_sample = pd.read_csv('../Sample data sets/random_sample_time.csv')
full_data = pd.read_csv('../Experiments/Time/full_data_set_time.csv')

first_random = random_sample.loc[random_sample['zoom_level'] == 1]
second_random = random_sample.loc[random_sample['zoom_level'] == 2]
third_random = random_sample.loc[random_sample['zoom_level'] == 3]

first_full = full_data.loc[full_data['zoom_level'] == 1]
second_full = full_data.loc[full_data['zoom_level'] == 2]
third_full = full_data.loc[full_data['zoom_level'] == 3]

first_random_avg = pd.DataFrame({'zoom_level': [], 'x_axis_spacing': [], 'y_axis_spacing': [], 'time_in_seconds': [],
                                 'number_of_samples': []})
second_random_avg = pd.DataFrame({'zoom_level': [], 'x_axis_spacing': [], 'y_axis_spacing': [], 'time_in_seconds': [],
                                 'number_of_samples': []})
third_random_avg = pd.DataFrame({'zoom_level': [], 'x_axis_spacing': [], 'y_axis_spacing': [], 'time_in_seconds': [],
                                 'number_of_samples': []})

first_full_avg = pd.DataFrame({'zoom_level': [], 'x_axis_spacing': [], 'y_axis_spacing': [], 'time_in_seconds': [],
                                 'number_of_samples': []})
second_full_avg = pd.DataFrame({'zoom_level': [], 'x_axis_spacing': [], 'y_axis_spacing': [], 'time_in_seconds': [],
                                 'number_of_samples': []})
third_full_avg = pd.DataFrame({'zoom_level': [], 'x_axis_spacing': [], 'y_axis_spacing': [], 'time_in_seconds': [],
                                 'number_of_samples': []})

full_avg = pd.DataFrame({'zoom_level': [], 'x_axis_spacing': [], 'y_axis_spacing': [], 'time_in_seconds': [],
                                 'number_of_samples': []})

random_avg = pd.DataFrame({'zoom_level': [], 'x_axis_spacing': [], 'y_axis_spacing': [], 'time_in_seconds': [],
                                 'number_of_samples': []})

first_random = first_random.sort_values(by=['number_of_samples'], ignore_index=True)
second_random = second_random.sort_values(by=['number_of_samples'], ignore_index=True)
third_random = third_random.sort_values(by=['number_of_samples'],  ignore_index=True)
first_full = first_full.sort_values(by=['number_of_samples'], ignore_index=True)
second_full = second_full.sort_values(by=['number_of_samples'], ignore_index=True)
third_full = third_full.sort_values(by=['number_of_samples'],  ignore_index=True)

full_data = full_data.sort_values(by=['number_of_samples'], ignore_index=True)
random_sample = random_sample.sort_values(by=['number_of_samples'], ignore_index=True)

index = 0
avg_index = 0

while index <= len(first_random)-1:
    if index == len(first_random)-1:
        first_random_avg.at[avg_index, 'zoom_level'] = first_random.at[index, 'zoom_level']
        first_random_avg.at[avg_index, 'x_axis_spacing'] = first_random.at[index, 'x_axis_spacing']
        first_random_avg.at[avg_index, 'y_axis_spacing'] = first_random.at[index, 'y_axis_spacing']
        first_random_avg.at[avg_index, 'time_in_seconds'] = first_random.at[index, 'time_in_seconds']
        first_random_avg.at[avg_index, 'number_of_samples'] = first_random.at[index, 'number_of_samples']
        avg_index += 1
        index += 1
        continue
    diff = first_random.at[index+1, 'number_of_samples'] - first_random.at[index, 'number_of_samples']
    if diff <= 10:
        first_random_avg.at[avg_index, 'zoom_level'] = first_random.at[index, 'zoom_level']
        first_random_avg.at[avg_index, 'time_in_seconds'] = statistics.mean(
            [first_random.at[index + 1, 'time_in_seconds'], first_random.at[index, 'time_in_seconds']])
        first_random_avg.at[avg_index, 'number_of_samples'] = statistics.mean(
            [first_random.at[index + 1, 'number_of_samples'], first_random.at[index, 'number_of_samples']])
        avg_index += 1
        index += 2
    else:
        first_random_avg.at[avg_index, 'zoom_level'] = first_random.at[index, 'zoom_level']
        first_random_avg.at[avg_index, 'x_axis_spacing'] = first_random.at[index, 'x_axis_spacing']
        first_random_avg.at[avg_index, 'y_axis_spacing'] = first_random.at[index, 'y_axis_spacing']
        first_random_avg.at[avg_index, 'time_in_seconds'] = first_random.at[index, 'time_in_seconds']
        first_random_avg.at[avg_index, 'number_of_samples'] = first_random.at[index, 'number_of_samples']
        avg_index += 1
        index += 1

index = 0
avg_index = 0

while index <= len(second_random)-1:
    if index == len(second_random)-1:
        second_random_avg.at[avg_index, 'zoom_level'] = second_random.at[index, 'zoom_level']
        second_random_avg.at[avg_index, 'x_axis_spacing'] = second_random.at[index, 'x_axis_spacing']
        second_random_avg.at[avg_index, 'y_axis_spacing'] = second_random.at[index, 'y_axis_spacing']
        second_random_avg.at[avg_index, 'time_in_seconds'] = second_random.at[index, 'time_in_seconds']
        second_random_avg.at[avg_index, 'number_of_samples'] = second_random.at[index, 'number_of_samples']
        avg_index += 1
        index += 1
        continue
    diff = second_random.at[index+1, 'number_of_samples'] - second_random.at[index, 'number_of_samples']
    if diff <= 10:
        second_random_avg.at[avg_index, 'zoom_level'] = second_random.at[index, 'zoom_level']
        second_random_avg.at[avg_index, 'time_in_seconds'] = statistics.mean(
            [second_random.at[index + 1, 'time_in_seconds'], second_random.at[index, 'time_in_seconds']])
        second_random_avg.at[avg_index, 'number_of_samples'] = statistics.mean(
            [second_random.at[index + 1, 'number_of_samples'], second_random.at[index, 'number_of_samples']])
        avg_index += 1
        index += 2
    else:
        second_random_avg.at[avg_index, 'zoom_level'] = second_random.at[index, 'zoom_level']
        second_random_avg.at[avg_index, 'x_axis_spacing'] = second_random.at[index, 'x_axis_spacing']
        second_random_avg.at[avg_index, 'y_axis_spacing'] = second_random.at[index, 'y_axis_spacing']
        second_random_avg.at[avg_index, 'time_in_seconds'] = second_random.at[index, 'time_in_seconds']
        second_random_avg.at[avg_index, 'number_of_samples'] = second_random.at[index, 'number_of_samples']
        avg_index += 1
        index += 1

index = 0
avg_index = 0

while index <= len(third_random)-1:
    if index == len(third_random)-1:
        third_random_avg.at[avg_index, 'zoom_level'] = third_random.at[index, 'zoom_level']
        third_random_avg.at[avg_index, 'x_axis_spacing'] = third_random.at[index, 'x_axis_spacing']
        third_random_avg.at[avg_index, 'y_axis_spacing'] = third_random.at[index, 'y_axis_spacing']
        third_random_avg.at[avg_index, 'time_in_seconds'] = third_random.at[index, 'time_in_seconds']
        third_random_avg.at[avg_index, 'number_of_samples'] = third_random.at[index, 'number_of_samples']
        avg_index += 1
        index += 1
        continue
    diff = third_random.at[index+1, 'number_of_samples'] - third_random.at[index, 'number_of_samples']
    if diff <= 10:
        third_random_avg.at[avg_index, 'zoom_level'] = third_random.at[index, 'zoom_level']
        third_random_avg.at[avg_index, 'time_in_seconds'] = statistics.mean(
            [third_random.at[index + 1, 'time_in_seconds'], third_random.at[index, 'time_in_seconds']])
        third_random_avg.at[avg_index, 'number_of_samples'] = statistics.mean(
            [third_random.at[index + 1, 'number_of_samples'], third_random.at[index, 'number_of_samples']])
        avg_index += 1
        index += 2
    else:
        third_random_avg.at[avg_index, 'zoom_level'] = third_random.at[index, 'zoom_level']
        third_random_avg.at[avg_index, 'x_axis_spacing'] = third_random.at[index, 'x_axis_spacing']
        third_random_avg.at[avg_index, 'y_axis_spacing'] = third_random.at[index, 'y_axis_spacing']
        third_random_avg.at[avg_index, 'time_in_seconds'] = third_random.at[index, 'time_in_seconds']
        third_random_avg.at[avg_index, 'number_of_samples'] = third_random.at[index, 'number_of_samples']
        avg_index += 1
        index += 1

index = 0
avg_index = 0

while index <= len(first_full)-1:
    if index == len(first_full)-1:
        first_full_avg.at[avg_index, 'zoom_level'] = first_full.at[index, 'zoom_level']
        first_full_avg.at[avg_index, 'x_axis_spacing'] = first_full.at[index, 'x_axis_spacing']
        first_full_avg.at[avg_index, 'y_axis_spacing'] = first_full.at[index, 'y_axis_spacing']
        first_full_avg.at[avg_index, 'time_in_seconds'] = first_full.at[index, 'time_in_seconds']
        first_full_avg.at[avg_index, 'number_of_samples'] = first_full.at[index, 'number_of_samples']
        avg_index += 1
        index += 1
        continue
    diff = first_full.at[index+1, 'number_of_samples'] - first_full.at[index, 'number_of_samples']
    if diff <= 10:
        first_full_avg.at[avg_index, 'zoom_level'] = first_full.at[index, 'zoom_level']
        first_full_avg.at[avg_index, 'time_in_seconds'] = statistics.mean(
            [first_full.at[index + 1, 'time_in_seconds'], first_full.at[index, 'time_in_seconds']])
        first_full_avg.at[avg_index, 'number_of_samples'] = statistics.mean(
            [first_full.at[index + 1, 'number_of_samples'], first_full.at[index, 'number_of_samples']])
        avg_index += 1
        index += 2
    else:
        first_full_avg.at[avg_index, 'zoom_level'] = first_full.at[index, 'zoom_level']
        first_full_avg.at[avg_index, 'x_axis_spacing'] = first_full.at[index, 'x_axis_spacing']
        first_full_avg.at[avg_index, 'y_axis_spacing'] = first_full.at[index, 'y_axis_spacing']
        first_full_avg.at[avg_index, 'time_in_seconds'] = first_full.at[index, 'time_in_seconds']
        first_full_avg.at[avg_index, 'number_of_samples'] = first_full.at[index, 'number_of_samples']
        avg_index += 1
        index += 1

index = 0
avg_index = 0

while index <= len(second_full)-1:
    if index == len(second_full)-1:
        second_full_avg.at[avg_index, 'zoom_level'] = second_full.at[index, 'zoom_level']
        second_full_avg.at[avg_index, 'x_axis_spacing'] = second_full.at[index, 'x_axis_spacing']
        second_full_avg.at[avg_index, 'y_axis_spacing'] = second_full.at[index, 'y_axis_spacing']
        second_full_avg.at[avg_index, 'time_in_seconds'] = second_full.at[index, 'time_in_seconds']
        second_full_avg.at[avg_index, 'number_of_samples'] = second_full.at[index, 'number_of_samples']
        avg_index += 1
        index += 1
        continue
    diff = second_full.at[index+1, 'number_of_samples'] - second_full.at[index, 'number_of_samples']
    if diff <= 10:
        second_full_avg.at[avg_index, 'zoom_level'] = second_full.at[index, 'zoom_level']
        second_full_avg.at[avg_index, 'time_in_seconds'] = statistics.mean(
            [second_full.at[index + 1, 'time_in_seconds'], second_full.at[index, 'time_in_seconds']])
        second_full_avg.at[avg_index, 'number_of_samples'] = statistics.mean(
            [second_full.at[index + 1, 'number_of_samples'], second_full.at[index, 'number_of_samples']])
        avg_index += 1
        index += 2
    else:
        second_full_avg.at[avg_index, 'zoom_level'] = second_full.at[index, 'zoom_level']
        second_full_avg.at[avg_index, 'x_axis_spacing'] = second_full.at[index, 'x_axis_spacing']
        second_full_avg.at[avg_index, 'y_axis_spacing'] = second_full.at[index, 'y_axis_spacing']
        second_full_avg.at[avg_index, 'time_in_seconds'] = second_full.at[index, 'time_in_seconds']
        second_full_avg.at[avg_index, 'number_of_samples'] = second_full.at[index, 'number_of_samples']
        avg_index += 1
        index += 1

index = 0
avg_index = 0

while index <= len(third_full)-1:
    if index == len(third_full)-1:
        third_full_avg.at[avg_index, 'zoom_level'] = third_full.at[index, 'zoom_level']
        third_full_avg.at[avg_index, 'x_axis_spacing'] = third_full.at[index, 'x_axis_spacing']
        third_full_avg.at[avg_index, 'y_axis_spacing'] = third_full.at[index, 'y_axis_spacing']
        third_full_avg.at[avg_index, 'time_in_seconds'] = third_full.at[index, 'time_in_seconds']
        third_full_avg.at[avg_index, 'number_of_samples'] = third_full.at[index, 'number_of_samples']
        avg_index += 1
        index += 1
        continue
    diff = third_full.at[index+1, 'number_of_samples'] - third_full.at[index, 'number_of_samples']
    if diff <= 10:
        third_full_avg.at[avg_index, 'zoom_level'] = third_full.at[index, 'zoom_level']
        third_full_avg.at[avg_index, 'time_in_seconds'] = statistics.mean(
            [third_full.at[index + 1, 'time_in_seconds'], third_full.at[index, 'time_in_seconds']])
        third_full_avg.at[avg_index, 'number_of_samples'] = statistics.mean(
            [third_full.at[index + 1, 'number_of_samples'], third_full.at[index, 'number_of_samples']])
        avg_index += 1
        index += 2
    else:
        third_full_avg.at[avg_index, 'zoom_level'] = third_full.at[index, 'zoom_level']
        third_full_avg.at[avg_index, 'x_axis_spacing'] = third_full.at[index, 'x_axis_spacing']
        third_full_avg.at[avg_index, 'y_axis_spacing'] = third_full.at[index, 'y_axis_spacing']
        third_full_avg.at[avg_index, 'time_in_seconds'] = third_full.at[index, 'time_in_seconds']
        third_full_avg.at[avg_index, 'number_of_samples'] = third_full.at[index, 'number_of_samples']
        avg_index += 1
        index += 1

sns.set()
fig, axs = plt.subplots(3, 1)
fig.set_figheight(11)
fig.set_figwidth(5)
fig.tight_layout(pad=3.0)
first_random_avg.plot(kind='line', x='number_of_samples', y='time_in_seconds', color='blue', ax=axs[0], label='Random sample')
first_full_avg.plot(kind='line', x='number_of_samples', y='time_in_seconds', color='green', ax=axs[0], label='Complete data set')
axs[0].set_title('First zoom')
axs[0].set_xlabel('Number of samples')
axs[0].set_ylabel('Time in seconds')

second_random_avg.plot(kind='line', x='number_of_samples', y='time_in_seconds', color='blue', ax=axs[1], label='Random sample')
second_full_avg.plot(kind='line', x='number_of_samples', y='time_in_seconds', color='green', ax=axs[1], label='Complete data set')
axs[1].set_title('Second zoom')
axs[1].set_xlabel('Number of samples')
axs[1].set_ylabel('Time in seconds')

third_random_avg.plot(kind='line', x='number_of_samples', y='time_in_seconds', color='blue', ax=axs[2], label='Random sample')
third_full_avg.plot(kind='line', x='number_of_samples', y='time_in_seconds', color='green', ax=axs[2], label='Complete data set')
axs[2].set_title('Third zoom')
axs[2].set_xlabel('Number of samples')
axs[2].set_ylabel('Time in seconds')

# sns.set()
# fig, axs = plt.subplots(1, 2, constrained_layout=True)
# fig.set_figwidth(11)
# first_random_avg.plot(kind='line', x='number_of_samples', y='time_in_seconds', color='blue', ax=axs[0], label='First zoom')
# second_random_avg.plot(kind='line', x='number_of_samples', y='time_in_seconds', color='green', ax=axs[0], label='Second zoom')
# third_random_avg.plot(kind='line', x='number_of_samples', y='time_in_seconds', color='red', ax=axs[0], label='Third zoom')
# axs[0].set_title('Random sample of samples')
# axs[0].set_xlabel('Number of samples')
# axs[0].set_ylabel('Time in seconds')
#
# first_full_avg.plot(kind='line', x='number_of_samples', y='time_in_seconds', color='blue', ax=axs[1], label='First zoom')
# second_full_avg.plot(kind='line', x='number_of_samples', y='time_in_seconds', color='green', ax=axs[1], label='Second zoom')
# third_full_avg.plot(kind='line', x='number_of_samples', y='time_in_seconds', color='red', ax=axs[1], label='Third zoom')
# axs[1].set_title('Complete data of samples')
# axs[1].set_xlabel('Number of samples')
# axs[1].set_ylabel('Time in seconds')

plt.savefig('sampling_individual_comparison.png')
plt.show()
