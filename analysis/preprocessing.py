import constants
import annotator
import composite



#Read in all the data
annotators = list()
for i in range(constants.NUMBER_OF_FILES):

    tasks = constants.DATA + str(i) + ".txt"
    meta = constants.DATA_META + str(i) + ".txt"
    annotations = constants.DATA_ANNOTATIONS + str(i) + ".txt"
    #use "annotator" class
    new_annotator = annotator.annotator()
    new_annotator.from_raw(i, tasks, meta, annotations)

    annotators.append(new_annotator)
    
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

def stats(annotator_list):
    for annotator_object in annotator_list:
        ## get binom test for all left-right choices put together - per annotator looks fairly reasonable
        annotator_object.run_statistics()
        annotator_object.draw_all()

basic_numbers(annotators)
stats(annotators)