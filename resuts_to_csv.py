import os
import json
import argparse
import logging
import csv


def read_simulations(base_directory):
    simulation_runs = []
    for d in os.listdir(base_directory):
        simulation_folder = os.path.join(base_directory, d)

        # noinspection PyBroadException
        try:
            with open(os.path.join(simulation_folder, 'Configuration.json'), "r") as read_file:
                conf = json.load(read_file)
        except:
            conf = None
            logging.error("couldn't read conf for " + str(simulation_folder), exc_info=True)
            
        # noinspection PyBroadException
        try:
            with open(os.path.join(simulation_folder, 'Log.json'), 'r') as read_file:
                log = json.load(read_file)
        except Exception:
            log = None
            logging.error("couldn't read log for " + str(simulation_folder), exc_info=True)
        sim = {
            "dir": d,
            "conf": conf,
            "log": log,
        }
        simulation_runs.append(sim)
    return simulation_runs


def get_attribute_or_none(d, attr):
    if attr in d:
        return d[attr]
    return None


def walk_dict(node, callback_node, depth=0):
    for key, item in node.items():
        if isinstance(item, dict):
            callback_node(key, item, depth, False)
            walk_dict(item, callback_node, depth + 1)
        else:
            callback_node(key, item, depth, True)


def gather_info_for_csv(simulation):
    log = simulation["log"]
    conf = simulation["conf"]
    generations = [i for i in range(len(log))]
    avg = [generation["avg"] for generation in log]
    maximum = [generation["max"] for generation in log]
    brain = conf["brain"]
    trainer = conf["trainer"]
    episode_runner = conf["episode_runner"]
    del conf["brain"]
    del conf["trainer"]
    del conf["episode_runner"]

    return {"gen": str(max(generations)),
            "mavg": str(max(avg)),
            "max": str(max(maximum)),
            "directory": simulation["dir"], **conf, **brain, **trainer, **episode_runner}


logging.basicConfig()
parser = argparse.ArgumentParser(description='Visualize experiment results')
parser.add_argument('--dir', metavar='dir', type=str, help='base directory for input',
                    default='data')
parser.add_argument('--csv', metavar='type', type=str, help='location of output csv file', default='output.csv')
args = parser.parse_args()

data = []

for simulation in read_simulations(args.dir):
    data.append(gather_info_for_csv(simulation))

keys = data[0].keys()
with open(args.csv, 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)
    logging.info("log written to " + str(args.csv))
