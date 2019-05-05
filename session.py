import random
import time

class Session:
    def __init__(self, id, path, mode):
        full_path = "./serv_data/" + path
        self.textList, self.pairs = self.prepareAnnotationData(full_path)
        if mode == "binary":
            self.mode = ["binary" for x in range(len(self.pairs))]
        elif mode == "slider":
            self.mode = ["slider" for x in range(len(self.pairs))]
        elif mode == "scale":
            self.mode = ["scale" for x in range(len(self.pairs))]
        elif mode == "split":
            self.mode = ["binary" if x % 2 == 0 else "slider" for x in range(len(self.pairs))]
            random.shuffle(self.mode)
        elif mode == "short":
            self.mode = ["binary" if x % 2 == 0 else "slider" for x in range(10)]
            random.shuffle(self.mode)
        self.pos_track = 0
        self.prev_time = time.clock()
        self.dataPath = '.\sessions\log_' + path[:-4] + "_id" + str(id) + ".txt"
        session_log = open(self.dataPath, "w", encoding="utf-8")
        session_log.write("start_" + str(self.prev_time) + "_0\n")
        session_log.close()

    def retrieveAnnotationData(self, path):
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
        return (textList, pairs)

    def getNextAnnotation(self):
        if self.pos_track >= len(self.mode):
            return None
        else:
            next_pair = self.pairs[self.pos_track]
            next_mode = self.mode[self.pos_track]
            self.pos_track = self.pos_track + 1
            return {"LeftText": self.textList[int(next_pair[0])], "RightText": self.textList[int(next_pair[1])], "InputMethod": next_mode}

    def writeToSessionLog(self, log_content):
        curr_time = time.clock()
        session_log = open(self.dataPath, "a", encoding="utf-8")
        session_log.write("_".join(self.pairs[self.pos_track - 1]) + "_" + 
                            log_content + "_" + 
                            str(curr_time) + "_" + str(curr_time - self.prev_time) + "\n")
        session_log.close()
        self.prev_time = curr_time