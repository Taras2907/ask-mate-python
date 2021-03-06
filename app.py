from flask import Flask, render_template, request, redirect, url_for, session

from data_manager import *

app = Flask(__name__)
file_q = 'sample_data/question.csv'
file_a = 'sample_data/answer.csv'
FIELDS_Q = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image', 'username']
FIELDS_A = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image', 'username']
FIELDS_C_Q = ['id', 'question_id', 'message', 'submission_time', 'username']
FIELDS_C_A = ['id', 'answer_id', 'message', 'submission_time', 'username']
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/register', methods=['GET', 'POST'])
def register():
    all_user_names = [each['username'] for each in get_all_user_logins()]
    if request.method == 'POST':
        if request.form['username'] in all_user_names:
            user_exists = 'User name already exists'
            return render_template('register.html', user_exists=user_exists)
        else:
            users_data = [hash_password(request.form[item]) if item == 'password' else request.form[item] for item in ['username', 'password']]
            add_data('users',['username', 'password'], users_data)
            return redirect(url_for('login'))
    return render_template('register.html', all_users_names=all_user_names)


@app.route('/', methods=['GET', 'POST'])
def main():
    key_sort = 0
    questions_list = get_columns('question')
    up = '\u21A5'
    down = '\u21A7'
    sort_title = ['id' + up, 'id' + down, 'vote_number' + up, 'vote_number' + down, 'view_number' + up,
                  'view_number' + down]
    tags_names = get_columns('tag')
    tags_questions = get_columns('question_tag')
    if request.method == "POST":
        key_sort = [item for item in sort_title if request.form['sort'] == item][0]
        sorting_order = 'asc' if key_sort[-1] == up else 'desc'
        questions_list = sort_by_column('question', key_sort[:-1],
                                        sorting_order)  # get all columns sorted by column(key_sort returns
    shortened_list = questions_list[0:5]
    return render_template("list.html", questions_list=shortened_list,  # for exapmple id and arrow up or down as string
                           sort_titles=sort_title,
                           sorto=key_sort,
                           tags_names=tags_names, tags_questions=tags_questions)


@app.route('/all_questions', methods=['GET', 'POST'])
def all_questions():
    key_sort = 0
    questions_list = get_columns('question')
    up = '\u21A5'
    down = '\u21A7'
    sort_title = ['id' + up, 'id' + down, 'vote_number' + up, 'vote_number' + down, 'view_number' + up,
                  'view_number' + down]
    tags_names = get_columns('tag')
    tags_questions = get_columns('question_tag')
    if request.method == "POST":
        key_sort = [item for item in sort_title if request.form['sort'] == item][0]
        sorting_order = 'asc' if key_sort[-1] == up else 'desc'
        questions_list = sort_by_column('question', key_sort[:-1],
                                        sorting_order)  # get all columns sorted by column(key_sort returns
    return render_template("list.html", questions_list=questions_list,  # for exapmple id and arrow up or down as string
                           sort_titles=sort_title,
                           sorto=key_sort,
                           tags_names=tags_names, tags_questions=tags_questions)


@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    change_view_count(question_id, "up")
    answers_data = sorted(get_all(question_id), key=lambda z: z['id'])
    comment_data = sorted(get_columns('comment'), key=lambda z: z['id'])
    question_user = get_columns_with_condition('username', 'question', 'id', question_id)

    time = get_columns_with_condition('submission_time', 'question', 'id', question_id)
    tags_names = get_columns('tag')
    tags_questions = get_columns('question_tag')
    if request.method == "POST":
        change = 1 if request.form['send'] == '+' else -1
        change_view_count(question_id, 'down')
        update_vote('question', change, question_id)
        if change == 1:
            update_reputation(5, question_user)
        elif change == -1:
            update_reputation(-2, question_user)



    question_data = get_all_columns_with_condition('question', 'id', question_id)[0]
    if question_data['image'] is None:
        img = 'https://i.pinimg.com/236x/24/23/93/242393e70e9f431d3d10ebaa48d76806--bukowski-facebook-profile.jpg'
    else:
        img = question_data['image']

    return render_template('question.html', question_data=question_data, time=time,
                           answers=answers_data, question_id=question_id, comment_data=comment_data, image=img,
                           tags_names=tags_names, tags_questions=tags_questions)


