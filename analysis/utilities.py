import constants
import annotator
#import networkx as nx
#import statsmodels.stats as sm_st
#from statsmodels.stats.proportion import binom_test
#import matplotlib.pyplot as plt

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