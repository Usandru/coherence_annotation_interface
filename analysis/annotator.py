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

        self.minimal_pairs = list()

        self.number_of_annotations = -1
        self.is_partial = True
        self.number_of_rights = 0
        self.number_of_lefts = 0
        self.slider_zeros = 0

        self.graphs = list()
        self.null_graph = nx.Graph()

        for _ in range(constants.NUM_OF_BLOCKS):
            self.graphs.append(nx.DiGraph())
        


    def from_raw(self, id, task_filepath, meta_filepath, annotation_filepath):
        self.id = id

        # Retrieve all the raw data from the file paths and assign it to the general containers
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

        # Establish the core values for later processing
        self.number_of_annotations = len(self.annotations)
        
        for i in range(self.number_of_annotations):
            self.mode.append(self.annotations[i][0])
            self.content.append(self.annotations[i][1])
            self.time.append(self.annotations[i][2])

        # Determine if the set is partial or complete
        if self.number_of_annotations % 33 > 0:
            self.is_partial = True
        else:
            self.is_partial = False
        
        # Generate lists of comparison ids by their left-right position for later use
        for i in range(len(self.tasks)):
            self.left_id.append(self.tasks[i][0])
            self.right_id.append(self.tasks[i][1])

        # Determine the unweighted coherence direction (or if there is a null, for slider annotations)
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

        # Gather up the minimal pairs into tuples, storing them by numerical id, tag on the left,
        # tag on the right, and direction of the coherence arrow
        for i in range(self.number_of_annotations):
            left_num, left_tag = self.left_id[i].split()
            right_num, right_tag = self.right_id[i].split()

            if left_num == right_num:
                self.minimal_pairs.append((left_num, left_tag, right_tag, self.coherence_direction[i]))

        # Construct the graph here - this is likely a temporary placement of this function call
        self.build_graph()

    def run_statistics(self):
        # Generate binomial values for areas of interest - does the position of the text determine
        # the coherence relationship? Discard nulls as noise
        print(binom_test(self.number_of_lefts, self.number_of_annotations - self.slider_zeros))

    def build_graph(self):
        for i in range(self.blocks):
            current_graph = self.graphs[(i + self.offset) % constants.NUM_OF_BLOCKS]
            current_graph.add_nodes_from(self.right_id[(i * constants.BLOCK_SIZE):((i+1) * constants.BLOCK_SIZE)])
            current_graph.add_nodes_from(self.left_id[(i * constants.BLOCK_SIZE):((i+1) * constants.BLOCK_SIZE)])
            for j in range(i * constants.BLOCK_SIZE, (i+1) * constants.BLOCK_SIZE):
                if self.coherence_direction[i] == constants.RIGHT:
                    current_graph.add_edge(self.right_id[j], self.left_id[j]) # "mode"=self.mode[i], "id"=self.id
                elif self.coherence_direction[i] == constants.LEFT:
                    current_graph.add_edge(self.left_id[j], self.right_id[j])
                elif self.coherence_direction[i] == constants.NULL:
                    self.null_graph.add_node(self.left_id[j])
                    self.null_graph.add_node(self.right_id[j])
                    self.null_graph.add_edge(self.left_id[j], self.right_id[j])

    def draw_graph(self, ident):
        plt.subplot(111)
        nx.draw(self.graphs[ident], pos=nx.circular_layout(self.graphs[ident]))
        plt.savefig(constants.OUTPUT + str(self.id) + "_" + str(ident) + ".png")
        plt.clf()

    def draw_all(self):
        for i in range(self.blocks):
            self.draw_graph((i + self.offset) % constants.NUM_OF_BLOCKS)

## TODO implement handling for slider vs. binary mode, including graphs of only slider edges or only binary edges
## fix up the graphics of the graph displays
## implement time analysis functions