import random
import time
from Document_Preprocessing import utils

## THERE ARE TWO DIFFERENT TYPES OF MODE - THIS NEEDS TO BE FIXED
class Session:
    def __init__(self, id, subset, interval_a, interval_b, mode):
        self.subset_path = "C:/data/serv_data/" + subset + "/"
        self.text_source_list = list()
        self.text_id_dict = dict()
        self.pairs = list()
        self.current_pair = list()

        #Index values for each text-cluster modified by Mode (3 patterns)
        A = (0 + int(mode)) % 3 + 4
        B = (1 + int(mode)) % 3 + 4
        C = (2 + int(mode)) % 3 + 4
        
        #Index values for which text in the two text pairs to use, modified by Mode (4 patterns)
        X = mode % 2
        Y = (mode // 2) % 2 + 2

        #CSV file column ids:
        text_id = 6
        text_tag = 5
        text_content = 2

        for i in range(interval_a, interval_b):
            self.text_source_list.append(utils.get_csv(self.subset_path + str(i) + ".csv"))

        for source in self.text_source_list:
            for text in source:
                if text[text_id] in self.text_id_dict:
                    self.text_id_dict[text[text_id]][text[text_tag]] = text[text_content]
                else:
                    self.text_id_dict[text[text_id]] = {text[text_tag] : text[text_content]}

        mode_counter = 0
        #Generates the 8 internal pairs for each cluster of 5 + 2 texts, total 8 * len(source)
        for source in self.text_source_list:
            if (mode_counter + mode) % 2 == 0:
                current_mode = "slider"
            else:
                current_mode = "binary"
            mode_counter += 1

            self.pairs.extend([
                ((source[0][text_id], source[0][text_tag]), (source[1][text_id], source[1][text_tag]), current_mode),
                ((source[2][text_id], source[2][text_tag]), (source[3][text_id], source[3][text_tag]), current_mode),
                ((source[X][text_id], source[X][text_tag]), (source[Y][text_id], source[Y][text_tag]), current_mode),
                ((source[1][text_id], source[1][text_tag]), (source[A][text_id], source[A][text_tag]), current_mode),
                ((source[3][text_id], source[3][text_tag]), (source[A][text_id], source[A][text_tag]), current_mode),
                ((source[0][text_id], source[0][text_tag]), (source[C][text_id], source[C][text_tag]), current_mode),
                ((source[2][text_id], source[2][text_tag]), (source[B][text_id], source[B][text_tag]), current_mode),
                ((source[B][text_id], source[B][text_tag]), (source[C][text_id], source[C][text_tag]), current_mode)
            ])

        mode_counter = 0
        #Adds a redundant pair if there is only one source document
        for i in range(len(self.text_source_list)):
            if (mode_counter + mode) % 2 == 1:
                current_mode = "slider"
            else:
                current_mode = "binary"
            mode_counter += 1

            self.pairs.extend([
                ((self.text_source_list[i][A][text_id], self.text_source_list[i][A][text_tag]), 
                    (self.text_source_list[(i + 1) % len(self.text_source_list)][B][text_id], 
                     self.text_source_list[(i + 1) % len(self.text_source_list)][B][text_tag]),
                        current_mode),
                ((self.text_source_list[i][A][text_id], self.text_source_list[i][A][text_tag]),
                    (self.text_source_list[(i + 1) % len(self.text_source_list)][C][text_id],
                     self.text_source_list[(i + 1) % len(self.text_source_list)][C][text_tag]),
                        current_mode),
                ((self.text_source_list[i][X][text_id], self.text_source_list[i][X][text_tag]),
                    (self.text_source_list[(i + 1) % len(self.text_source_list)][Y][text_id],
                     self.text_source_list[(i + 1) % len(self.text_source_list)][Y][text_tag]),
                        current_mode)
            ])

        #print(self.pairs)
        #print(len(self.pairs))

        random.shuffle(self.pairs)

        self.pos_track = 0
        self.prev_time = time.clock()
        self.dataPath = 'C:\data\sessions\log_id' + str(id) + ".txt"
        session_log = open(self.dataPath, "w", encoding="utf-8")
        session_log.write("start_" + str(self.prev_time) + "_0\n")
        session_log.close()

    def getNextAnnotation(self):
        if self.pos_track >= len(self.pairs):
            return None
        else:
            text1_id = self.pairs[self.pos_track][0]
            text2_id = self.pairs[self.pos_track][1]
            mode = self.pairs[self.pos_track][2]
            self.current_pair = [text1_id, text2_id]
            random.shuffle(self.current_pair)
            self.pos_track = self.pos_track + 1

            return {"LeftText": self.text_id_dict[self.current_pair[0][0]][self.current_pair[0][1]].replace(" LINEBREAK", "\n"), 
                    "RightText": self.text_id_dict[self.current_pair[1][0]][self.current_pair[1][1]].replace(" LINEBREAK", "\n"),
                    "InputMethod": mode
                    }

    def writeToSessionLog(self, log_content):
        curr_time = time.clock()
        session_log = open(self.dataPath, "a", encoding="utf-8")
        session_log.write(self.current_pair[0][0] + "_" + self.current_pair[0][1] + "_" + 
                          self.current_pair[1][0] + "_" + self.current_pair[1][1] + "_" +
                            log_content + "_" + 
                            str(curr_time) + "_" + str(curr_time - self.prev_time) + "\n")
        session_log.close()
        self.prev_time = curr_time

"""     def retrieveAnnotationData(self, path):
        data_file = open(path, encoding="utf-8")
        data = data_file.read()
        data_file.close()
        return [x.strip() for x in data.split("|||")]

    def prepareAnnotationData(self, path):
        textList = self.retrieveAnnotationData(path)
        pairs = []
        for p1 in range(len(textList)):
            for p2 in range(p1+1,len(textList)):
                pairs.append([str(p1),str(p2)])
                random.shuffle(pairs[-1])
        random.shuffle(pairs)
        return (textList, pairs) """
