from datetime import datetime

from psycopg2 import sql
import bcrypt
import database_common

LAST_ELEMENT = -1
FIELDS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
FIELDS_A = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
file_q = 'sample_data/question.csv'
file_a = 'sample_data/answer.csv'


def convert_time_from_csv(timestamp):
    return datetime.fromtimestamp(timestamp)


def get_real_time():
    now = datetime.now()
    return now.replace(microsecond=0)


@database_common.connection_handler
def change_view_count(cursor, question_id, change):
    cursor.execute('''
                    SELECT view_number FROM question
                    WHERE id = %(question_id)s
                    ''',
                   {'question_id': question_id})
    views = cursor.fetchall()
    temp = views[0]['view_number']
    if change == 'up':
        temp += 1
    else:
        temp -= 1
    cursor.execute('''
                    UPDATE question SET view_number = %(temp)s
                    WHERE id = %(question_id)s
                    ''',
                   {'temp': temp,
                    'question_id': question_id})


@database_common.connection_handler
def get_columns(cursor, table):
    sql_all_quuery = sql.SQL("SELECT * FROM {} ").format(
        sql.Identifier(table)
    )
    cursor.execute(sql_all_quuery)
    all_columns = cursor.fetchall()
    return all_columns


@database_common.connection_handler
def get_columns_with_condition(cursor, column, table, condition_column, condition_value):
    sql_all_quuery = sql.SQL("SELECT {} FROM {}  WHERE {} = %s").format(
        sql.Identifier(column),
        sql.Identifier(table),
        sql.Identifier(condition_column)
    )
    cursor.execute(sql_all_quuery, [condition_value])
    all_columns = cursor.fetchall()

    result = [] if all_columns == [] else all_columns[0][column]
    return result


@database_common.connection_handler
def update_vote(cursor, table, change, condition):
    current_vote = get_columns_with_condition('vote_number', table, 'id', condition) + change
    sql_query_to_update = sql.SQL("UPDATE {} SET {} =%s WHERE {} =%s").format(
        sql.Identifier(table),
        sql.Identifier('vote_number'),
        sql.Identifier('id'),

    )
    cursor.execute(sql_query_to_update, [current_vote, condition])


@database_common.connection_handler
def del_data(cursor, table, condition_column, data_id):
    sql_query_to_delete = sql.SQL("DELETE FROM {}  WHERE {} = %s;").format(
        sql.Identifier(table),
        sql.Identifier(condition_column))
    cursor.execute(sql_query_to_delete, [data_id])


@database_common.connection_handler
def search_db(cursor, key):
    key = "%" + key.lower() + "%"
    search1 = sql.SQL('SELECT * FROM answer WHERE LOWER(message) LIKE %s')
    cursor.execute(search1, [key])
    rows = cursor.fetchall()
    search2 = sql.SQL('SELECT * FROM question WHERE LOWER(message) LIKE %s or LOWER(title) LIKE %s')
    cursor.execute(search2, [key, key])
    rows2 = cursor.fetchall()

    return rows + rows2


@database_common.connection_handler
def get_all_columns_with_condition(cursor, table, condition_column, condition_value):
    sql_all_quuery = sql.SQL("SELECT * FROM {}  WHERE {} = %s").format(
        sql.Identifier(table),
        sql.Identifier(condition_column)
    )

    cursor.execute(sql_all_quuery, [condition_value])
    all_columns = cursor.fetchall()
    return [] if all_columns == [] else all_columns  # return a list with one dict


@database_common.connection_handler
def get_all(cursor, id_):
    cursor.execute("SELECT * FROM answer WHERE question_id = %s", [id_])
    all_columns = cursor.fetchall()
    return all_columns


@database_common.connection_handler
def get_last_id(cursor, table):
    sql_all_quuery = sql.SQL("SELECT MAX({}) FROM {}").format(
        sql.Identifier('id'),
        sql.Identifier(table)
    )
    cursor.execute(sql_all_quuery)
    all_columns = cursor.fetchall()
    return 0 if all_columns[0]['max'] is None else all_columns[0]['max']  # returns values


@database_common.connection_handler
def add_data(cursor, table, column_headers, list_of_values):
    sql_insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table),
        sql.SQL(', ').join(map(sql.Identifier, column_headers)),
        sql.SQL(', ').join(sql.Placeholder() * len(column_headers))
    )
    cursor.execute(sql_insert_query, list_of_values)


