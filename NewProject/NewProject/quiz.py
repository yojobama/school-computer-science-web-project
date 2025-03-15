
import random
import uuid
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
import json
import database
from auth import login_required, username, yj_render,  is_admin

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
                        parameters=(quiz_id,))
                    if not existing_quiz:
                        break
                
                # Save the image with the name of the quiz id under the images folder in static
                image.save(f'static/images/{quiz_id}.png')
                
                # Insert the quiz into the database
                database.query_database(
                    query='INSERT INTO quizzes (ID, title, description, creator) VALUES (?, ?, ?, ?)',
                    parameters=(quiz_id, title, description, username))

                # Insert each question into the questions table
                for question in questions:
                    question_text = question["question"]
                    question_answer = question["answer"]
                    options = json.dumps(question["options"])  # Store options as JSON
                    database.query_database(
                        query='INSERT INTO questions (quizID, question, answer, options) VALUES (?, ?, ?, ?)',
                        parameters=(quiz_id, question_text, question_answer, options))

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
def viewQuizes():
    return yj_render('quizView.html')


@quiz_bp.route('/getQuiz/<quizName>')
@login_required
def getQuiz(quizName):
    global username
    data = database.query_database(
        query='SELECT * FROM quizzes WHERE title = ?',
        parameters=(quizName, ))
    
    quiz_data = next((item for item in data if item['title'] == quizName), None)
    if quiz_data is None:
        return "Quiz not found", 404
    
    return yj_render('quiz.html', data=json.dumps(quiz_data))


@quiz_bp.route('/getQuizes')
# @login_required
def getQuizes():
    # query the database to get all of the quizzes and then jsonify them
    data = database.query_database(
        query='SELECT ID ,title, description FROM quizzes')
    print(jsonify(data))
    return jsonify(data)


@quiz_bp.route("/users")
def users():
    user_list = database.query_database(
        query='SELECT username, password, firstName, lastName, email FROM users'
    )
    return yj_render('users.html', users=user_list)
