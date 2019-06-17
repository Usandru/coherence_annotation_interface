import os
import csv
import utils
import random

source_dir = "./output"

target_dir = "./sampled_texts/"

by_speaker = dict()

selected_texts = list()

counter = 0
for filename in os.listdir(source_dir):
    data = utils.get_csv(source_dir + "/" + filename)
    for row in data:
        curr_row = row.copy()
        curr_row.append(filename[:-4])
        curr_row.append("ORIGINAL")
        curr_row.append(counter)
        counter += 1
        if row[1] in by_speaker:
            by_speaker[row[1]].append(curr_row)
        else:
            by_speaker[row[1]] = [curr_row]

for key in list(by_speaker.keys()):
    if len(by_speaker[key]) < 40:
        by_speaker.pop(key)
    else:
        selected_texts.extend(random.sample(by_speaker[key], 20))

random.shuffle(selected_texts)

utils.output_csv(target_dir + "everything", selected_texts)