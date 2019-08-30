import constants
import annotator
import sourcetexts
import utilities
import string
import networkx as nx
from collections import Counter

#Read in all the data
def generate_annotators(sourcetext_object):
    annotators = list()
    for i in range(constants.NUMBER_OF_FILES):

        tasks = constants.DATA + str(i) + ".txt"
        meta = constants.DATA_META + str(i) + ".txt"
        annotations = constants.DATA_ANNOTATIONS + str(i) + ".txt"
        #use "annotator" class
        new_annotator = annotator.annotator(sourcetext_object)
        new_annotator.from_raw(i, tasks, meta, annotations)

        annotators.append(new_annotator)
    return annotators
    
def basic_numbers(annotator_list):
    new_composite = composite.composite(annotator_list)
    agreement = new_composite.agreement()

    total_agreement = 0
    twos = 0
    two_ag = 0
    threes = 0
    three_ag = 0
    fours = 0
    four_ag = 0
    fives = 0
    five_ag = 0
    sixes = 0
    six_ag = 0
    for i in range(len(agreement)):
        current = agreement[i]

        if current[1] + current[2] == 2:
            twos += 1
            if current[1] == 0 or current[2] == 0:
                two_ag += 1

        if current[1] + current[2] == 3:
            threes += 1
            if current[1] == 0 or current[2] == 0:
                three_ag += 1

        if current[1] + current[2] == 4:
            fours += 1
            if current[1] == 0 or current[2] == 0:
                four_ag += 1

        if current[1] + current[2] == 5:
            fives += 1
            if current[1] == 0 or current[2] == 0:
                five_ag += 1

        if current[1] + current[2] == 6:
            sixes += 1
            if current[1] == 0 or current[2] == 0:
                six_ag += 1

        if current[1] == 0 or current[2] == 0:
            total_agreement += 1

    print("Total number of pairs: " + str(len(agreement)))
    print("Pairs with two annotations, and number of total agreements: " + str(twos) + " " + str(two_ag))
    print("Pairs with three annotations, and number of total agreements: " + str(threes) + " " + str(three_ag))
    print("Pairs with four annotations, and number of total agreements: " + str(fours) + " " + str(four_ag))
    print("Pairs with five annotations, and number of total agreements: " + str(fives) + " " + str(five_ag))
    print("Pairs with six annotations, and number of total agreements: " + str(sixes) + " " + str(six_ag))
    print("Overall total agreement count: " + str(total_agreement))

def get_types_from_texts(list_of_texts):
    joined_text = " ".join(list_of_texts)
    casefolded_text = joined_text.casefold()
    punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))
    punctuation_stripped_text = casefolded_text.translate(punctuation_table)
    types = Counter(punctuation_stripped_text.split())
    return types.most_common()

def get_types(source_text_object):
    source_text_list = source_text_object.get_all_texts()

    all_types = get_types_from_texts(source_text_list)
    print(len(all_types))

    with open(constants.TEXT_TYPES_OUTPUT, mode='a', encoding='utf-8') as output_file:
        output_file.writelines("\n".join([str(item) for item in all_types]))

class generate_core_datastructures:
    def __init__(self):
        self.source_text_object = sourcetexts.sourcetexts(constants.ORIGINALS, constants.ORIGINALS_CONFIG)
        self.annotator_list = generate_annotators(self.source_text_object)



#basic_numbers(annotators)
#print(utilities.minimal_pair_summary(annotators))