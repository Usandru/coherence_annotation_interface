SOURCE_DATA_FILEPATH = "C:\\annotation_source_data\\"

def generate_block(block_index, group):
    #Index values for each text-cluster modified by group (3 patterns)
    A = (0 + int(group)) % 3 + 4
    B = (1 + int(group)) % 3 + 4
    C = (2 + int(group)) % 3 + 4
        
    #Index values for which text in the two text pairs to use, modified by group (4 patterns)
    X = group % 2
    Y = (group // 2) % 2 + 2

