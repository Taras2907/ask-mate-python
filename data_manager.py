import csv
from datetime import datetime
import psycopg2

LAST_ELEMENT = -1
FIELDS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
FIELDS_A = ['id', 'submission_time', 'vote_number', 'question_id', 'message','image']
file_q = 'sample_data/question.csv'
file_a = 'sample_data/answer.csv'


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


def del_data(filename, data_id, fields, header):
    input = import_data(filename)
    output = [record for record in input if record[header] != str(data_id) ]
    export_data(filename, output, fields)



def get_dictionary_key(id_, key='id'):
    all_stories = import_data(file_q)
    if id_ == -1:
        return 0 if all_stories ==[] else all_stories[::-1][0]['id']
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

    key = 'view_number'
    questions_data = import_data(file)
    for dic in questions_data:
        if dic['id'] == str(question_id):
            if change == 'up':
                dic[key] = str(int(dic[key]) + 1)
            else:
                dic[key] = str(int(dic[key]) - 1)
    export_data(file, questions_data, FIELDS)

def sort_by_item(item='id', order='desc_order'):
    lis = import_data(file_q)
    return sorted(lis, key=lambda dic: int(dic[item])) if order=='desc_order' else sorted(lis, key=lambda dic: int(dic[item]), reverse=True)


def update_vote(question_id, change):
    dicts_to_export = import_data(file_q)
    for dic in dicts_to_export:
        if dic['id'] == str(question_id):
            if change == "up":
                dic['vote_number'] = str(int(dic['vote_number']) + 1)
            else:
                dic['vote_number'] = str(int(dic['vote_number']) - 1)
    export_data(file_q, dicts_to_export, FIELDS)
    return dicts_to_export


def search_db(key):
    user_name = "dmk"
    password = "7230"
    host = "localhost"
    database_name = "localhost"

    connect_str = "postgresql://{user_name}:{password}@{host}/{database_name}".format(
        user_name=user_name,
        password=password,
        host=host,
        database_name=database_name
    )

    con = psycopg2.connect(connect_str)
    con.autocommit = True
    cur = con.cursor()

    cur.execute("SELECT id, message FROM answer WHERE message LIKE %s", [f"%{key}%"])
    rows = cur.fetchall()
    cur.execute("SELECT id, title FROM question WHERE message LIKE %s or title LIKE %s", [f"%{key}%", f"%{key}%"])
    rows2 = cur.fetchall()

    cur.close()
    con.close()
    return rows + rows2
