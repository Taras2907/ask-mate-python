from flask import Flask, render_template, request, redirect, url_for
from data_manager import *

app = Flask(__name__)
file_q = 'sample_data/question.csv'
file_a = 'sample_data/answer.csv'
FIELDS_Q = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
FIELDS_A = ['id', 'submission_time', 'vote_number', 'question_id', 'message,image']


@app.route('/', methods=['GET', 'POST'])
def main():
    questions_list = sort_by_item()
    up = '\u21A5'
    down = '\u21A7'
    sort_title = ['id' + up, 'id' + down, 'vote_number' + up, 'vote_number' + down,  'view_number'+ up, 'view_number' + down ]
    if request.method == "POST":
        key_sort = [item for item in sort_title if request.form['sort'] == item][0]
        if key_sort[-1] == up:
            sor = 'asc_order'
        else:
            sor= 'desc_order'
        questions_list= sort_by_item(key_sort[:-1],sor )
    return render_template("list.html", questions_list=questions_list, sort_titles = sort_title, sorto = key_sort)


@app.route('/list')
def list():
    pass




@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    change_view_count(question_id, file_q, "up")
    time = convert_time_from_csv(int(get_dictionary_key(question_id, 'submission_time')))
    answers_data =[dict for dict in import_data(file_a) if dict['question_id'] == str(question_id)]
    for dict in answers_data:
        dict['submission_time'] = str(convert_time_from_csv(int(dict['submission_time'])))

    if request.method == "POST":
        if request.form['send'] == '+':
            change_view_count(question_id, file, 'down')
            update_vote(question_id, 'up')

        else:
            change_view_count(question_id, file_q, 'down')
            update_vote(question_id, 'down')

    question_data = [question for question in import_data(file_q) if int(question["id"]) == int(question_id)][0]

    return render_template('question.html', question_data=question_data, time=time,
                           answers=answers_data, question_id=question_id)

@app.route('/question/<question_id>/edit', methods=["GET", "POST"])
def edit_question():
    pass


@app.route('/question/<int:question_id>/new-answer', methods=["GET", "POST"])
def answer_question(question_id):
    if request.method == "POST":
        time = get_real_time()
        answer_list = [question_id,
                       time,
                       "0",
                       question_id,
                       request.form["answer"],
                       ""]
        add_data(file_a, answer_list)
        return redirect(url_for('.display_question', question_id = question_id))
    return render_template('answer.html', question_id = question_id)



@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        new_id = int(get_dictionary_key(-1,'id')) + 1
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

@app.route("/question/<question_id>/delete")
def del_question(question_id):
    del_data("sample_data/question.csv", question_id, FIELDS_Q)
    return redirect("/")



if __name__ == '__main__':
    app.run()
