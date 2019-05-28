from flask import Flask, render_template, request
from data_manager import *

app = Flask(__name__)
file = 'sample_data/question.csv'
FIELDS_Q = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
FIELDS_A = ['id', 'submission_time', 'vote_number', 'question_id', 'message,image']


@app.route('/')
def main():
    return render_template("list.html", questions_list=import_data())

@app.route('/list')
def list():
    pass

@app.route('/question/<question_id>')
def ask_question(question_id):
    pass

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
        add_data(file, new_question)
    return render_template('ask_question.html')

if __name__ == '__main__':
    app.run()
