import random
import json

SOURCE_DATA_FILEPATH = "C:\\annotation_source_data\\"
SOURCE_DATA_KW_JSON = SOURCE_DATA_FILEPATH + "id_to_text.json"
SOURCE_META_FILEPATH = SOURCE_DATA_FILEPATH + "meta.txt"

def generate_block(block_index, group):
    block_list = list()
    cluster_connections = list()

    #Index values for each text-cluster modified by group (3 patterns)
    A = (0 + int(group)) % 3 + 4
    B = (1 + int(group)) % 3 + 4
    C = (2 + int(group)) % 3 + 4
        
    #Index values for which text in the two text pairs to use, modified by group (4 patterns)
    X = group % 2
    Y = (group // 2) % 2 + 2

    #Assumes that each block-file is a set of 7 ints
    for i in range(block_index * 3, block_index * 3 + 3):
        if (i + group) % 2 == 0:
            mode = "slider"
        else:
            mode = "binary"

        with open(SOURCE_DATA_FILEPATH + i + ".txt", mode="r", encoding="utf-8") as file:
            text_ids = file.readlines()

            chunk = [
                [text_ids[0], text_ids[1]],
                [text_ids[2], text_ids[3]],
                [text_ids[X], text_ids[Y]],
                [text_ids[1], text_ids[A]],
                [text_ids[2], text_ids[B]],
                [text_ids[3], text_ids[A]],
                [text_ids[0], text_ids[C]],
                [text_ids[B], text_ids[C]]
            ]

            cluster_connections.extend(
                [text_ids[A], text_ids[B], text_ids[C], text_ids[X], text_ids[Y]]
            )

            for pair in chunk:
                random.shuffle(pair)
                pair.append(mode)
            
            block_list.extend(chunk)

    #text id pairs for the connecting comparisons, hard-coded due to lacking a good structure
    chunk = [
        [cluster_connections[0], cluster_connections[11]],
        [cluster_connections[0], cluster_connections[12]],
        [cluster_connections[5], cluster_connections[1]],
        [cluster_connections[5], cluster_connections[2]],
        [cluster_connections[10], cluster_connections[6]],
        [cluster_connections[10], cluster_connections[7]],
        [cluster_connections[3], cluster_connections[14]],
        [cluster_connections[8], cluster_connections[4]],
        [cluster_connections[13], cluster_connections[9]]
    ]
        
    for i in range(len(chunk)):
        pair = chunk[i]

        if (i + group) % 2 == 0:
            mode = "slider"
        else:
            mode = "binary"

        random.shuffle(pair)
        pair.append(mode)

    block_list.extend(chunk)

    random.shuffle(block_list)

    return block_list


def id_block_to_text_block(block):
    #add a way of accessing the general kw-JSON for ids to texts
    with open(SOURCE_DATA_KW_JSON, mode="r", encoding="utf-8") as file:
        kw_json = json.load(file)

        new_block = list()
        mode_list = list()

        for line in block:
            new_line = list()
            for item in line[:-1]:
                new_line.append(kw_json[item])
            mode_list.append(line[-1])
            new_block.append(new_line)

        return new_block, mode_list

def get_meta():
    with open(SOURCE_META_FILEPATH, mode="r", encoding="utf-8") as file:
        return json.load(file)

def update_meta(meta):
    with open(SOURCE_META_FILEPATH, mode="r", encoding="utf-8") as file:
        return json.dump(meta, file)