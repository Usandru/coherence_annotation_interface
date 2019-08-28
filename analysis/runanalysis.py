import preprocessing
import utilities
import networkx
import statsmodels
from statsmodels.stats.proportion import binom_test
import annotator
import constants
import edgelist

def init_output_files():
    for output_path in constants.OUTPUT_PATHS:
        with open(output_path, mode='w', encoding='utf-8') as file_init:
            file_init.write("")

def output_content(path, content):
    with open(path, mode='a', encoding='utf-8') as output_file:
        output_file.write(content)

source_and_annotators = preprocessing.generate_core_datastructures()

#raw, minimal pairs only, cast to original tag, slider only, binary only (merged and unmerged for all)

#generate the basic summary
all_annotators = source_and_annotators.annotator_list
annotators_above_10_annotations = [annotator for annotator in all_annotators if annotator.number_of_annotations > 10]

annotator_summary = list()
for annotator in all_annotators:
    content, label = annotator.print_summary()
    annotator_summary.append(content)

annotator_summary.insert(0, label)
joined_content = "\n".join(annotator_summary)

output_content(constants.OUTPUT_GENERAL_SUMMARY, joined_content)

#get the edgelists for the above-10 annotators
base_edgelist_set = list()
for annotator in annotators_above_10_annotations:
    base_edgelist_set.append(annotator.generate_edgelist())

#generate the edge_lists and obtain the more complex data
minimal_pair_set = [edgelist.filter_to_minimal_pairs() for edgelist in base_edgelist_set]
slider_only_set = [edgelist.copy_by_mode(constants.SLIDER) for edgelist in base_edgelist_set]
binary_only_set = [edgelist.copy_by_mode(constants.BINARY) for edgelist in base_edgelist_set]
simplified_base_edgelist_set = [edgelist.cast_tags_to_original() for edgelist in base_edgelist_set]
simplified_slider_only_set = [edgelist.cast_tags_to_original() for edgelist in slider_only_set]
simplified_binary_only_set = [edgelist.cast_tags_to_original() for edgelist in binary_only_set]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

list_of_edgelist_sets = [base_edgelist_set, slider_only_set, binary_only_set, simplified_base_edgelist_set, simplified_slider_only_set, simplified_binary_only_set]

merged_minimal_pair = edgelist.merge_list_of_edgelists(minimal_pair_set)

list_of_merged_edgelists = [merged_minimal_pair]

minimal_pair_set.append(merged_minimal_pair)

for set_of_edgelists in list_of_edgelist_sets:
    merged_set = edgelist.merge_list_of_edgelists(set_of_edgelists)
    set_of_edgelists.append(merged_set)
    list_of_merged_edgelists.append(merged_set)

#generate the basic statistical information

#binom test of left/right for above-10 annotators + binom test for aggregate
agg_lefts = 0
agg_rights = 0
binom_test_results = ["id,p-value"]
for annotator in annotators_above_10_annotations:
    p_val = binom_test([annotator.number_of_lefts, annotator.number_of_rights], annotator.number_of_lefts + annotator.number_of_rights)
    binom_test_results.append(str(annotator.id) + "," + str(p_val))
    agg_lefts += annotator.number_of_lefts
    agg_rights += annotator.number_of_rights

binom_test_results.append("aggregate," + str(binom_test([agg_lefts, agg_rights], agg_lefts + agg_rights)))

output_content(constants.OUTPUT_BINOM_TESTS, "LEFT-RIGHT BINOM TESTS, INDIVIDUAL AND AGGREGATE\n")
output_content(constants.OUTPUT_BINOM_TESTS, "\n".join(binom_test_results))


#compare edge list outcome to WORD COUNT
#compare to PRONOUN, CONJUNCTION and PRONOUN + CONJUNCTION count


#generate the graphs and check for cycles and transitivity

#run the analysis on time