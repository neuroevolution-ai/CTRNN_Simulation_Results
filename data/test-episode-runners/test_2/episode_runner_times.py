import os
import json
import numpy as np


def calculate(directory):
    logs = []
    for dir in os.listdir(directory):
        with open(os.path.join(directory, dir, "Log.json"), "r") as log_file:
            logs.append(json.load(log_file))

    mean_times = []
    std_times = []
    max_times = []
    min_times = []

    for log in logs:
        mean_times.append(np.mean([x["ep_runner_mean_time"] for x in log]))
        std_times.append(np.mean([x["ep_runner_std_time"] for x in log]))
        max_times.append(np.mean([x["ep_runner_max_time"] for x in log]))
        min_times.append(np.mean([x["ep_runner_min_time"] for x in log]))

    return np.mean(mean_times), np.std(std_times), np.max(max_times), np.min(min_times)


def main():
    training_mean, training_std, training_max, training_min = calculate("training_episode_runner")
    visualize_mean, visualize_std, visualize_max, visualize_min = calculate("visualize_episode_runner")

    print("Mean | Training {} | Visualize {}".format(training_mean, visualize_mean))
    print("Std | Training {} | Visualize {}".format(training_std, visualize_std))
    print("Max | Training {} | Visualize {}".format(training_max, visualize_max))
    print("Min | Training {} | Visualize {}".format(training_min, visualize_min))


if __name__ == "__main__":
    main()
