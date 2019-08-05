import json

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

        self.number_of_annotations = -1
        self.is_partial = True
        self.number_of_rights = -1
        self.number_of_lefts = -1
        self.slider_zeros = -1


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

        right_count = len([item for item in self.content if item[1] == "right"])
        positive_count = len([item for item in self.content if item[1] == "right"])
        self.number_of_lefts = len([item for item in self.annotations if item[1] == "left"])
        
        self.number_of_rights
        
        self.slider_zeros = len([item for item in self.annotations if item[1] == "0"])



    
