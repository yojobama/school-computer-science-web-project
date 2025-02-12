from functools import wraps
import json
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flash messages

users = {'Yoav': 'A!1111', 'John': 'A!1111', 'Barak': 'A!1111', 'Maurice': 'A!1111', 'yojobama': 'A!1111'}  # Example user data
username = "Guest"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if username == None or username == "Guest":
            return redirect('/login', code=302)
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=['GET', 'POST'])
def login():
    global username
    if request.method == 'POST':
        l_username = request.form["username"]
        password = request.form["password"]

        global users
        
        if l_username in users and users[l_username] == password:
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
def signup():
    global username
    if request.method == "POST":
        global users
        l_username = request.form["username"]
        password = request.form["password"]
        if l_username not in users:
            users[l_username] = password
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

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)