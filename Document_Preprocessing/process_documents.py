import os
import csv
import utils
import random
import itertools

source_dir = "./output"

target_dir = "./sampled_texts/"

sub1a = "./subset1a/"
sub1b = "./subset1b/"
sub2a = "./subset2a/"
sub2b = "./subset2b/"

by_speaker = dict()

selected_texts = list()
subset1_a = list()
subset1_b = list()
subset2_a = list()
subset2_b = list()

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

set1 = random.sample([n for n in range(12)], 6)
set2 = [n for n in range(12) if n not in set1]

subset1_a = list(itertools.chain.from_iterable([selected_texts[i*20:i*20+10] for i in set1]))
subset1_b = list(itertools.chain.from_iterable([selected_texts[i*20+10:i*20+20] for i in set1]))

subset2_a = list(itertools.chain.from_iterable([selected_texts[i*20:i*20+10] for i in set2]))
subset2_b = list(itertools.chain.from_iterable([selected_texts[i*20+10:i*20+20] for i in set2]))

random.shuffle(subset1_a)
random.shuffle(subset1_b)
random.shuffle(subset2_a)
random.shuffle(subset2_b)

for i in range(12):
    j = i * 5
    k = j + 5
    utils.output_csv(sub1a + str(i), subset1_a[j:k])
    utils.output_csv(sub1b + str(i), subset1_b[j:k])
    utils.output_csv(sub2a + str(i), subset2_a[j:k])
    utils.output_csv(sub2b + str(i), subset2_b[j:k])

utils.output_csv(target_dir + "everything", selected_texts)