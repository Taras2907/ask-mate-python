import csv
from datetime import datetime

FIELDNAMES = ['id', 'submission_time', 'vote_number', 'question_id', 'message,image']
<<<<<<< Updated upstream
LAST_ELEMENT = -1
=======

>>>>>>> Stashed changes
def export_data(filename='sample_data/answer.csv', data_to_write=[]):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(fieldnames=FIELDNAMES)
        writer.writerow(data_to_write)


def import_data(filename='sample_data/answer.csv'):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return [{k:v for k, v in row.items()} for row in reader]
<<<<<<< Updated upstream


def get_dictionary_key(key='id', id=LAST_ELEMENT):
    all_stories = import_data()
    return 0 if all_stories == [] else all_stories[id][key]
print(get_dictionary_key('id', 0))
=======
print(import_data())






































def convert_time_from_csv(timestamp):
        return datetime.fromtimestamp(timestamp)

def get_real_time():
    now = datetime.now()
    return datetime.timestamp(now)
>>>>>>> Stashed changes
