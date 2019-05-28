import csv
from datetime import datetime
import math

FIELDNAMES = ['id', 'submission_time', 'vote_number', 'question_id', 'message,image']

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


def get_dictionary_key(id_=LAST_ELEMENT, key='id'):
    all_stories = import_data(file)
    return 0 if all_stories == [] else all_stories[id_][key]


def convert_time_from_csv(timestamp):
    return datetime.fromtimestamp(timestamp)


def get_real_time():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return round(timestamp)

def add_view_count(question_id, file):
    fields = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    key = 'view_number'
    view_count = int(get_dictionary_key(question_id, key))
    view_count += 1
    questions_data = import_data(file)
    questions_data[question_id][key] = view_count
    export_data(file, questions_data, fields)


