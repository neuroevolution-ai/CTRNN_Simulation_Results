import os
import json
import argparse
import logging
import csv
import pickle
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
import tikzplotlib

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
    ax.violinplot(values, positions=positions, widths=0.7, showmedians=True, vert=False)
    for v,p in zip(values, positions):
        # plt.annotate("n=" + str(len(v)), (p-0.1, 178), annotation_clip=False)
        # plt.text(200, (p/len(positions))+0.1, "n=" + str(len(v)), transform=ax.get_xaxis_transform())
        plt.text(max(v)+5, p-0.1, "\scriptsize n=" + str(len(v)), fontsize=6)
        ax.scatter(x=v, y=[p]*len(v), s=[100]*len(v), marker="|", color='#ff9900', alpha=0.3)

    ax.set_ylabel(prop_name.replace('_', ' '))
    ax.legend(loc='best')
    plt.yticks(np.arange(len(labels)), labels)
    ax.set_xlabel("mavg")
    plt.xlim(-200, +300)
    plt.xticks(range(-200, 201, 100))
    plt.grid(axis='x')


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
        d['number_neurons'] = float(d['number_neurons'])
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
    axis.set_xlabel("mavg")
    plt.xlim(-200, +300)
    axis.violinplot(values, widths=0.3, showmedians=True, vert=False)
    plt.tick_params(
        axis='y',
        which='both',
        top=False,
        bottom=False,
        left=False,
        right=False,
        labelleft=False,
        labelbottom=False)
    #plt.xticks(range(-200, 201, 100))
    # plt.annotate("n=" + str(len(values)), (1-0.03, 190), annotation_clip=False)
    plt.text(1-20, 0.85, "n=" + str(len(values)))
    plt.grid(axis='x')

def filter_data(data):
    filtered = []
    for d in data:
        if d['v_mask_param'] == 95:
            continue
        if d['t_mask_param'] == 95:
            continue
        if d['sigma'] == 2.0:
            continue
        if d['mu'] == 250:
            continue
        if d['number_fitness_runs'] == 1:
            continue

        if d['mu'] == 20:
            continue
        if d['mu'] == 5:
            continue
        filtered.append(d)
    return filtered

#matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "xelatex",
    'font.family': 'serif',
    'pgf.rcfonts': False,
    'text.usetex': True,
})


width_inches = 2
height_inches = width_inches / 2

data = read_data(args.csv)
data = filter_data(data)

def xplotsplit(parameter):
    fig, axes = plt.subplots(1)
    if parameter=='all':
        fig.set_size_inches(width_inches , height_inches )
        plot_all(axes, data)
    else:
        fig.set_size_inches(width_inches, height_inches)
        split_and_plot(axes, data, parameter)
    # fig.savefig('hyper_'+parameter+'_unfiltered.pgf')
    tikzplotlib.clean_figure()
    tikzplotlib.save(filepath='hyper_'+parameter+'_filtered2mu80.tex', strict=True,  axis_height='4cm', axis_width='5cm')
    fig.show()

xplotsplit('all')
xplotsplit('mu')
xplotsplit('sigma')
# xplotsplit('number_neurons')
