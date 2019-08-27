import constants
import annotator
import networkx as nx
import string
from collections import Counter
#import statsmodels.stats as sm_st
#from statsmodels.stats.proportion import binom_test
#import matplotlib.pyplot as plt

def reverse_direction(direction):
    if direction == constants.LEFT:
        return constants.RIGHT
    elif direction == constants.RIGHT:
        return constants.LEFT
    else:
        return constants.NULL

def same_num_id(left_id, right_id):
    l_num = left_id.split()[0]
    r_num = right_id.split()[0]
    if l_num == r_num:
        return True
    else:
        return False

def tag_is_original(text_id):
    _, tag = text_id.split()
    if tag == constants.TAG_ORIGINAL:
        return True
    else:
        return False

def compare_ids(left_id, right_id):
    l_num, l_tag = left_id.split()
    r_num, r_tag = right_id.split()

    if l_num == r_num:
        if l_tag == constants.TAG_ORIGINAL:
            return constants.LEFT
        else:
            return constants.RIGHT
    elif int(l_num) < int(r_num):
        return constants.LEFT
    else:
        return constants.RIGHT

def minimal_pair_agreement(list_of_annotators):
    m_p_dict = dict()
    for annotator_object in list_of_annotators:
        for m_p_tuple in annotator_object.minimal_pairs:
            if m_p_tuple[0] not in m_p_dict:
                m_p_dict[m_p_tuple[0]] = {m_p_tuple[1] : 0,
                                          m_p_tuple[2] : 0,
                                          constants.NULL : 0}
            
            if m_p_tuple[3] == constants.LEFT:
                m_p_dict[m_p_tuple[0]][m_p_tuple[1]] += 1
            elif m_p_tuple[3] == constants.RIGHT:
                m_p_dict[m_p_tuple[0]][m_p_tuple[2]] += 1
            else:
                m_p_dict[m_p_tuple[0]][constants.NULL] += 1
    
    return m_p_dict

def minimal_pair_summary(list_of_annotators):
    m_p_agreement = minimal_pair_agreement(list_of_annotators)

    summary_string = list()

    for m_p in m_p_agreement.keys():
        single_text = list()
        for tag in m_p_agreement[m_p].keys():
            temp = m_p + " " + tag + " = " + str(m_p_agreement[m_p][tag])
            single_text.append(temp)
        summary_string.append(", ".join(single_text))

    return "\n".join(summary_string)

def get_text_types(text):
    casefolded_text = text.casefold()
    punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))
    punctuation_stripped_text = casefolded_text.translate(punctuation_table)
    types = Counter(punctuation_stripped_text.split())
    return types.most_common()

def normalize_slider(graph):
    #create copy of graph

    weights = nx.get_edge_attributes(graph, constants.WEIGHT)
    weights.values
    print(weights)
    ## get the max absolute value of the weights, divide all weights by the max
    #return the copied graph

def merge_slider(graphs):
    out_graph = nx.DiGraph()

    for graph in graphs:
        out_graph.add_nodes_from(graph)
        for edge in graph.edges:
            out_graph.add_edges_from([edge])
            if constants.WEIGHT_SUM in out_graph[edge[0], edge[1]]:
                out_graph[edge[0], edge[1]][constants.WEIGHT_SUM] = graph[edge[0], edge[1]][constants.WEIGHT]
                out_graph[edge[0], edge[1]][constants.WEIGHT_INSTANCES] = 1
            else:
                out_graph[edge[0], edge[1]][constants.WEIGHT_SUM] += graph[edge[0], edge[1]][constants.WEIGHT]
                out_graph[edge[0], edge[1]][constants.WEIGHT_INSTANCES] += 1

    return out_graph

def merge_binary(graphs):
    out_graph = nx.DiGraph()

    for graph in graphs:
        out_graph.add_nodes_from(graph)
        for edge in graph.edges:
            out_graph.add_edges_from([edge])
            if constants.WEIGHT_SUM in out_graph[edge[0], edge[1]]:
                out_graph[edge[0], edge[1]][constants.BINARY_INSTANCES] = 1
            else:
                out_graph[edge[0], edge[1]][constants.BINARY_INSTANCES] += 1

    return out_graph

def merge_both(graphs):
    #ignore slider weights and merge purely by agreement? Essentially "merge binary" again.
    pass


def cycles_in_graph(graph):
    #use the cycle detector
    #return the nodes involved in the cycle
    pass

def remove_cycles(graph):
    #get the cycles
    #remove the edges involved
    #return the copied graph with the removed edges
    pass

def save_graph_to_file(graph):
    #save the graph into a file-type good for whatever graph visualization I pick
    pass

##how do I highlight cycles?

#graph sort


##TODO resolve merged graph cases of single-pair cycles - pure agreement, weighted agreement, normalized weighted agreement
##add merging for binary and slider graphs into full aggregate graphs
##add graphics functions for these graphs, add highlighting of cycles and minimal pairs