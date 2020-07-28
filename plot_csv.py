import os
import json
import argparse
import logging
import csv
import pickle
import numpy as np

import matplotlib.pyplot as plt

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description='Visualize experiment results')
parser.add_argument('--csv', type=str, help='location of csv file', default='output.csv')
args = parser.parse_args()


def norm(x):
    return (x - min(x)) / (max(x) - min(x))


count = -1
sigma = []
mavg = []
delta = []
mu = []
mmax = []
with open(args.csv, 'r') as f:
    reader = csv.DictReader(f)

    print(reader.fieldnames)
    data = list(reader)

# test = np.column_stack((mavg, sigma, mu))
mus05 = [[], [], [], []]
mus10 = [[], [], [], []]
mus20 = [[], [], [], []]


for line in data:

    sigma.append(float(line["sigma"]))
    mu.append(float(line["mu"]))
    v = float(line["mavg"])
    mavg.append(v)
    mmax.append(float(line["max"]))
    count += 1

    if line['number_fitness_runs'] == '0':
        logging.debug("skip, number_fitness_runs " + line['number_fitness_runs'])
        continue

    if line['t_mask_param'] == '95':
        logging.debug("skip, t_mask_param " + line['t_mask_param'])
        continue

    if line['v_mask_param'] == '95':
        logging.debug("skip, v_mask_param " + line['v_mask_param'])
        continue

    if line["sigma"] == "0.5":
        mus = mus05
    elif line["sigma"] == "1.0":
        mus = mus10
    elif line["sigma"] == "2.0":
        mus = mus20
    else:
        logging.warn("unknown sigma: " + line["sigma"])
    if line["mu"] == "0":
        mus[3].append(v)
    elif line["mu"] == "5":
        mus[0].append(v)
    elif line["mu"] == "20":
        mus[1].append(v)
    elif line["mu"] == "80":
        mus[2].append(v)
    else:
        logging.warn("unknown mu: " + line["mu"])


mavg_norm = norm(np.array(mavg))
max_norm = norm(np.array(mmax))

for i in range(count):
    c = (0, 0, mavg_norm[i])
    t = "o"

widths = 0.8
quantile = [0.2, 0.8]
# plt.hist(x=test, bins=5, density=True,)
fig, axs = plt.subplots(3)

def violinplot(data,ax, title):
    ax.violinplot(data, positions=[1, 2, 3, 4], widths=widths)
    for idx, d in enumerate( data):
        count = len(d)
        plt.annotate("n="+str(len(d)), (idx+0.88,200), annotation_clip=False)
    ax.set_xlabel("mu")
    ax.set_ylabel("mavg")
    ax.legend(loc='best')
    plt.sca(ax)
    plt.xticks(np.arange(4) + 1, ('5', '20', '80', '250'))
    plt.title(title)
    plt.ylim(-200,+200)

    plt.yticks( range(-200,201,100))
    plt.grid(axis='y')



violinplot(mus05,axs[0], "sigma=0.5")
violinplot(mus10,axs[1], "sigma=1.0")
violinplot(mus20,axs[2], "sigma=2.0")

fig.show()
