import mysql.connector
from mysql.connector import errorcode

def getCursorToAccount(usernameinput, passwordinput):
    try:
        cnx = mysql.connector.connect(user=usernameinput, password=passwordinput, host='127.0.0.1', database='movesprofile')
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    else:
      return cnx.cursor

def testLogin(cursor, username, email, password):
    cursor.execute(
            'SELECT * FROM accounts WHERE username = % s \
            AND email = % s \
            AND password = % s', (username, email, password))
    account = cursor.fetchone()
    if account:
        return true
    else:
        return false

def createAccount(cursor, username, email, password):
    cursor.execute(
            'SELECT * FROM accounts WHERE email = % s', (email, ))
    account = cursor.fetchone()
    if account:
        print("Account already exists!")
        return false
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Invalid email")
        return false
    else:
        cursor.execute('INSERT INTO movesprofile '
                       '(username, email, password)'
                       'VALUES (% s, % s, % s)',
                       (username, email, password, ))
        return true
