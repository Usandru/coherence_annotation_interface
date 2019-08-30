import preprocessing
import utilities
import networkx
import statsmodels
from statsmodels.stats.proportion import binom_test
from scipy.stats import chisquare
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

init_output_files()

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
word_count_top_label = "id,matches,total,p-value"
word_count_content = list()
for edgelist_set in list_of_edgelist_sets:
    edgelist_results = [word_count_top_label]

    for curr_edgelist in edgelist_set:
        l_nodes = [pair[constants.EDGE_LEFT] for pair in curr_edgelist.edge_list]
        r_nodes = [pair[constants.EDGE_RIGHT] for pair in curr_edgelist.edge_list]
        directions = [pair[constants.EDGE_KEYVALUE][constants.DIRECTION] for pair in curr_edgelist.edge_list]

        pair_list = list(zip(l_nodes, r_nodes))
        pred_list = list(curr_edgelist.sourcetext_object.predict_pairs(curr_edgelist.sourcetext_object.compare_length, pair_list))
        
        match_count = 0
        for i in range(len(directions)):
            if directions[i] == pred_list[i]:
                match_count += 1

        p_value = str(binom_test(match_count, len(directions)))

        edgelist_results.append(",".join([curr_edgelist.source_id, str(match_count), str(len(directions)), p_value]))

    word_count_content.append("\n".join(edgelist_results))

output_content(constants.OUTPUT_BINOM_TESTS, "\n\n\nWORDCOUNT BINOM TESTS, BY EDGELISTS\n")
output_content(constants.OUTPUT_BINOM_TESTS, "\n".join(word_count_content))

#sentence count
sentence_top_label = "id,matches,total,p-value"
sentence_count_content = list()
for edgelist_set in list_of_edgelist_sets:
    edgelist_results = [sentence_top_label]

    for curr_edgelist in edgelist_set:
        l_nodes = [pair[constants.EDGE_LEFT] for pair in curr_edgelist.edge_list]
        r_nodes = [pair[constants.EDGE_RIGHT] for pair in curr_edgelist.edge_list]
        directions = [pair[constants.EDGE_KEYVALUE][constants.DIRECTION] for pair in curr_edgelist.edge_list]

        pair_list = list(zip(l_nodes, r_nodes))
        pred_list = list(curr_edgelist.sourcetext_object.predict_pairs(curr_edgelist.sourcetext_object.compare_punctuation, pair_list))
        
        match_count = 0
        for i in range(len(directions)):
            if directions[i] == pred_list[i]:
                match_count += 1

        p_value = str(binom_test(match_count, len(directions)))

        edgelist_results.append(",".join([curr_edgelist.source_id, str(match_count), str(len(directions)), p_value]))

    sentence_count_content.append("\n".join(edgelist_results))

output_content(constants.OUTPUT_BINOM_TESTS, "\n\n\nSENTENCE COUNT BINOM TESTS, BY EDGELISTS\n")
output_content(constants.OUTPUT_BINOM_TESTS, "\n".join(sentence_count_content))

#compare to PRONOUN, CONJUNCTION and PRONOUN + CONJUNCTION count
coherence_element_top_label = "id,pronoun matches (p-val),conjunction matches (p-val),all-types matches (p-val),total"
coherence_element_count_content = list()
for edgelist_set in list_of_edgelist_sets:
    edgelist_results = [coherence_element_top_label]

    for curr_edgelist in edgelist_set:
        l_nodes = [pair[constants.EDGE_LEFT] for pair in curr_edgelist.edge_list]
        r_nodes = [pair[constants.EDGE_RIGHT] for pair in curr_edgelist.edge_list]
        directions = [pair[constants.EDGE_KEYVALUE][constants.DIRECTION] for pair in curr_edgelist.edge_list]

        pair_list = list(zip(l_nodes, r_nodes))
        pred_list_pron = list(curr_edgelist.sourcetext_object.predict_pairs(curr_edgelist.sourcetext_object.compare_pronouns, pair_list))
        pred_list_conj = list(curr_edgelist.sourcetext_object.predict_pairs(curr_edgelist.sourcetext_object.compare_conjunctions, pair_list))
        pred_list_all = list(curr_edgelist.sourcetext_object.predict_pairs(curr_edgelist.sourcetext_object.compare_all_coherence_elements, pair_list))
        
        pron_match_count = 0
        conj_match_count = 0
        all_match_count = 0
        for i in range(len(directions)):
            if directions[i] == pred_list_pron[i]:
                pron_match_count += 1
            if directions[i] == pred_list_conj[i]:
                conj_match_count += 1
            if directions[i] == pred_list_all[i]:
                all_match_count += 1

        p_value_pron = str(pron_match_count) + " (" +  str(binom_test(pron_match_count, len(directions)))  + ")"
        p_value_conj = str(conj_match_count) + " (" +  str(binom_test(conj_match_count, len(directions)))  + ")"
        p_value_all = str(all_match_count) + " (" +  str(binom_test(all_match_count, len(directions)))  + ")"

        edgelist_results.append(",".join([curr_edgelist.source_id, p_value_pron, p_value_conj, p_value_all, str(len(directions))]))

    coherence_element_count_content.append("\n".join(edgelist_results))

