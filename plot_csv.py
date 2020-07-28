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
mus = [[], [], [], []]
sigmas = [[], [], []]

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

    if line["mu"] == "0":
        mus[0].append(v)
    elif line["mu"] == "5":
        mus[1].append(v)
    elif line["mu"] == "20":
        mus[2].append(v)
    elif line["mu"] == "80":
        mus[3].append(v)
    else:
        logging.warn("unknown mu: " + line["mu"])

    if line["sigma"] == "0.5":
        sigmas[0].append(v)
    elif line["sigma"] == "1.0":
        sigmas[1].append(v)
    elif line["sigma"] == "2.0":
        sigmas[2].append(v)
    else:
        logging.warn("unknown sigma: " + line["sigma"])

mavg_norm = norm(np.array(mavg))
max_norm = norm(np.array(mmax))

for i in range(count):
    c = (0, 0, mavg_norm[i])
    t = "o"

widths = 0.8
quantile = [0.2, 0.8]
# plt.hist(x=test, bins=5, density=True,)
fig, axs = plt.subplots(2)
ax = axs[0]
ax.violinplot(mus, positions=[4, 1, 2, 3], showmeans=True, widths=widths)

ax.set_xlabel("mu")
ax.set_ylabel("mavg")
ax.legend(loc='best')
plt.sca(axs[0])
plt.xticks(np.arange(4) + 1, ('5', '20', '80', '250'))

ax = axs[1]
ax.violinplot(sigmas, positions=[1,2,3], showmeans=True,widths=widths)

ax.set_xlabel("sigma")
ax.set_ylabel("mavg")
plt.sca(axs[1])
plt.xticks(np.arange(3) + 1, ('0.5', '1.0', '2.0'))

fig.show()
