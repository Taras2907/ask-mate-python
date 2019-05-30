import csv
from datetime import datetime
import math


LAST_ELEMENT = -1


file = 'sample_data/question.csv'


def export_data(filename, data_to_write, fields):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data_to_write)


def import_data(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return [{k:v for k, v in row.items()} for row in reader]


def add_data(filename, new_question):
    with open(filename, 'a') as f:
        add = csv.writer(f)
        add.writerow(new_question)



def del_data(filename, data_id, fields):
    input = import_data(filename)
    output = [record for record in input if record["id"] != str(data_id)]
    export_data(filename, output, fields)


def get_dictionary_key(id_, key='id'):
    all_stories = import_data(file)
    if id_ == -1:
        dict_by_id = all_stories[::-1][0]['id']
        return dict_by_id
    else:
        dict_by_id = [dict for dict in all_stories if dict['id'] == str(id_)][0]
        return 0 if dict_by_id ==[] else dict_by_id[key]



def convert_time_from_csv(timestamp):
    return datetime.fromtimestamp(timestamp)


def get_real_time():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return round(timestamp)

def change_view_count(question_id, file, change):
    fields = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    key = 'view_number'
    questions_data = import_data(file)
    for dic in questions_data:
        if dic['id'] == str(question_id):
            if change == 'up':
                dic[key] = str(int(dic[key]) + 1)
            else:
                dic[key] = str(int(dic[key]) - 1)
    export_data(file, questions_data, fields)

def sort_by_item(item='id', order='desc_order'):
    lis = import_data(file)
    return sorted(lis, key=lambda i: i[item]) if order=='desc_order' else sorted(lis, key=lambda i: i[item], reverse=True)