output_content(constants.OUTPUT_BINOM_TESTS, "\n\n\nPRONOUN AND CONJUNCTION COUNT BINOM TESTS, BY EDGELISTS\n")
output_content(constants.OUTPUT_BINOM_TESTS, "\n".join(coherence_element_count_content))

#compare number of types
types_top_label = "id,matches,total,p-value"
types_content = list()
for edgelist_set in list_of_edgelist_sets:
    edgelist_results = [types_top_label]

    for curr_edgelist in edgelist_set:
        l_nodes = [pair[constants.EDGE_LEFT] for pair in curr_edgelist.edge_list]
        r_nodes = [pair[constants.EDGE_RIGHT] for pair in curr_edgelist.edge_list]
        directions = [pair[constants.EDGE_KEYVALUE][constants.DIRECTION] for pair in curr_edgelist.edge_list]

        pair_list = list(zip(l_nodes, r_nodes))
        pred_list = list(curr_edgelist.sourcetext_object.predict_pairs(curr_edgelist.sourcetext_object.compare_number_of_types , pair_list))
        
        match_count = 0
        for i in range(len(directions)):
            if directions[i] == pred_list[i]:
                match_count += 1

        p_value = str(binom_test(match_count, len(directions)))

        edgelist_results.append(",".join([curr_edgelist.source_id, str(match_count), str(len(directions)), p_value]))

    types_content.append("\n".join(edgelist_results))

output_content(constants.OUTPUT_BINOM_TESTS, "\n\n\nTYPE COUNT BINOM TESTS, BY EDGELISTS\n")
output_content(constants.OUTPUT_BINOM_TESTS, "\n".join(types_content))

#generate agreement statistics:
expected_frequencies_by_max_categories = [[1], #single annotator
                                          [0.5, 0.5], #two annotators
                                          [0.25, 0.75], #three annotators
                                          [0.125, 0.5, 0.375], #four annotators
                                          [0.0625, 0.3125, 0.625], #five annotators
                                          [0.03125, 0.1875, 0.46875, 0.3125]] #six annotators

agreement_test_labels = "number of annotators,counts (likelihood),chisquare test val,p-value"

for merged_edgelist in list_of_merged_edgelists:
    agreement_test_content = [agreement_test_labels]
    agreement_counts_by_categories = [[0],
                                      [0,0],
                                      [0,0],
                                      [0,0,0],
                                      [0,0,0],
                                      [0,0,0,0]]
    for edge in merged_edgelist.edge_list:
        number_of_annotators = len(edge[constants.EDGE_KEYVALUE][constants.AGREEMENT_COMPONENTS])
        if number_of_annotators > 6 or edge[constants.EDGE_KEYVALUE][constants.AGREEMENT] / number_of_annotators < 0.5:
            continue
        agreement_counts_by_categories[number_of_annotators - 1][number_of_annotators - edge[constants.EDGE_KEYVALUE][constants.AGREEMENT]] += 1

    for i in range(len(agreement_counts_by_categories)):
        curr_freq_list = expected_frequencies_by_max_categories[i]
        curr_count = agreement_counts_by_categories[i]

        count_sum = sum(curr_count)

        expected_freq_list = [count_sum * freq for freq in curr_freq_list]

        chisq, p_value = chisquare(curr_count, expected_freq_list)

        count = ";".join(list(map(str, curr_count))) + " (" + ";".join(list(map(str, curr_freq_list))) + ")"

        agreement_test_content.append(",".join([str(i+1), count, str(chisq), str(p_value)]))

    output_content(constants.OUTPUT_AGREEMENT_TESTS, "\n" + merged_edgelist.source_id + "\n")
    output_content(constants.OUTPUT_AGREEMENT_TESTS, "\n".join(agreement_test_content))

