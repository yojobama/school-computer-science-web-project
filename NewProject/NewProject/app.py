from flask import Flask, render_template
import database
from auth import auth_bp, yj_render
from quiz import quiz_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flash messages

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp)

# Initialize the database
database.create_database()

@app.route('/')
def hello():
    from auth import username  # Import the username variable
    return yj_render('home.html')

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
