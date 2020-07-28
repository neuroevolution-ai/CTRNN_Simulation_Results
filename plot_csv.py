import os
import json
import argparse
import logging
import csv
import pickle

import matplotlib.pyplot as plt

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description='Visualize experiment results')
parser.add_argument('--csv', type=str, help='location of csv file', default='output.csv')
args = parser.parse_args()

with open( args.csv, 'r' ) as f:
    reader = csv.DictReader(f)
    i = 0
    for line in reader:

        x = i

        y=float( line["mavg"])
        c = "blue"
        t = "o"
        i+=1
        plt.scatter(x=x, y=y, marker=t, c=c)


plt.show()