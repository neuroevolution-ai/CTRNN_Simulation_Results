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
parser.add_argument('--savefig',
                    type=str,
                    help='save figure? Requires xelatex to be installed. '
                         '(sudo apt-get install texlive-xetex )',
                    default='')
args = parser.parse_args()


def norm(x):
    return (x - min(x)) / (max(x) - min(x))


def split_into_buckets(data, property):
    property_values = set([e[property] for e in data])
    result = []
    for property_value in property_values:
        res = [e for e in data if e[property] == property_value]
        result.append((property_value, res))
    return result


def violinplot(data, ax, title, prop_name):
    plt.sca(ax)
    pure_data = [x[1] for x in data]
    values = [[float(y['mavg']) for y in x] for x in pure_data]
    labels = [x[0] for x in data]
    positions = range(len(values))
    ax.violinplot(values, positions=positions, widths=0.7)
    for v,p in zip(values, positions):
        plt.annotate("n=" + str(len(v)), (p-0.1, 200), annotation_clip=False)
    ax.set_xlabel(prop_name)
    ax.legend(loc='best')
    plt.xticks(np.arange(len(labels)), labels)
    ax.set_ylabel("mavg")
    plt.ylim(-200, +200)
    plt.yticks(range(-200, 201, 100))
    plt.grid(axis='y')


def histplot(data, ax, title):
    plt.sca(ax)
    colors = [
        (0.5, 0.0, 0.0),
        (0.5, 0.3, 0.3),
        (0.5, .6, 0.6),
        (0.5, 0.9, 0.9),
    ]
    plt.hist(x=data, density=False,
             bins=5,
             range=(-250, 250),
             cumulative=False,
             histtype='bar',
             label=('5', '20', '80', '250'),
             color=colors)

    plt.title(title)
    plt.legend(loc='best')

    plt.xlim(-150, +150)


def read_data(file):

    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        print(reader.fieldnames)
        data = list(reader)

    for d in data:
        d['mu'] = int(d['mu'])
        d['mavg'] = float(d['mavg'])
        d['max'] = float(d['max'])
        d['delta_t'] = float(d['delta_t'])
        d['sigma'] = float(d['sigma'])
        d['population_size'] = float(d['population_size'])
        d['number_generations'] = int(d['number_generations'])
        d['v_mask_param'] = int(d['v_mask_param'])
        d['w_mask_param'] = int(d['w_mask_param'])
        d['t_mask_param'] = int(d['t_mask_param'])
        d['number_fitness_runs'] = int(d['number_fitness_runs'])
        if d['mu'] == 0:
            # when 0 is used, it defaults to half the population
            d['mu'] = int(d['population_size']/2)
    return data

def split_and_plot(axis, data, property):
    splitted = split_into_buckets(data, property)
    splitted = sorted(splitted, key=lambda x: x[0])
    all = []
    for x in splitted: all.append(x)
    violinplot(splitted,axis, "asd", property)

def plot_all(axis, data):
    # draw entire population
    values = [d['mavg'] for d in data]
    axis.set_ylabel("mavg")
    plt.ylim(-200, +200)
    axis.violinplot(values, widths=0.3)
    plt.tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=False,
        labelbottom=False)
    plt.yticks(range(-200, 201, 100))
    plt.grid(axis='y')


data = read_data(args.csv)
fig, axes = plt.subplots(1)
# plot_all(axes[0], data)
# split_and_plot(axes[0], data, 'number_fitness_runs')
# split_and_plot(axes[1], data, 'sigma')
fig.set_size_inches(6, 3)
split_and_plot(axes, data, 'mu')
if args.savefig:
    fig.savefig(args.savefig)

fig.show()
