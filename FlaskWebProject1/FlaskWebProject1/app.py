"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

username = "Guest"


@app.route("/signup")
def signup():
    global username
    return render_template('signup.html', username = username)


@app.route("/login")
def login():
    global username
    return render_template('login.html', username = username)

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
