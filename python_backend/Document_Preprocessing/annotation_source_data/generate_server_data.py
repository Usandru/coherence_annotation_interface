import json
import csv

ORIGINALS = './originals/'
CONFIG = ORIGINALS + 'config.json'
META = './meta.json'
ID_TO_TEXT_JSON = "./id_to_text.json"

def get_csv(filename):
    csv_data = list()
    with open(filename, newline='', encoding='utf-8') as curr_file:
        curr_reader = csv.reader(curr_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in curr_reader:
            if row != []:
                csv_data.append(row)
        curr_file.close()
    return csv_data

id_tag_to_text_dict = dict()

with open(CONFIG, mode='r', encoding='utf-8') as file:
    config = json.load(file)

for i in range(config['Number_of_Texts']):
    current_text = get_csv(ORIGINALS + str(i) + '.csv')
    
    with open('./' + str(i) + '.txt', mode='w', encoding='utf-8') as file:
        for line in current_text:
            text_content = line[2]
            text_tag = line[5]
            text_id = line[6]

            text_content = text_content.replace(' LINEBREAK ', '\n')
            text_content = text_content.rstrip('\n')
            
            key = text_id + " " + text_tag

            file.write(key + "\n")
            id_tag_to_text_dict[key] = text_content

with open(ID_TO_TEXT_JSON, mode='w', encoding='utf-8') as file:
    json.dump(id_tag_to_text_dict, file)

with open(META, mode='w', encoding='utf-8') as file:
    meta_json = {"Blocks" : config['Number_of_Texts'] // 3, "Current_block" : 0, "Current_group" : 0}
    json.dump(meta_json, file)
