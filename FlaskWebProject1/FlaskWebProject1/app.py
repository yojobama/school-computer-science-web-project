from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flash messages

users = {'Yoav': 'A!1111', 'John': 'A!1111', 'Barak': 'A!1111', 'Maurice': 'A!1111', 'yojobama': 'A!1111'}  # Example user data
username = "Guest"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        l_username = request.form["username"]
        password = request.form["password"]

        global users
        
        if l_username in users and users[l_username] == password:
            global username
            username = l_username
            return redirect(url_for('hello'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        global users
        l_username = request.form["username"]
        password = request.form["password"]
        if l_username not in users:
            users[l_username] = password
            global username
            username = l_username
            return redirect(url_for('hello'))
        else:
            flash("Username is already taken!")
            return redirect(url_for('signup'))
    return render_template("signup.html")

@app.route('/')
def hello():
    global username
    return render_template('home.html', username=username)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
