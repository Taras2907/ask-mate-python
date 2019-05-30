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
    sort_title = ['id', 'vote number', 'time', 'viev number' ]
    if request.method == "POST":
        questions_list =sort_by_item(request.form['key_to_sort'], 'asc_order')
    return render_template("list.html", questions_list=questions_list, sort_titles = sort_title)


@app.route('/list')
def list():
    pass




@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    change_view_count(question_id, file_q, "up")
    question_data = [question for question in import_data(file_q) if int(question["id"]) == int(question_id)][0]

    time = convert_time_from_csv(int(get_dictionary_key(question_id, 'submission_time')))
    answers_data =[dict for dict in import_data(file_a) if dict['question_id'] == str(question_id)]
    for dict in answers_data:
        dict['submission_time'] = str(convert_time_from_csv(int(dict['submission_time'])))

    if request.method == "POST":
        if request.form['send'] == '+':
            change_view_count(question_id, file_q, 'down')
            data_to_export = import_data(file_q)
            data_to_export[question_id]['vote_number'] = int(data_to_export[question_id]['vote_number']) + 1
            export_data(file_q, data_to_export, FIELDS_Q)
            question_data = [dic for dic in import_data(file_q) if dict['id'] == question_id]
        else:
            change_view_count(question_id, file_q, 'down')
            data_to_export = import_data(file_q)
            data_to_export[question_id]['vote_number'] = int(data_to_export[question_id]['vote_number']) - 1
            export_data(file_q, data_to_export, FIELDS_Q)
            question_data = [dic for dic in import_data(file_q) if dict['id'] == question_id]
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