#minimal pair testing
minimal_pair_dict = dict([(pair[0], pair[2]) for pair in constants.EXPECTED_MINIMAL_PAIR_OUTCOMES])
minimal_pair_count_by_node = dict([(pair[0], 0) for pair in constants.EXPECTED_MINIMAL_PAIR_OUTCOMES])
minimal_pair_count_all = dict([(pair[0], 0) for pair in constants.EXPECTED_MINIMAL_PAIR_OUTCOMES])

minimal_pair_top_label = "id,matches,total,p-value"
minimal_pair_content = [minimal_pair_top_label]

for minimal_pair_edgelist in minimal_pair_set[:-1]:
    count = 0
    for edge in minimal_pair_edgelist.edge_list:
        minimal_pair_count_all[edge[0]] += 1
        if minimal_pair_dict[edge[0]] == edge[constants.EDGE_KEYVALUE][constants.DIRECTION]:
            minimal_pair_count_by_node[edge[0]] += 1
            count += 1
    
    p_value = binom_test(count, len(minimal_pair_edgelist.edge_list))

    minimal_pair_content.append(",".join([minimal_pair_edgelist.source_id, str(count), str(len(minimal_pair_edgelist.edge_list)), str(p_value)]))

count = 0
for edge in merged_minimal_pair.edge_list:
    if minimal_pair_dict[edge[0]] == edge[constants.EDGE_KEYVALUE][constants.DIRECTION]:
        count += 1
p_value = binom_test(count, len(merged_minimal_pair.edge_list))
minimal_pair_content.append(",".join([minimal_pair_edgelist.source_id, str(count), str(len(minimal_pair_edgelist.edge_list)), str(p_value)]))

output_content(constants.OUTPUT_BINOM_TESTS, "\n\n\n MINIMAL PAIR BINOM TESTS")
output_content(constants.OUTPUT_BINOM_TESTS, "\n".join(minimal_pair_content))

for node in constants.EXPECTED_MINIMAL_PAIR_OUTCOMES:
    pass
print(minimal_pair_count_by_node)
print(minimal_pair_count_all)

#generate the graphs and check for cycles and transitivity
base_graphs = list()
base_graphs_cycles = list()
for curr_edgelist in list_of_edgelist_sets[0]:
    all_nodes = [edge[0] for edge in curr_edgelist.edge_list] + [edge[1] for edge in curr_edgelist.edge_list]
    curr_digraph = networkx.DiGraph()
    curr_digraph.add_nodes_from(all_nodes)
    for edge in curr_edgelist.edge_list:
        if edge[constants.EDGE_KEYVALUE][constants.DIRECTION] == constants.LEFT:
            curr_digraph.add_edge(edge[constants.EDGE_RIGHT], edge[constants.EDGE_LEFT], agreement=edge[constants.EDGE_KEYVALUE][constants.AGREEMENT])
        elif edge[constants.EDGE_KEYVALUE][constants.DIRECTION] == constants.RIGHT:
            curr_digraph.add_edge(edge[constants.EDGE_LEFT], edge[constants.EDGE_RIGHT], agreement=edge[constants.EDGE_KEYVALUE][constants.AGREEMENT])

    base_graphs.append(curr_digraph)
    base_graphs_cycles.append(list(networkx.algorithms.simple_cycles(curr_digraph)))
    networkx.write_graphml(curr_digraph, constants.OUTPUT + curr_edgelist.source_id + ".xml")

no_minimal_pair_graphs = list()
no_minimal_pair_graphs_cycles = list()
for curr_edgelist in list_of_edgelist_sets[3]:
    all_nodes = [edge[0] for edge in curr_edgelist.edge_list] + [edge[1] for edge in curr_edgelist.edge_list]
    curr_digraph = networkx.DiGraph()
    curr_digraph.add_nodes_from(all_nodes)
    for edge in curr_edgelist.edge_list:
        if edge[constants.EDGE_KEYVALUE][constants.DIRECTION] == constants.LEFT:
            curr_digraph.add_edge(edge[constants.EDGE_RIGHT], edge[constants.EDGE_LEFT], agreement=edge[constants.EDGE_KEYVALUE][constants.AGREEMENT])
        elif edge[constants.EDGE_KEYVALUE][constants.DIRECTION] == constants.RIGHT:
            curr_digraph.add_edge(edge[constants.EDGE_LEFT], edge[constants.EDGE_RIGHT], agreement=edge[constants.EDGE_KEYVALUE][constants.AGREEMENT])

    no_minimal_pair_graphs.append(curr_digraph)
    no_minimal_pair_graphs_cycles.append(list(networkx.algorithms.simple_cycles(curr_digraph)))
    networkx.write_graphml(curr_digraph, constants.OUTPUT + curr_edgelist.source_id + ".xml")


#run the analysis on time