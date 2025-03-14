from functools import wraps
import json
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
import sqlite3

import database

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flash messages

# TODO: delete the dictionary
users = {
    'Yoav': 'A!1111',
    'John': 'A!1111',
    'Barak': 'A!1111',
    'Maurice': 'A!1111',
    'yojobama': 'A!1111'
}  # Example user data
username = "Guest"

USER_DB = 'userDB.db'

# a function that simpliphies the process of querying the database
# calling the function that creates the database
database.create_database()


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if username == None or username == "Guest":
            return redirect('/login', code=302)
        return f(*args, **kwargs)

    return decorated_function


# TODO: add a function that returns if the current user is an admin or not
@app.route('/is_admin')
def is_admin():
    return database.query_database(
        database=USER_DB,
        query='SELECT isAdmin FROM users WHERE username = ?',
        parameters=(username))


@app.route("/create", methods=["POST"])
@login_required
def create():
    if request.method == "POST":
        data = request.get_json()
        title = data["name"]
        description = data["description"]
        questions = data["questions"]

        # Insert the quiz into the database
        database.query_database(
            database=USER_DB,
            query='INSERT INTO quizzes (title, description) VALUES (?, ?)',
            parameters=(title, description))

        # Get the quiz ID of the newly inserted quiz
        quiz_id = database.query_database(
            database=USER_DB,
            query='SELECT id FROM quizzes WHERE title = ?',
            parameters=(title, ))[0]['id']

        # Insert each question into the questions table
        for question in questions:
            question_text = question["question"]
            options = json.dumps(question["options"])  # Store options as JSON
            database.query_database(
                database=USER_DB,
                query='INSERT INTO questions (quiz_id, question_text, options) VALUES (?, ?, ?)',
                parameters=(quiz_id, question_text, options))

        flash("Quiz created successfully!")
        return jsonify({"message": "Quiz created successfully!"}), 200
    else:
        return render_template("quizCreation.html")


@app.route("/login", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    global username
    if request.method == 'POST':
        l_username = request.form["username"]
        l_password = request.form["password"]

        # Query the database to check if the username and password match
        result = database.query_database(
            database=USER_DB,
            query='SELECT * FROM users WHERE username = ? AND password = ?',
            parameters=(l_username, l_password))

        if result:  # If a matching user is found
            username = l_username
            return redirect(url_for('hello'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('login'))
    return render_template('login.html', username=username)


@app.route("/getQuizView")
@login_required
def viewQuizes():
    return render_template('quizView.html', username=username)


@app.route("/signup", methods=["POST", "GET"])
@app.route("/signup", methods=["POST", "GET"])
def signup():
    global username
    if request.method == "POST":
        l_username = request.form["username"]
        l_password = request.form["password"]
        l_firstName = request.form["firstName"]
        l_lastName = request.form["lastName"]
        l_email = request.form["email"]

        # Check if the username already exists
        result = database.query_database(
            database=USER_DB,
            query='SELECT * FROM users WHERE username = ?',
            parameters=(l_username, ))
        if not result:  # If no result is found, the username is available
            database.query_database(
                database=USER_DB,
                query=
                'INSERT INTO users (username, password, firstName, lastName, email, isAdmin) VALUES (?, ?, ?, ?, ?, ?)',
                parameters=(l_username, l_password, l_firstName, l_lastName,
                            l_email, False))
            username = l_username
            return redirect(url_for('hello'))
        else:
            flash("Username is already taken!")
            return redirect(url_for('signup'))
    return render_template("signup.html", username=username)


@app.route('/logout')
@login_required
def logout():
    global username
    username = "Guest"
    return render_template('home.html', username=username)


@app.route('/')
def hello():
    global username
    return render_template('home.html', username=username)


@app.route('/getQuiz/<quizName>')
@login_required
def getQuiz(quizName):
    global username
    # query the database to get the questions of the quiz
    # then make it a json object and pass it to the template
    data = database.query_database(
        database=USER_DB,
        query='SELECT * FROM quizzes WHERE title = ?',
        parameters=(quizName, ))

    # data = {
    #     'test1': {'header': 'Sample Quiz', 'questions':
    #               [{'question': "test question 1", 'options': ['option 1', 'option 2', 'option 3']},
    #                {'question': "test question 2", 'options': ['option 1 p', 'option 2 p', 'option 3 p']},
    #                {'question': "test question 3", 'options': ['option 1 pp', 'option 2 pp', 'option 3 pp']}]}
    # }
    return render_template('quiz.html',
                           data=json.dumps(data[quizName]),
                           username=username)


@app.route('/getQuizes')
@login_required
def getQuizes():
    # query the database to get all of the quizzes and then jsonify them
    # TODO: add picture GUID (global unique ID)
    data = database.query_database(
        database=USER_DB, query='SELECT title, description FROM quizzes')

    data = {
        'items': [{
            'imageSrc': url_for('static', filename='images/test1.png'),
            'name': 'test1'
        }, {
            'imageSrc': url_for('static', filename='images/test2.png'),
            'name': 'test2'
        }, {
            'imageSrc': url_for('static', filename='images/test3.png'),
            'name': 'test3'
        }, {
            'imageSrc': url_for('static', filename='images/test4.png'),
            'name': 'test4'
        }]
    }
    return jsonify(data)


@app.route("/users")
def users():
    user_list = database.query_database(
        database=USER_DB,
        query='SELECT username, password, firstName, lastName, email FROM users'
    )
    return render_template('users.html', users=user_list, username=username)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)