@app.route('/question/<int:question_id>/<int:answer_id>', methods=["GEt", "POST"])
def update_answer_vote(answer_id, question_id):
    if request.method == "POST":
        change = 1 if request.form['send-a'] == '+' else -1
        change_view_count(question_id, 'down')
        update_vote('answer', change, answer_id)
        answer_user = get_columns_with_condition('username', 'answer', 'id', answer_id)
        if change == 1:
            update_reputation(10, answer_user)
        elif change == -1:
            update_reputation(-2, answer_user)
    return redirect(url_for('.display_question', question_id=question_id))


@app.route('/question/<int:question_id>/new-answer', methods=["GET", "POST"])
def answer_question(question_id):
    if request.method == "POST":
        if session.get('logged_in'):
            username = session['username']
        else:
            username = None
        time = get_real_time()
        answer_list = [get_last_id('answer') + 1,  # unique key?
                       time,
                       "0",
                       question_id,
                       request.form["answer"],
                       None,
                       username]
        add_data('answer', FIELDS_A, answer_list)
        return redirect(url_for('.display_question', question_id=question_id))
    return render_template('answer.html', question_id=question_id)


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        search_phrase = request.form['search']
        print(search_phrase)
        return redirect(url_for('search_query', search_phrase=search_phrase))


@app.route("/search?q=<search_phrase>")
def search_query(search_phrase):
    data = search_db(search_phrase)

    return render_template('search.html', question_list=data, phrase=search_phrase)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if session.get('logged_in'):
        username = session['username']
    else:
        username = None
    tag_names = get_columns('tag')
    if request.method == 'POST':
        new_id = get_last_id('question') + 1
        time = get_real_time()
        view = 0
        vote = 0
        title = request.form['title']
        image = None
        message = request.form['message']
        new_question = [
            new_id,
            time,
            view,
            vote,
            title,
            message,
            image,
            username
        ]
        tags = request.form.getlist('box')
        add_data('question', FIELDS_Q, new_question)
        add_tags(tags, new_id)
        return redirect('/')
    return render_template('ask_question.html', tag_names=tag_names)


@app.route("/question/<question_id>/delete")
def del_question(question_id):
    del_data('comment', "question_id", question_id)
    del_data('answer', 'question_id', question_id)
    del_data('question_tag', "question_id", question_id)
    del_data('question', "id", question_id)
    return redirect("/")


