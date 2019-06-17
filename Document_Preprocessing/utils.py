import csv

def output_csv(filename, data):
    with open('./output/{}.csv'.format(filename), mode='w', encoding='utf-8') as curr_file:
        curr_writer = csv.writer(curr_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for t in data:
            curr_writer.writerow(t)
        curr_file.close()

def get_csv(filename):
    csv_data = list()
    with open(filename, newline='', encoding='utf-8') as curr_file:
        curr_reader = csv.reader(curr_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in curr_reader:
            if row != []:
                csv_data.append(row)
        curr_file.close()
    return csv_data
