
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
import json
import database
from utills import login_required

quiz_bp = Blueprint('quiz', __name__)

username = "Guest"

@quiz_bp.route("/create", methods=["POST"])
@login_required
def create():
    if request.method == "POST":
        data = request.get_json()
        title = data["name"]
        description = data["description"]
        questions = data["questions"]

        # Insert the quiz into the database
        database.query_database(
            query='INSERT INTO quizzes (title, description) VALUES (?, ?)',
            parameters=(title, description))

        # Get the quiz ID of the newly inserted quiz
        quiz_id = database.query_database(
            query='SELECT id FROM quizzes WHERE title = ?',
            parameters=(title, ))[0]['id']

        # Insert each question into the questions table
        for question in questions:
            question_text = question["question"]
            options = json.dumps(question["options"])  # Store options as JSON
            database.query_database(
                query=
                'INSERT INTO questions (quiz_id, question_text, options) VALUES (?, ?, ?)',
                parameters=(quiz_id, question_text, options))

        flash("Quiz created successfully!")
        return jsonify({"message": "Quiz created successfully!"}), 200
    else:
        return render_template("quizCreation.html")


@quiz_bp.route("/getQuizView")
@login_required
def viewQuizes():
    return render_template('quizView.html', username=username)


@quiz_bp.route('/getQuiz/<quizName>')
@login_required
def getQuiz(quizName):
    global username
    # query the database to get the questions of the quiz
    # then make it a json object and pass it to the template
    data = database.query_database(
        query='SELECT * FROM quizzes WHERE title = ?',
        parameters=(quizName, ))

    return render_template('quiz.html',
                           data=json.dumps(data[quizName]),
                           username=username)


@quiz_bp.route('/getQuizes')
@login_required
def getQuizes():
    # query the database to get all of the quizzes and then jsonify them
    data = database.query_database(
        query='SELECT title, description FROM quizzes')

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


@quiz_bp.route("/users")
def users():
    user_list = database.query_database(
        query='SELECT username, password, firstName, lastName, email FROM users'
    )
    return render_template('users.html', users=user_list, username=username)
