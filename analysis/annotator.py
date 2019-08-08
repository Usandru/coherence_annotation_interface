import json
import constants
import networkx as nx
import statsmodels.stats as sm_st
from statsmodels.stats.proportion import binom_test
import matplotlib.pyplot as plt

class annotator:
    def __init__(self):
        self.id = ""
        
        self.offset = -1
        self.blocks = -1
        self.group = -1

        self.tasks = list()
        self.annotations = list()

        self.mode = list()
        self.content = list()
        self.time = list()

        self.right_id = list()
        self.left_id = list()

        self.coherence_direction = list()

        self.number_of_annotations = -1
        self.is_partial = True
        self.number_of_rights = 0
        self.number_of_lefts = 0
        self.slider_zeros = 0

        self.graph = nx.DiGraph()
        self.null_graph = nx.Graph()


    def from_raw(self, id, task_filepath, meta_filepath, annotation_filepath):
        self.id = id

        with open(task_filepath, mode="r", encoding="utf-8") as file:
            self.tasks = [item.split(",") for item in file.readlines()]

        with open(meta_filepath, mode="r", encoding="utf-8") as file:
            meta = json.load(file)
            self.offset = meta["Offset"]
            self.blocks = meta["Blocks"]
            self.group = meta["Group"]

        with open(annotation_filepath, mode="r", encoding="utf-8") as file:
            strip_comments = [item.split("///")[0] for item in file.readlines()]
            self.annotations = [item.split("_") for item in strip_comments]

        self.number_of_annotations = len(self.annotations)
        
        for i in range(self.number_of_annotations):
            self.mode.append(self.annotations[i][0])
            self.content.append(self.annotations[i][1])
            self.time.append(self.annotations[i][2])

        if self.number_of_annotations % 33 > 0:
            self.is_partial = True
        else:
            self.is_partial = False
        
        for i in range(len(self.tasks)):
            self.left_id.append(self.tasks[i][0])
            self.right_id.append(self.tasks[i][1])

        for i in range(self.number_of_annotations):
            if self.mode[i] == constants.BINARY:
                if self.content[i] == constants.LEFT:
                    self.number_of_lefts += 1
                    self.coherence_direction.append(constants.LEFT)
                else:
                    self.number_of_rights += 1
                    self.coherence_direction.append(constants.RIGHT)
                
            elif self.mode[i] == constants.SLIDER:
                if float(self.content[i]) < 0:
                    self.number_of_lefts += 1
                    self.coherence_direction.append(constants.LEFT)
                elif float(self.content[i]) > 0:
                    self.number_of_rights += 1
                    self.coherence_direction.append(constants.RIGHT)
                else:
                    self.slider_zeros += 1
                    self.coherence_direction.append(constants.NULL)

        self.build_graph()

    def run_statistics(self):
        print(binom_test(self.number_of_lefts, self.number_of_annotations - self.slider_zeros))

    def build_graph(self):
        self.graph.add_nodes_from(self.right_id)
        self.graph.add_nodes_from(self.left_id)

        
        for i in range(self.number_of_annotations):
            if self.coherence_direction[i] == constants.RIGHT:
                self.graph.add_edge(self.right_id[i], self.left_id[i]) # "mode"=self.mode[i], "id"=self.id
            elif self.coherence_direction[i] == constants.LEFT:
                self.graph.add_edge(self.left_id[i], self.right_id[i])
            elif self.coherence_direction[i] == constants.NULL:
                self.null_graph.add_node(self.left_id[i])
                self.null_graph.add_node(self.right_id[i])
                self.null_graph.add_edge(self.left_id[i], self.right_id[i])

        remove_list = list()
        for node in self.graph.nodes:
            if self.graph.degree(node) == 0:
                remove_list.append(node)
        
        for node in remove_list:
            self.graph.remove_node(node)

    def draw_graph(self):
        plt.subplot(111)
        nx.draw(self.graph, pos=nx.circular_layout(self.graph))
        plt.savefig(constants.OUTPUT + str(self.id) + ".png")
        plt.clf()
