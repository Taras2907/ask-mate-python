from flask import Flask

app = Flask(__name__)


@app.route('/')
def main():

    pass

@app.route('/list')
def list():
    pass

@app.route('/question/<question_id>')
def ask_question(question_id):
    pass

@app.route('question/<question_id>/new-answer')
def answer_question(question_id):
    pass


if __name__ == '__main__':
    app.run()
