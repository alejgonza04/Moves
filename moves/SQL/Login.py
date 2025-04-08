import mysql
import mysql.connector
from mysql.connector import errorcode
import re

def getDatabaseForAccountTable(usernameinput, passwordinput):
    try:
        database = mysql.connector.connect(
            user=usernameinput,
            password=passwordinput,
            host='127.0.0.1',
            port=3306,
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
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Invalid email")
        return database, False
    cursor.execute(
        'SELECT * FROM account WHERE email = %s AND password = SHA2(%s, 512)',
        (email, password,)
    )
    account = cursor.fetchone()
    cursor.close()
    return database, account is not None


def createAccount(database, username, email, password):
    cursor = database.cursor()
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Invalid email")
        return database, False
    cursor.execute(
            'SELECT * FROM account WHERE email = %s', (email, ))
    account = cursor.fetchone()
    if account:
        print("Account already exists!")
        return database, False
    else:
        cursor.execute('INSERT INTO account'
                       '(username, email, password)'
                       'VALUES (%s, %s, SHA2(%s, 512))',
                       (username, email, password, ))
        database.commit()
        return database, True

def removeAccount(database, email):
    cursor = database.cursor();
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Invalid email")
        return database, False
    cursor.execute(
            'SELECT * FROM account WHERE email = %s', (email, ))
    account = cursor.fetchone()
    if not account:
        print("Account does not exist!")
        return database, False
    else:
        cursor.execute('DELETE FROM account where email = %s',
                       (email, ))
        database.commit()
        return database, True

def updateEmail(database, email, newemail):
    cursor = database.cursor();
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Invalid email")
        return database, False
    if not re.match(r'[^@]+@[^@]+\.[^@]+', newemail):
        print("Invalid email")
        return database, False
    cursor.execute(
            'SELECT * FROM account WHERE email = %s', (email, ))
    account = cursor.fetchone()
    if not account:
        print("Account does not exist!")
        return database, False
    cursor.execute(
            'SELECT * FROM account WHERE email = %s', (newemail, ))
    account = cursor.fetchone()
    if account:
        print("Account already exists!")
        return database, False
    else:
        cursor.execute('UPDATE account SET email = %s WHERE email = %s',
                       (newemail, email, ))
        database.commit()
        return database, True

def updateUsername(database, email, username):
    cursor = database.cursor();
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Invalid email")
        return database, False
    cursor.execute(
            'SELECT * FROM account WHERE email = %s', (email, ))
    account = cursor.fetchone()
    if not account:
        print("Account does not exist!")
        return database, False
    else:
        cursor.execute('UPDATE account SET username = %s WHERE email = %s',
                       (username, email, ))
        database.commit()
        return database, True

def updatePassword(database, email, password):
    cursor = database.cursor();
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Invalid email")
        return database, False
    cursor.execute(
            'SELECT * FROM account WHERE email = %s', (email, ))
    account = cursor.fetchone()
    if not account:
        print("Account does not exist!")
        return database, False
    else:
        cursor.execute('UPDATE account SET password = SHA2(%s, 512) WHERE email = %s',
                       (password, email, ))
        database.commit()
        return database, True
