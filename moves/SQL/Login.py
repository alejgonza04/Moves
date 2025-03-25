import mysql.connector
from mysql.connector import errorcode
import re

def getDatabaseForAccountTable(usernameinput, passwordinput):
    try:
        database = mysql.connector.connect(user=usernameinput, password=passwordinput, host='127.0.0.1', database='movesprofile')
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    else:
        print("got cursor")
        return database

def testLogin(database, username, email, password):
    cursor = database.cursor()
    cursor.execute(
            'SELECT * FROM account WHERE username = %s \
            AND email = %s \
            AND password = %s', (username, email, password, ))
    account = cursor.fetchone()
    if account:
        return database, True
    else:
        return database, False

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
