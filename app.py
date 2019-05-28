from flask import Flask, render_template
from data_manager import import_data

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run()
