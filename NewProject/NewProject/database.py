import sqlite3
import utills


def query_database(database, query, parameters=()):
    connection = sqlite3.connect(database)
    executor = connection.cursor()
    executor.execute(query, parameters)
    result = executor.fetchall()
    executor.close()
    connection.commit()
    connection.close()
    return result


# a function that creates the database if it doesn't exist
def create_database():
    # create the users table
    query_database(database=utills.USER_DB,
                   query='''
                   CREATE TABLE IF NOT EXISTS users 
                   (
                     username TEXT UNIQUE NOT NULL,
                     password TEXT NOT NULL,
                     firstName TEXT NOT NULL,
                     lastName TEXT NOT NULL,
                     email TEXT NOT NULL,
                     isAdmin BOOLEAN NOT NULL
                   )
                   ''')
    # create the quizzes table
    query_database(database=utills.USER_DB,
                   query='''
                   CREATE TABLE IF NOT EXISTS quizzes 
                   (
                     ID INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     description TEXT NOT NULL,
                     creator TEXT NOT NULL
                   )
                   ''')
    # create the questions table
    query_database(database=utills.USER_DB,
                   query='''
                   CREATE TABLE IF NOT EXISTS questions
                   (
                     quizID INTEGER NOT NULL,
                     question TEXT NOT NULL,
                     answer TEXT NOT NULL,
                     options TEXT NOT NULL
                   )
                   ''')

    # create an admin user named "Admin"
    query_database(
        database=utills.USER_DB,
        query=
        ('INSERT INTO users (username, password, firstName, lastName, email, isAdmin) '
         'VALUES (?, ?, ?, ?, ?, ?)'),
        parameters=("Admin", "A!1111", "Yoav John", "Barak-Maurice", "yojobama@gmail.com",
                    True))
