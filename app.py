from flask import Flask, render_template, request, redirect, url_for
from data_manager import *

app = Flask(__name__)
file_q = 'sample_data/question.csv'
file_a = 'sample_data/answer.csv'
FIELDS_Q = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
FIELDS_A = ['id', 'submission_time', 'vote_number', 'question_id', 'message','image']


@app.route('/', methods=['GET', 'POST'])
def main():
    key_sort = 0
    questions_list = get_columns('question')
    up = '\u21A5'
    down = '\u21A7'
    sort_title = ['id' + up, 'id' + down, 'vote_number' + up, 'vote_number' + down,  'view_number'+ up, 'view_number' + down ]
    if request.method == "POST":
        key_sort = [item for item in sort_title if request.form['sort'] == item][0]
        sorting_order = 'asc' if key_sort[-1] == up else 'desc'
        questions_list = sort_by_column('question', key_sort[:-1], sorting_order) # get all columns sorted by column(key_sort returns
    return render_template("list.html", questions_list=questions_list, # for exapmple id and arrow up or donw
                           sort_titles = sort_title,
                           sorto = key_sort)


@app.route('/list')
def list():
    pass


@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    change_view_count(question_id, file_q, "up")
    answers_data = get_all(question_id)
    time = get_columns_with_condition('submission_time', 'question', 'id', question_id)
    if request.method == "POST":
        change = 1 if request.form['send'] == '+' else -1
        change_view_count(question_id, file_q, 'down')
        update_vote('question', change, question_id)

    question_data = get_all_columns_with_condition('question', 'id', question_id)
    return render_template('question.html', question_data=question_data, time=time,
                           answers=answers_data, question_id=question_id)


@app.route('/question/<int:question_id>/new-answer', methods=["GET", "POST"])
def answer_question(question_id):
    if request.method == "POST":
        time = get_real_time()
        answer_list = [get_last_id('answer') + 1,   # unique key?
                       convert_time_from_csv(time),
                       "0",
                       question_id,
                       request.form["answer"],
                       ""]
        add_data('answer', FIELDS_A, answer_list)
        return redirect(url_for('.display_question', question_id = question_id))
    return render_template('answer.html', question_id = question_id)


@app.route("/search", methods=["POST", "GET"])
def search():
    data = []
    if request.method == "POST":
        search_word = request.form["search"]
        print(search_word)
        data = search_db(search_word)
    return render_template("../db-connection-example-python/templates/cwiczenia/search.html", data=data)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        new_id = get_last_id('question') + 1
        time = get_real_time()
        view = 0
        vote = 0
        image = ''
        title = request.form['title']
        message = request.form['message']
        new_question = [
            new_id,
            convert_time_from_csv(time),
            view,
            vote,
            title,
            message,
            image
        ]
        add_data('question', FIELDS_Q, new_question)
        return redirect('/')
    return render_template('ask_question.html')


@app.route("/question/<question_id>/delete")
def del_question(question_id):
    del_data(file_q, question_id, FIELDS_Q, 'id')
    del_data(file_a,question_id, FIELDS_A, 'question_id' )
    return redirect("/")


if __name__ == '__main__':
    app.run()
