import json

USER_DATA_FILEPATH = "C:\\annotation_user_data\\"
USER_META_FILEPATH = USER_DATA_FILEPATH + "meta\\"
USER_ANNOTATION_FILEPATH = USER_DATA_FILEPATH + "annotations\\"

## Make sure to check for FileExistsError when calling this
def create_user(name):
    with open(USER_DATA_FILEPATH + name + '.txt', mode='x', encoding='utf-8'):
        pass

    with open(USER_META_FILEPATH + name + '.txt', mode='x', encoding='utf-8'):
        pass

    with open(USER_ANNOTATION_FILEPATH + name + '.txt', mode='x', encoding='utf-8'):
        pass

def get_user(name):
    content_list = list()
    with open(USER_DATA_FILEPATH + name + '.txt', mode='r', encoding='utf-8') as file:
        for line in file:
            content_list.append(line.split(","))
        return content_list

def get_meta(name):
    with open(USER_META_FILEPATH + name + '.txt', mode='r', encoding='utf-8') as file:
        return json.load(file)

def get_annotations(name):
    with open(USER_ANNOTATION_FILEPATH + name + '.txt', mode='r', encoding='utf-8') as file:
        return file.readlines()

def extend_user(name, content):
    with open(USER_DATA_FILEPATH + name + '.txt', mode='a', encoding='utf-8') as file:
        for line in content:
            file.write(",".join(line) + "\n")

def add_annotation(name, content):
    with open(USER_ANNOTATION_FILEPATH + name + '.txt', mode='a', encoding='utf-8') as file:
        file.write(content + "\n")

def write_meta(name, content):
    with open(USER_META_FILEPATH + name + '.txt', mode='w', encoding='utf-8') as file:
        json.dump(content, file)