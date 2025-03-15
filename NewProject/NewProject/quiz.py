
from email import quoprimime
import random
import uuid
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
import json
import database
from auth import admin_required, login_required, username, yj_render, is_admin

quiz_bp = Blueprint('quiz', __name__)


@quiz_bp.route("/create", methods=["POST", "GET"])
@login_required
def create():
    if request.method == "POST":
        if request.content_type.startswith('multipart/form-data'):
            quiz_data = request.form.get('quizData')
            if quiz_data:
                data = json.loads(quiz_data)
                title = data["name"]
                description = data["description"]
                questions = data["questions"]
                image = request.files["image"]

                # create a uuid for the quiz using a random 32 bit integer
                quiz_id: int
                while True:
                    quiz_id = str(random.randint(0, 4294967296))
                    existing_quiz = database.query_database(
                        query='SELECT ID FROM quizzes WHERE ID = ?',
                        parameters=(quiz_id, ))
                    if not existing_quiz:
                        break

                # Save the image with the name of the quiz id under the images folder in static
                image.save(f'static/images/{quiz_id}.png')

                # Insert the quiz into the database
                database.query_database(
                    query=
                    'INSERT INTO quizzes (ID, title, description, creator) VALUES (?, ?, ?, ?)',
                    parameters=(quiz_id, title, description, username))

                # Insert each question into the questions table
                for question in questions:
                    question_text = question["question"]
                    question_answer = question["answer"]
                    options = json.dumps(
                        question["options"])  # Store options as JSON
                    database.query_database(
                        query=
                        'INSERT INTO questions (quizID, question, answer, options) VALUES (?, ?, ?, ?)',
                        parameters=(quiz_id, question_text, question_answer,
                                    options))

                flash("Quiz created successfully!")
                return jsonify({"message": "Quiz created successfully!"}), 200
            else:
                flash("Invalid form data.", "error")
                return redirect(url_for('quiz.create'))
        else:
            flash("Unsupported Media Type. Please send form data.", "error")
            return redirect(url_for('quiz.create'))
    else:
        return yj_render("quizCreation.html")


@quiz_bp.route("/getQuizView")
@login_required
def viewQuizes():
    return yj_render('quizView.html')


@quiz_bp.route("/getQuiz/<quizID>")
@login_required
def getQuiz(quizID):
    global username
    data = database.query_database(
        query='SELECT question, options, answer FROM questions WHERE quizID = ?',
        parameters=(quizID, ))

    if not data:
        return jsonify({"error": "Quiz not found"}), 404

    # Format the data to match the expected JSON structure
    quiz_data = {
        "header":
        f"{database.query_database('SELECT title FROM quizzes WHERE ID = ?', (quizID,))[0][0]}",
        "questions": [
            {
                "question":
                item[0],  # Access the first element of the tuple
                "options":
                json.loads(
                    item[1]
                ),  # Access the second element of the tuple and parse JSON
                "answer":
                item[2]
            } for item in data
        ]
    }

    return yj_render('quiz.html', data=json.dumps(quiz_data))


@quiz_bp.route('/getQuizes')
@login_required
def getQuizes():
    # query the database to get all of the quizzes and then jsonify them
    data = database.query_database(
        query='SELECT ID ,title, description FROM quizzes')
    print(jsonify(data))
    return jsonify(data)


@quiz_bp.route("/users")
@login_required
@admin_required
def users():
    user_list = database.query_database(
        query='SELECT username, password, firstName, lastName, email FROM users'
    )
    return yj_render('users.html', users=user_list)
