### build a sourcetexts object by reading the sourcetext folder path and constructing a dict of dicts
### keyed by text id, and then trait
### add in functions for passing lists of text pairs and edge directions and returning analysis on this
### make the object saveable?

# TRAITS
# word count
# "sentences" == number of punctuation marks
# word types
# number of pronouns (need a list - generate a list of all word types of the whole set of texts)
# number of conjunctions (need a list)
# (if possible) number of proper nouns
# author (this is more complex to handle)
# 

import constants
import json
import csv
import utilities

def get_csv(filename):
    csv_data = list()
    with open(filename, newline='', encoding='utf-8') as curr_file:
        curr_reader = csv.reader(curr_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in curr_reader:
            if row != []:
                csv_data.append(row)
        curr_file.close()
    return csv_data

class sourcetexts:

    def __init__(self, source_text_path, source_text_config):
        self.text_id_dict = dict()

        with open(source_text_config, mode="r", encoding="utf-8") as file:
            config = json.load(file)
        
        for i in range(config[constants.NUMBER_OF_SOURCE_TEXTS]):
            path = source_text_path + str(i) + ".csv"

            data = get_csv(path)

            for text_data in data:
                text_id = text_data[constants.CSV_ID] + " " + text_data[constants.CSV_TAG]
                self.text_id_dict[text_id] = dict()

                data_text = text_data[constants.CSV_TEXT].replace("LINEBREAK", "")
                self.text_id_dict[text_id][constants.TEXT] = data_text
                self.text_id_dict[text_id][constants.WORD_COUNT] = len(data_text.split())

                sentence_count = 0
                for item in constants.PUNCTUATION:
                    sentence_count += data_text.count(item)

                self.text_id_dict[text_id][constants.SENTENCES] = sentence_count

                #add more things

    def predict_pairs(self, compare_func, pair_list):
        return map(compare_func, pair_list)

    def compare_length(self, pair):
        if self.text_id_dict[pair[0]][constants.WORD_COUNT] < self.text_id_dict[pair[1]][constants.WORD_COUNT]:
            return constants.LEFT
        elif self.text_id_dict[pair[0]][constants.WORD_COUNT] > self.text_id_dict[pair[1]][constants.WORD_COUNT]:
            return constants.RIGHT
        else:
            return constants.NULL

    def compare_number_of_types(self, pair):
        #needs a lemmatizer
        left_types = utilities.get_text_types(self.text_id_dict[pair[0]][constants.TEXT])
        right_types = utilities.get_text_types(self.text_id_dict[pair[1]][constants.TEXT])
        
        if len(left_types) > len(right_types):
            return constants.LEFT
        elif len(left_types) < len(right_types):
            return constants.RIGHT
        else:
            return constants.NULL

    def compare_punctuation(self, pair):
        left_count = self.text_id_dict[pair[0]][constants.TEXT] #need something to actually count this
        right_count = self.text_id_dict[pair[1]][constants.TEXT]

        if left_count > right_count:
            return constants.LEFT
        elif left_count < right_count:
            return constants.RIGHT
        else:
            return constants.NULL

    def get_all_texts(self):
        text_list = list()
        for key in self.text_id_dict.keys():
            text_list.append(self.text_id_dict[key][constants.TEXT])
        return text_list

#generate output files of normal text statistics - distribution and frequency and so on
#