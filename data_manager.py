import csv
from datetime import datetime
import database_common
from psycopg2 import sql
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



def del_data(filename, data_id, fields, header):
    input = import_data(filename)
    output = [record for record in input if record[header] != str(data_id) ]
    export_data(filename, output, fields)





def convert_time_from_csv(timestamp):
    return datetime.fromtimestamp(timestamp)


def get_real_time():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return round(timestamp)

def change_view_count(question_id, file, change):

    key = 'view_number'
    questions_data = import_data(file)
    for question in questions_data:
        if question['id'] == str(question_id):
            if change == 'up':
                question['view_number'] = str(int(question['view_number']) + 1)
            else:
                question['view_number'] = str(int(question['view_number']) - 1)
    export_data(file, questions_data, FIELDS)

def sort_by_item(item='id', order='desc_order'):
    lis = import_data(file_q)
    return sorted(lis, key=lambda dic: int(dic[item])) if order=='desc_order' else sorted(lis, key=lambda dic: int(dic[item]), reverse=True)







@database_common.connection_handler
def get_columns(cursor, table):
    sql_all_quuery = sql.SQL("select * from {} ").format(
        sql.Identifier(table)
    )
    cursor.execute(sql_all_quuery)
    all_columns = cursor.fetchall()
    return all_columns


@database_common.connection_handler
def get_columns_with_condition(cursor,column, table, condition_column, condition_value):
    sql_all_quuery = sql.SQL("select {} from {}  where {} = %s").format(
        sql.Identifier(column),
        sql.Identifier(table),
        sql.Identifier(condition_column)
    )
    cursor.execute(sql_all_quuery, [condition_value])
    all_columns = cursor.fetchall()
    return [] if all_columns ==[] else all_columns[0] # return a list with one dict


@database_common.connection_handler
def update_vote(cursor, table, change, condition):
    current_vote = get_columns_with_condition('vote_number', 'question', 'id', condition)['vote_number'] + change
    sql_query_to_update = sql.SQL("update {} set {} =%s where {} =%s").format(
        sql.Identifier(table),
        sql.Identifier('vote_number'),
        sql.Identifier('id'),

    )
    cursor.execute(sql_query_to_update, [current_vote, condition])


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



@database_common.connection_handler
def get_all_columns_with_condition(cursor, table, condition_column, condition_value):
    sql_all_quuery = sql.SQL("select * from {}  where {} = %s").format(
        sql.Identifier(table),
        sql.Identifier(condition_column)
    )
    cursor.execute(sql_all_quuery, [condition_value])
    all_columns = cursor.fetchall()
    return [] if all_columns ==[] else all_columns[0] # return a list with one dict



@database_common.connection_handler
def get_all(cursor,id_):
    cursor.execute("select * from answer where question_id = %s", [id_])
    all_columns = cursor.fetchall()
    return all_columns

@database_common.connection_handler
def get_last_id(cursor, table):
    sql_all_quuery = sql.SQL("select MAX({}) from {}").format(
        sql.Identifier('id'),
        sql.Identifier(table)
    )
    cursor.execute(sql_all_quuery)
    all_columns = cursor.fetchall()
    return all_columns[0]['max'] # return a list with one dict{max:value}


@database_common.connection_handler
def add_data(cursor, table, column_headers, list_of_values):
    sql_insert_query = sql.SQL("insert into {} ({}) values ({})").format(
        sql.Identifier(table),
        sql.SQL(', ').join(map(sql.Identifier, column_headers)),
        sql.SQL(', ').join(sql.Placeholder() * len(column_headers))
    )
    cursor.execute(sql_insert_query, list_of_values)


@database_common.connection_handler
def sort_by_column(cursor, table, column,desc_or_asc_order):
    if desc_or_asc_order == 'desc':
        sql_sort_query = sql.SQL("select * from {} order by {} DESC").format(
        sql.Identifier(table),
        sql.Identifier(column)
        )
    else:
        sql_sort_query = sql.SQL("select * from {} order by {} ASC").format(
            sql.Identifier(table),
            sql.Identifier(column)
        )
    cursor.execute(sql_sort_query)
    sorte_coll = cursor.fetchall()
    return  sorte_coll