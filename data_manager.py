import csv
from datetime import datetime

FIELDNAMES = ['id', 'submission_time', 'vote_number', 'question_id', 'message,image']
LAST_ELEMENT = -1

file = 'sample_data/question.csv'



def export_data(filename='sample_data/answer.csv', data_to_write=[]):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(fieldnames=FIELDNAMES)
        writer.writerow(data_to_write)


def import_data(filename='sample_data/answer.csv'):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return [{k:v for k, v in row.items()} for row in reader]


def get_dictionary_key(id=LAST_ELEMENT, key='id'):
    all_stories = import_data()
    return 0 if all_stories == [] else all_stories[id][key]

print(import_data())

# print(get_dictionary_key('id', 0))
#
# print(import_data())





































#
#
# def convert_time_from_csv(timestamp):
#     return datetime.fromtimestamp(timestamp)
#
#
# def get_real_time():
#     now = datetime.now()
#     return datetime.timestamp(now)
#
#
# def add_view_count(question_id):
#     key = 'view_number'
#     view_count = get_dictionary_key(key, question_id)
#     view_count += 1
#     questions_data = import_data(file)
#     questions_data[question_id][key] = view_count
#     export_data(file, questions_data)
#
#
# add_view_count(1)
