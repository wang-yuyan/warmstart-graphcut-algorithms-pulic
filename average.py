"""
This file is used to take the average of the cold-/warm-start running time and the statistics
such as # of paths taken and average path lengths.
"""

import numpy as np

def mstd(row):
    return (np.mean(row), np.std(row))

groups = ["birdhouse", "head", "shoe", "dog"]
sizes = [30, 60, 120]

time_average_dir = "./sequential_datasets/all_time_averages.txt"
path_average_dir = "./sequential_datasets/all_path_averages.txt"
time_average_f = open(time_average_dir, 'w')
path_average_f = open(time_average_dir, 'w')
time_titles = "image_group\tsize\tff\twarm_start\tfeas_proj\tratio(%)\n"
time_average_f.write(time_titles)
path_titles = "image_group\tsize\texcess_ratio\trecoverd_flow_ratio\tnum_aug_path_avg\tavg_path_len\tnum_proj_path_avg\tavg_proj_len\tnum_warm_start_path_avg\tavg_warm_start_len\n"
path_average_f.write(path_titles)

for group in groups:
    for size in sizes:
        result_dir = "./sequential_datasets/{}_results".format(group)
        time_f = open("{}/{}_{}.txt".format(result_dir, size, "time"), 'r')
        path_f = open("{}/{}_{}.txt".format(result_dir, size, "path"), 'r')

        time_average_f.write('{}\t{}\t'.format(group, size))
        path_average_f.write('{}\t{}\t'.format(group, size))

        lines = time_f.readlines()[1:]
        lines = [line.split('\t')[1:] for line in lines]
        time_data = np.array(lines, dtype=np.float64)
        time_average = np.average(time_data, axis=0)

        for time in time_average:
            time_average_f.write(str(round(time, 2)) + '\t')
        time_average_f.write(str(round(1 - time_average[1] / time_average[0], 4)) + '\n')

        lines = path_f.readlines()[1:]
        lines = [line.split('\t')[1:] for line in lines]
        path_data = np.array(lines, dtype=np.float64)

        path_averages = []
        path_process = np.divide(path_data[:, 1:3].T, path_data[:, 0])
        path_averages.extend([mstd(path_process[0]), mstd(path_process[1])])

        for i in range(3, 9):
            path_averages.append(mstd(path_data[:, i]))
        for avg in path_averages:
            path_average_f.write("({}, {})\t".format(round(avg[0], 2), round(avg[1], 2)))
        path_average_f.write("\n")