@app.route("/question/<question_id>/delete_comment/<comment_id>")
def del_comment(question_id, comment_id):
    del_data('comment', "id", comment_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/question/<question_id>/delete_answer/<answer_id>")
def del_answer(question_id, answer_id):
    del_data('answer', "id", answer_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if session.get('logged_in'):
        username = session['username']
    else:
        username = None
    if request.method == 'POST':
        time = get_real_time()
        message = request.form['comment']
        new_id = get_last_id('comment') + 1
        values = [
            new_id,
            question_id,
            message,
            time,
            username
        ]
        add_data('comment', FIELDS_C_Q, values)
        return redirect(url_for('.display_question', question_id=question_id))
    return render_template('comment.html', question_id=question_id)


@app.route('/question/<question_id>/new-comment/<answer_id>', methods=['GET', 'POST'])
def add_comment_to_answer(question_id, answer_id):
    if session.get('logged_in'):
        username = session['username']
    else:
        username = None
    if request.method == 'POST':
        time = get_real_time()
        message = request.form['comment']
        new_id = get_last_id('comment') + 1
        values = [
            new_id,
            answer_id,
            message,
            time,
            username
        ]
        add_data('comment', FIELDS_C_A, values)
        return redirect(url_for('.display_question', question_id=question_id))
    return render_template('comment.html', question_id=question_id, answer_id=answer_id)


@app.route('/question/<int:question_id>/edit_comment/<int:comment_id>', methods=['GET', 'POST'])
def edit_question_comment(question_id, comment_id):
    message = get_columns_with_condition('message', 'comment', 'id', comment_id)
    if request.method == 'POST':
        updated_message = request.form['message']
        edit_comments(updated_message, comment_id)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('edit.html', message=message, comment_id=comment_id,
                           question_id=question_id)


@app.route('/question/<int:question_id>/edit/<int:answer_id>', methods=['GET', 'POST'])
def edit_answers(question_id, answer_id):
    message = get_columns_with_condition('message', 'answer', 'id', answer_id)
    if request.method == 'POST':
        updated_message = request.form['message']
        edit_answer(updated_message, answer_id)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('edit.html', message=message, question_id=question_id,
                           answer_id=answer_id)


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def new_tag(question_id):
    tag_names = get_columns('tag')
    tag_question = get_all_columns_with_condition('question_tag', 'question_id', question_id)
    list_of_tag_ids = [dic['tag_id'] for dic in tag_question]
    for dicts in tag_question:
        if dicts['question_id'] == int(question_id):
            delete_tag(question_id, dicts['tag_id'])
    if request.method == 'POST':
        tags = request.form.getlist('box')

        temp = request.form['new_tag_add']
        if temp != '':
            new_id = get_last_id('tag') + 1
            headers = [

                'id',
                'name'
            ]
            tags.append(new_id)

            add_data('tag', headers, [new_id, temp])
            add_tags(tags, question_id)
            return redirect(url_for('display_question', question_id=question_id))
        else:
            add_tags(tags, question_id)
            return redirect(url_for('display_question', question_id=question_id))

    return render_template('new_tag.html', question_id=question_id, tag_names=tag_names,
                           list_of_tag_ids=list_of_tag_ids)


@app.route('/question/<int:question_id>/answer/<int:answer_id>/edit_comment/<int:comment_id>', methods=['GET', 'POST'])
def edit_answer_coment(question_id, answer_id, comment_id):
    message = get_columns_with_condition('message', 'comment', 'id', comment_id)
    if request.method == 'POST':
        updated_message = request.form['message']
        edit_comments(updated_message, comment_id)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('edit.html', message=message, comment_id=comment_id,
                           answer_id=answer_id, question_id=question_id)


@app.route('/question/<question_id>/delete-tag/<tag_id>')
def delete_tag_from_question(question_id, tag_id):
    delete_tag(question_id, tag_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = get_columns_with_condition('password', 'users', 'username', username)
        if not data:
            wrong_data = 'Invalid username or password'
            return render_template('login.html', wrong_data=wrong_data)
        else:
            if verify_password(password, data):
                session['username'] = username
                session['password'] = password
                session['logged_in'] = True
                return redirect(url_for('.main'))
            else:
                wrong_data = 'Invalid username or password'
                return render_template('login.html', wrong_data=wrong_data)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('logged_in', None)
    return redirect(url_for('.main'))



@app.route('/user/<string:users_name>', methods=['GET', 'POST'])
def user_cabinet(users_name):
    user_questions = get_all_columns_with_condition('question','username', users_name)
    user_answers = get_all_columns_with_condition('answer', 'username', users_name)
    user_comments = get_all_columns_with_condition('comment', 'username', users_name)
    user_reputation = get_all_columns_with_condition('users', 'username', users_name)[0]["reputation"]
    return render_template('user.html', user_questions=user_questions,
                           user_answers=user_answers, user_comments=user_comments,
                           user_reputation=user_reputation)


@app.route('/accept/<answer_id>/<question_id>')
def accept_answer(answer_id, question_id):
    update_accept(answer_id)
    question_user = get_columns_with_condition('username', 'answer', 'id', answer_id)
    update_reputation(10, question_user)
    return redirect(url_for('.display_question', question_id=question_id))


@app.context_processor
def pass_user_to_template():
    if session.get('logged_in'):
        user = session['username']
    else:
        user = 'Stranger'
    return dict(user=user)


@app.route('/tags')
def show_all_tags():
    counted_tags = count_tags()
    return render_template('all_tags.html', counted_taqs=counted_tags)


@app.route('/tags/<tag_id>')
def show_questions_with_tag(tag_id):
    questions_with_tag = get_question_with_tag(tag_id)
    return render_template('specific_tag.html', questions=questions_with_tag)


@app.route('/all_users')
def all_users():
    users_name_reputation = get_users_name_reputation()
    users_name_reputation = sorted(users_name_reputation, key=lambda z: z['reputation'], reverse=True)
    return render_template('all_users_properties.html', users_name_reputation=users_name_reputation)


if __name__ == '__main__':
    app.run()


