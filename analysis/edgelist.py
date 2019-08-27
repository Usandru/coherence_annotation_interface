import constants
import sourcetexts
import utilities
import copy

COMPONENT_LEFT = 0
COMPONENT_RIGHT = 1
COMPONENT_DIRECTION = 2
COMPONENT_CONTENT = 3
COMPONENT_MODE = 4

def raw_to_edge(left_node, right_node, direction, content, mode, time, origin_id):
    first_node_direction = utilities.compare_ids(left_node, right_node)
    
    if first_node_direction == constants.RIGHT:
        edge_direction = utilities.reverse_direction(direction)
        first_node = right_node
        second_node = left_node
    else:
        edge_direction = direction
        first_node = left_node
        second_node = right_node
    
    return make_edge(first_node, second_node, **{constants.AGREEMENT_COMPONENTS : [(left_node, right_node, direction, content, mode, time, origin_id)], 
                                                 constants.AGREEMENT : 1.0,
                                                 constants.DIRECTION : edge_direction,
                                                 constants.EDGELIST_MODE : mode})

#probably obsolete
def make_edge(left_node, right_node, **kwargs):
    return (left_node, right_node, kwargs)

def merge_check_if_same_origin(first_source_id, second_source_id):
    if second_source_id.split("_")[0] in first_source_id:
        return True
    else:
        return False

def compute_agreement_and_direction(left_node, right_node, list_of_agreement_components):
    tally = dict({left_node : 0, right_node : 0})
    for component in list_of_agreement_components:
        if component[COMPONENT_DIRECTION] == constants.LEFT:
            tally[component[COMPONENT_LEFT]] += 1
        elif component[COMPONENT_DIRECTION] == constants.RIGHT:
            tally[component[COMPONENT_RIGHT]] += 1

    if tally[left_node] > tally[right_node]:
        return_direction = constants.LEFT
    elif tally[left_node] > tally[right_node]:
        return_direction = constants.RIGHT
    else:
        return_direction = constants.NULL
    
    return max(tally.values()) / sum(tally.values()), return_direction

def compute_slider_weight_and_direction(left_node, right_node, list_of_agreement_components):
    tally = dict({left_node : 0, right_node : 0})
    slider_components = [component for component in list_of_agreement_components if component[COMPONENT_MODE] == constants.SLIDER]
    for component in slider_components:
        if component[COMPONENT_DIRECTION] == constants.LEFT:
            tally[component[COMPONENT_LEFT]] += abs(component[COMPONENT_CONTENT])
        elif component[COMPONENT_DIRECTION] == constants.RIGHT:
            tally[component[COMPONENT_RIGHT]] += abs(component[COMPONENT_CONTENT])

    if len(slider_components) > 0:
        average_weight = (tally[right_node] - tally[left_node]) / len(slider_components)
        if average_weight < 0:
            return average_weight, constants.LEFT
        elif average_weight > 0:
            return average_weight, constants.RIGHT
        else:
            return average_weight, constants.NULL
    else:
        return None, constants.NULL



class EdgeList:
    def __init__(self, edge_list, source_id, sourcetext_object):
        self.edge_list = edge_list
        self.source_id = source_id
        self.sourcetext_object = sourcetext_object

    def copy_by_mode(self, mode):
        new_edge_list = [edge for edge in self.edge_list if edge[constants.EDGE_KEYVALUE][constants.EDGELIST_MODE] == mode]
        new_source_id = self.source_id + "_modefilteron:" + mode
        return EdgeList(new_edge_list, new_source_id, self.sourcetext_object)

    def filter_to_minimal_pairs(self):
        new_edge_list = [edge for edge in self.edge_list if utilities.same_num_id(edge[constants.EDGE_LEFT], edge[constants.EDGE_RIGHT])]
        new_source_id = self.source_id + "_minimalpaironly"
        return EdgeList(new_edge_list, new_source_id, self.sourcetext_object)

##this is a terribly cluttered function which should probably be simplified - the goal is replacing "NUMBERS PRONOUN_O_NP" style tags with "NUMBERS ORIGINAL" tags
    def cast_tags_to_original(self):
        new_edge_list = [edge for edge in self.edge_list if utilities.tag_is_original(edge[constants.EDGE_LEFT]) and utilities.tag_is_original(edge[constants.EDGE_RIGHT])]
        edges_to_cast = [edge for edge in self.edge_list if not utilities.tag_is_original(edge[constants.EDGE_LEFT]) or not utilities.tag_is_original(edge[constants.EDGE_RIGHT])]

        edges_to_append = list()
        for edge in edges_to_cast:
            l_num, l_tag = edge[constants.EDGE_LEFT].split()
            r_num, r_tag = edge[constants.EDGE_RIGHT].split()
            edges_to_append.append(make_edge(" ".join([l_num, constants.TAG_ORIGINAL]), " ".join([r_num, constants.TAG_ORIGINAL]), **edge[constants.EDGE_KEYVALUE]))

        new_source_id = self.source_id + "_casttooriginal"
        return EdgeList(new_edge_list.extend(edges_to_append), new_source_id, self.sourcetext_object)

    def merge_edgelists(self, other_edgelist):
        new_edge_list = list()
        new_source_id = self.source_id + "_MERGED_" + other_edgelist.source_id

        for edge in self.edge_list:
            node_l = edge[constants.EDGE_LEFT]
            node_r = edge[constants.EDGE_RIGHT]
            for other_edge in other_edgelist:
                #if the nodes are the same...
                if node_l == other_edge[constants.EDGE_LEFT]:
                    if node_r == other_edge[constants.EDGE_RIGHT]:
                        
                        base_dict = copy.deepcopy(edge[constants.EDGE_KEYVALUE])
                        extend_dict = other_edge[constants.EDGE_KEYVALUE]

                        base_dict[constants.AGREEMENT_COMPONENTS].extend(extend_dict[constants.AGREEMENT_COMPONENTS])

                        merged_agreement, merged_direction = compute_agreement_and_direction(node_l, node_r, base_dict[constants.AGREEMENT_COMPONENTS])
                        base_dict[constants.AGREEMENT] = merged_agreement
                        base_dict[constants.DIRECTION] = merged_direction
                        base_dict[constants.EDGELIST_MODE] = constants.MERGED

                        slider_weight, slider_direction = compute_slider_weight_and_direction(node_l, node_r, base_dict[constants.AGREEMENT_COMPONENTS])

                        base_dict[constants.SLIDER_WEIGHT] = slider_weight
                        base_dict[constants.SLIDER_DIRECTION] = slider_direction

                        new_edge_list.append(make_edge(node_l, node_r, **base_dict))
                        break

        return EdgeList(new_edge_list, new_source_id, self.sourcetext_object)

