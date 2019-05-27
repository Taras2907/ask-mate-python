import csv

FIELDNAMES = ['id', 'submission_time', 'vote_number', 'question_id', 'message,image']

def export_data(filename='sample_data/answer.csv', data_to_write):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(fieldnames=FIELDNAMES)
        writer.writerow(data_to_write)

def import_data(filename='sample_data/answer.csv'):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return [{k:v for k, v in row.items()} for row in reader]
print(import_data())