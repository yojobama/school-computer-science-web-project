"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from turtle import home
from flask import Flask, flash, redirect, render_template, request, url_for
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

username = "Guest"
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flash messages

users = {'Yoav': 'A!1111', 'John': 'A!1111', 'Barak': 'A!1111', 'Maurice': 'A!1111', 'yojobama': 'A!1111'}  # Example user data

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        l_username = request.form["username"]
        password = request.form["password"]
        
        if l_username in users and users[l_username] == password:
            global username
            username = l_username
            return redirect(url_for('hello'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('login'))
    return render_template('login.html')
@app.route("/signup")
def signup():
    global username
    return render_template('signup.html', username = username)

# @app.route("/login")
# def login():
#     global username
#     return render_template('login.html', username = username)

@app.route('/')
def hello():
    global username
    return render_template('home.html', username = username)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
