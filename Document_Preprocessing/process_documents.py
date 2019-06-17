import os
import csv
import utils

source_dir = "./output"

by_speaker = dict()

counter = 0
for filename in os.listdir(source_dir):
    data = utils.get_csv(source_dir + "/" + filename)
    print(data)
    if counter >= 2:
        break
    counter += 1