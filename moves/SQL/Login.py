import mysql.connector
from mysql.connector import errorcode
import re

def getDatabaseForAccountTable(usernameinput, passwordinput):
    try:
        database = mysql.connector.connect(
            user=usernameinput,
            password=passwordinput,
            host='127.0.0.1',
            port=3307,
            database='movesprofile'
        )
        print("got cursor")
        return database
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None  # <-- Add this line!

def testLogin(database, email, password):
    cursor = database.cursor()
    cursor.execute(
        'SELECT * FROM account WHERE email = %s AND password = %s',
        (email, password,)
    )
    account = cursor.fetchone()
    cursor.close()
    return database, account is not None


def createAccount(database, username, email, password):
    cursor = database.cursor()
    cursor.execute(
            'SELECT * FROM account WHERE email = %s', (email, ))
    account = cursor.fetchone()
    if account:
        print("Account already exists!")
        return database, False
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Invalid email")
        return database, False
    else:
        cursor.execute('INSERT INTO account'
                       '(username, email, password)'
                       'VALUES (%s, %s, %s)',
                       (username, email, password, ))
        database.commit()
        return database, True
