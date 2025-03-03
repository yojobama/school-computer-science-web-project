from functools import wraps
import json
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
import sqlite3

from sympy import linear_eq_to_matrix

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flash messages

# TODO: delete the dictionary
users = {'Yoav': 'A!1111', 'John': 'A!1111', 'Barak': 'A!1111', 'Maurice': 'A!1111', 'yojobama': 'A!1111'}  # Example user data
username = "Guest"

# a function that simpliphies the process of querying the database
def query_database(database, query, parameters=()):
    connection = sqlite3.connect(database)
    executor = connection.cursor()
    executor.execute(query, parameters)
    result = executor.fetchall()
    executor.close()
    connection.commit()
    connection.close()
    return result

#  a function that creates the database if it doesn't exist
def create_database():
    query_database(database='userDB.db', query=
                   '''CREATE TABLE IF NOT EXISTS users 
                    (username TEXT UNIQUE NOT NULL,
                     password TEXT NOT NULL,
                     firstName TEXT NOT NULL,
                     lastName TEXT NOT NULL,
                     email TEXT NOT NULL,
                     isAdmin BOOLEAN NOT NULL)'''
                   )
# calling the function that creates the database
create_database()

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
    return query_database(database='userDB.db', query='SELECT isAdmin FROM users WHERE username = ?', parameters=(username))

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        pass
        # TODO: Implement this
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
        result = query_database(database='userDB.db', query='SELECT * FROM users WHERE username = ? AND password = ?', parameters=(l_username, l_password))
        
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
        result = query_database(database='userDB.db', query='SELECT * FROM users WHERE username = ?', parameters=(l_username,))
        if not result:  # If no result is found, the username is available
            query_database(database='userDB.db', query='INSERT INTO users (username, password, firstName, lastName, email, isAdmin) VALUES (?, ?, ?, ?, ?, ?)', parameters=(l_username, l_password, l_firstName, l_lastName, l_email, False))
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
    data = {
        'test1': {'header': 'Sample Quiz', 'questions': 
                  [{'question': "test question 1", 'options': ['option 1', 'option 2', 'option 3']},
                   {'question': "test question 2", 'options': ['option 1 p', 'option 2 p', 'option 3 p']},
                   {'question': "test question 3", 'options': ['option 1 pp', 'option 2 pp', 'option 3 pp']}]}
    }
    return render_template('quiz.html', data=json.dumps(data[quizName]), username=username)

@app.route('/getQuizes')
@login_required
def getQuizes():
    data = {
        'items': [
            {'imageSrc': url_for('static', filename='images/test1.png'), 'name': 'test1'},
            {'imageSrc': url_for('static', filename='images/test2.png'), 'name': 'test2'},
            {'imageSrc': url_for('static', filename='images/test3.png'), 'name': 'test3'},
            {'imageSrc': url_for('static', filename='images/test4.png'), 'name': 'test4'}
        ]
    }
    return jsonify(data)

@app.route("/users")
def users():
    user_list = query_database(database='userDB.db', query='SELECT username, password, firstName, lastName, email FROM users')
    return render_template('users.html', users=user_list, username=username)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)