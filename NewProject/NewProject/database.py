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

#  a function that creates the database if it doesn't exist
def create_database():
    # create the users table
    query_database(database=utills.USER_DB, query=
                   '''CREATE TABLE IF NOT EXISTS users 
                    (username TEXT UNIQUE NOT NULL,
                     password TEXT NOT NULL,
                     firstName TEXT NOT NULL,
                     lastName TEXT NOT NULL,
                     email TEXT NOT NULL,
                     isAdmin BOOLEAN NOT NULL)'''
                   )
    # create the quizzes table
    # create the questions table
    # create the answers table