@database_common.connection_handler
def sort_by_column(cursor, table, column, desc_or_asc_order):
    if desc_or_asc_order == 'desc':
        sql_sort_query = sql.SQL("SELECT * FROM {} ORDER BY {} DESC").format(
            sql.Identifier(table),
            sql.Identifier(column)
        )
    else:
        sql_sort_query = sql.SQL("SELECT * FROM {} ORDER BY {} ASC").format(
            sql.Identifier(table),
            sql.Identifier(column)
        )
    cursor.execute(sql_sort_query)
    sorte_coll = cursor.fetchall()
    return sorte_coll


@database_common.connection_handler
def edit_comments(cursor, message, condition):
    sql_update_title = sql.SQL("update comment set "
                               "submission_time = %s,"
                               "message = %s, "
                               "edited_count = %s"
                               " where id =%s").format(
    )
    edited_count = get_columns_with_condition('edited_count', 'comment', 'id', condition)
    edited_count = 1 if edited_count == None else edited_count + 1
    time = get_real_time()
    cursor.execute(sql_update_title, [time, message, edited_count, condition])


@database_common.connection_handler
def edit_answer(cursor, updated_message, condition):
    sql_update_query = sql.SQL("UPDATE answer SET submission_time = %s,message = %s WHERE id = %s").format(
    )
    time = get_real_time()
    cursor.execute(sql_update_query, [time, updated_message, condition])


def add_tags(tags_list, question_id):
    headers = ['question_id', 'tag_id']
    for tag in tags_list:
        values = [question_id, tag]
        add_data('question_tag', headers, values)


@database_common.connection_handler
def delete_tag(cursor, question_id, tag_id):
    cursor.execute('''
                    DELETE FROM question_tag 
                    WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s
                    ''',
                   {'question_id': question_id,
                    'tag_id': tag_id})


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@database_common.connection_handler
def get_reputation_db(cursor, username):
    cursor.execute('''
                       SELECT reputation FROM users
                       WHERE username = %s;
                      ''', [username])
    return cursor.fetchall()


@database_common.connection_handler
def update_reputation(cursor, number_of_points, user):
    "Number of points is an integer positive or negative which you want to add or subtract from current users reputation)"
    current_points = get_reputation_db(user)
    points = current_points[0]['reputation'] + number_of_points
    cursor.execute('''
                    UPDATE users
                    SET reputation = %s
                    WHERE username = %s;
                   ''', [points, user])


@database_common.connection_handler
def get_all_user_logins(cursor):
    sql_select = sql.SQL("SELECT username FROM users")
    cursor.execute(sql_select)
    all_logins = cursor.fetchall()
    return all_logins

@database_common.connection_handler
def update_accept(cursor, answer_id):
    cursor.execute('''
                    SELECT accept FROM answer
                    WHERE id=%(answer_id)s
                    ''',
                   {'answer_id': answer_id})
    accept_state = cursor.fetchall()
    if not accept_state[0]['accept']:
        cursor.execute('''
                        UPDATE answer SET accept = TRUE WHERE id=%(answer_id)s
                        ''',
                       {'answer_id': answer_id})
        cursor.execute('''
                        SELECT username FROM answer
                        WHERE id=%(answer_id)s
                        ''',
                       {'answer_id': answer_id})
        user_data = cursor.fetchall()
        if user_data[0]['username']:
            user = user_data[0]['username']
            update_reputation(15, user)


@database_common.connection_handler
def get_users_name_reputation(cursor):
    sql_select = sql.SQL("SELECT username, reputation FROM users")
    cursor.execute(sql_select)
    users_name_reputation = cursor.fetchall()
    return users_name_reputation


@database_common.connection_handler
def count_tags(cursor):
    cursor.execute("""
                    SELECT name, tag.id, COUNT(tag_id) 
                    FROM tag JOIN question_tag qt on tag.id = qt.tag_id
                    GROUP BY name, id
                    ORDER BY id
                    """)
    tags = cursor.fetchall()
    return tags


@database_common.connection_handler
def get_question_with_tag(cursor, tag_id):
    cursor.execute("""
                    SELECT question.title, tag.name, question.id
                    FROM question JOIN question_tag qt on question.id = qt.question_id 
                    JOIN tag on qt.tag_id = tag.id
                    WHERE question.id = qt.question_id AND tag_id = %(tag_id)s
                    """,
                   {'tag_id': tag_id})
    questions = cursor.fetchall()
    return questions
