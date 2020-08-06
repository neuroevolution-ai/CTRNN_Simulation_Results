import os
import json
import argparse
import logging
import csv
import pickle

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


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
            try:
                with open(os.path.join(simulation_folder, 'Log.pkl'), 'rb') as read_file_log:
                    log = pickle.load(read_file_log)
            except:
                with open(os.path.join(simulation_folder, 'Log.json'), 'r') as read_file:
                    log = json.load(read_file)
        except Exception:
            log = None
            logging.error("couldn't read log for " + str(simulation_folder), exc_info=True)

        plot_path = os.path.join(simulation_folder, 'plot.png')
        if os.path.isfile(plot_path):
            # plot_path = os.path.abspath(plot_path)
            plot_path = "=HYPERLINK(\"" + plot_path + "\")"
        else:
            logging.warning("no plot found")
            plot_path = None

        sim = {
            "dir": d,
            "conf": conf,
            "log": log,
            "plot": plot_path,
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

    if not conf:
        logging.warning("conf doesn't exist.")
        return

    if log:
        generations = [i for i in range(len(log))]
        if hasattr(log, "chapters"):
            min, avg, std, maximum = log.chapters["fitness"].select("min", "avg", "std", "max")
        else:
            try:
                avg = [generation["avg"] for generation in log]
                maximum = [generation["max"] for generation in log]
            except:
                generations = [-1]
                avg = [0]
                maximum = [0]
                logging.warning("couldn't read avg and max from log")
    else:
        logging.warning("no log found in simulation on path: " + str(simulation["dir"]))
        generations = [-1]
        avg = [0]
        maximum = [0]

    try:
        brain = conf["brain"]
        trainer = conf["optimizer"]
        episode_runner = conf["episode_runner"]
        del conf["brain"]
        del conf["optimizer"]
        del conf["episode_runner"]
    except:
        logging.warning("could not locate brain, optimizer or ep_runner in conf.")
        brain = {}
        trainer = {}
        episode_runner = {}

    return {"gen": str(max(generations)),
            "mavg": str(max(avg)),
            "max": str(max(maximum)),
            "directory": simulation["dir"],
            "plot": simulation["plot"],
            **conf, **brain, **trainer, **episode_runner}


logging.basicConfig()
parser = argparse.ArgumentParser(description='Visualize experiment results')
parser.add_argument('--dir', metavar='dir', type=str, help='base directory for input',
                    default='data')
parser.add_argument('--csv', metavar='type', type=str, help='location of output csv file', default=None)
args = parser.parse_args()

if not args.csv:
    args.csv = os.path.basename(args.dir) + ".csv"

data = []
keys = []
for simulation in read_simulations(args.dir):
    d = gather_info_for_csv(simulation)
    if d:
        data.append(d)
        keys += d.keys()

# make keys unique while preserving order
keys = [x for i, x in enumerate(keys) if i == keys.index(x)]

with open(args.csv, 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)
    logging.info("log written to " + str(args.csv))
