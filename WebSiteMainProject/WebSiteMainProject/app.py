"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, jsonify, render_template
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/getQuizes')
def get_quizes():
    data = {
        "quizes": [
            {"name": "stuff1", "author": "John1"},
            {"name": "stuff2", "author": "John2"},
            {"name": "stuff3", "author": "John3"}
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '8175'))
    except ValueError:
        PORT = 8175
    app.run(HOST, PORT)
