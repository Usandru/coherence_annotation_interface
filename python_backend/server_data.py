from flask import jsonify
import user_io
import task_generator

def fetch_user(name):
    user_content = user_io.get_user(name)
    user_annotations = user_io.get_annotations(name)
    total_length = len(user_content)
    position = len(user_annotations)
    if total_length <= position:
        pass # SOME ERROR
    else:
        user_texts, mode_list = task_generator.id_block_to_text_block(user_content)
        return jsonify({"Content" : user_texts, "Mode" : mode_list, "Position" : position, "Length" : total_length})

## THIS IS BUGGED IF THE NUMBER OF AVAILABLE BLOCKS IS INCREASED FOR ANY USERS WITHOUT OFFSET 0!
def extend_user(name):
    user_meta = user_io.get_meta(name)
    task_meta = task_generator.get_meta()
    if user_meta["Blocks"] >= task_meta["Blocks"]:
        pass # SOME ERROR
    else:
        new_block = task_generator.generate_block((user_meta["Offset"] + user_meta["Blocks"]) % task_meta["Blocks"], user_meta["Group"])
        user_io.extend_user(name, new_block)
        user_meta["Blocks"] = user_meta["Blocks"] + 1
        user_io.write_meta(name, user_meta)

# def extend_user_with_params(name, group, offset, blocks):
#     pass

def generate_user(name, group, offset, blocks):
    try:
        user_io.create_user(name)
    except FileExistsError:
        return # PASS MESSAGE BACK TO CLIENT
    
    user_content = list()
    for i in range(offset, offset + blocks):
        user_content.extend(task_generator.generate_block(i, group))

    user_io.extend_user(name, user_content)
    user_io.write_meta(name, {"Blocks" : blocks, "Group" : group, "Offset" : offset})


def generate_user_default(name):
    try:
        user_io.create_user(name)
    except FileExistsError:
        return # PASS MESSAGE BACK TO CLIENT
    
    task_meta = task_generator.get_meta()
    user_content = task_generator.generate_block(task_meta["Current_block"], task_meta["Current_group"])
    user_io.extend_user(name, user_content)

    #Loops through every block and switches group after every full loop
    user_io.write_meta(name, {"Blocks" : 1, "Group" : task_meta["Current_group"], "Offset" : task_meta["Current_block"]})
    task_meta["Current_block"] = (task_meta["Current_block"] + 1) % task_meta["Blocks"]
    if task_meta["Current_block"] == 0:
        task_meta["Current_group"] = (task_meta["Current_group"] + 1) % 2
    task_generator.update_meta(task_meta)


def annotate(name, content, position):
    if position >= len(user_io.get_annotations(name)):
        user_io.add_annotation(name, content)