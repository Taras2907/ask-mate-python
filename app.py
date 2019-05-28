from flask import Flask, render_template, request, redirect
from data_manager import *

app = Flask(__name__)
file_q = 'sample_data/question.csv'
file_a = 'sample_data/answer.csv'
FIELDS_Q = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
FIELDS_A = ['id', 'submission_time', 'vote_number', 'question_id', 'message,image']


@app.route('/')
def main():
    return render_template("list.html", questions_list=import_data(file_q))


@app.route('/list')
def list():
    pass


@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    add_view_count(question_id, file_q)
    question_data = import_data(file_q)[question_id]
    time = convert_time_from_csv(int(get_dictionary_key(question_id, 'submission_time')))
    answers_data =[(dict['message'],dict['submission_time'])for dict in import_data(file_a) if dict['question_id'] == str(question_id)]
    answers_data = [convert_time_from_csv(int(time_)) for message, time_ in answers_data ]
    return render_template('question.html', question_data=question_data, time=time, answers=answers_data)


@app.route('/question/<question_id>/new-answer')
def answer_question(question_id):
    pass


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        new_id = int(get_dictionary_key()) + 1
        time = get_real_time()
        view = 0
        vote = 0
        image = ''
        title = request.form['title']
        message = request.form['message']
        new_question = [
            new_id,
            time,
            view,
            vote,
            title,
            message,
            image
        ]
        add_data(file_q, new_question)
        return redirect('/')
    return render_template('ask_question.html')

if __name__ == '__main__':
    app.run()
