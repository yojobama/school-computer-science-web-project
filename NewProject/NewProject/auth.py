from flask import Blueprint, flash, redirect, render_template, request, url_for
import database

auth_bp = Blueprint('auth', __name__)

username = "Guest"


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    global username
    if request.method == 'POST':
        l_username = request.form["username"]
        l_password = request.form["password"]

        # Query the database to check if the username and password match
        result = database.query_database(
            query='SELECT * FROM users WHERE username = ? AND password = ?',
            parameters=(l_username, l_password))

        if result:  # If a matching user is found
            username = l_username
            return redirect(url_for('hello'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('auth.login'))
    return render_template('login.html', username=username)


@auth_bp.route("/signup", methods=["POST", "GET"])
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
            query='SELECT * FROM users WHERE username = ?',
            parameters=(l_username, ))
        if not result:  # If no result is found, the username is available
            database.query_database(query=(
                'INSERT INTO users (username, password, firstName, lastName, email, isAdmin) '
                'VALUES (?, ?, ?, ?, ?, ?)'),
                                    parameters=(l_username, l_password,
                                                l_firstName, l_lastName,
                                                l_email, False))
            username = l_username
            return redirect(url_for('hello'))
        else:
            flash("Username is already taken!")
            return redirect(url_for('auth.signup'))
    return render_template("signup.html", username=username)


@auth_bp.route('/logout')
def logout():
    global username
    username = "Guest"
    return redirect(url_for('hello'))
