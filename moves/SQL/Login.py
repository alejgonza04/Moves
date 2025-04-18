from asyncio.windows_events import NULL
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
        cursor.execute('INSERT INTO favorites'
                       '(email)'
                       'VALUES (%s)',
                       (email, ))
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
        cursor.execute('DELETE FROM favorites where email = %s',
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
        cursor.execute('UPDATE favorites SET email = %s WHERE email = %s',
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

def updateFavorite(database, email, newFavorite):
    cursor = database.cursor();
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Invalid email")
        return database, False
    cursor.execute(
            'SELECT * FROM favorites WHERE email = %s', (email, ))
    account = cursor.fetchone()
    if not account:
        print("Account does not exist!")
        return database, False
    for favorite in account:
        if (favorite == newFavorite):
            print("Favorite already in list")
            return database, False
    cursor.execute(
        'SELECT favorite1 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == None:
        cursor.execute(
            'UPDATE favorites SET favorite1 = %s WHERE email = %s', (newFavorite, email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite2 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == None:
        cursor.execute(
            'UPDATE favorites SET favorite2 = %s WHERE email = %s', (newFavorite, email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite3 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == None:
        cursor.execute(
            'UPDATE favorites SET favorite3 = %s WHERE email = %s', (newFavorite, email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite4 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == None:
        cursor.execute(
            'UPDATE favorites SET favorite4 = %s WHERE email = %s', (newFavorite, email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite5 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == None:
        cursor.execute(
            'UPDATE favorites SET favorite5 = %s WHERE email = %s', (newFavorite, email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite6 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == None:
        cursor.execute(
            'UPDATE favorites SET favorite6 = %s WHERE email = %s', (newFavorite, email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite7 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == None:
        cursor.execute(
            'UPDATE favorites SET favorite7 = %s WHERE email = %s', (newFavorite, email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite8 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == None:
        cursor.execute(
            'UPDATE favorites SET favorite8 = %s WHERE email = %s', (newFavorite, email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite9 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == None:
        cursor.execute(
            'UPDATE favorites SET favorite9 = %s WHERE email = %s', (newFavorite, email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite10 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == None:
        cursor.execute(
            'UPDATE favorites SET favorite10 = %s WHERE email = %s', (newFavorite, email, ))
        database.commit()
        return database, True
    return database, False

def deleteFavorite(database, email, favoriteToRemove):
    cursor = database.cursor();
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Invalid email")
        return database, False
    cursor.execute(
            'SELECT * FROM favorites WHERE email = %s', (email, ))
    account = cursor.fetchone()
    if not account:
        print("Account does not exist!")
        return database, False
    cursor.execute(
        'SELECT favorite1 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == favoriteToRemove:
        cursor.execute(
            'UPDATE favorites SET favorite1 = NULL WHERE email = %s', (email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite2 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == favoriteToRemove:
        cursor.execute(
            'UPDATE favorites SET favorite2 = NULL WHERE email = %s', (email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite3 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == favoriteToRemove:
        cursor.execute(
            'UPDATE favorites SET favorite3 = NULL WHERE email = %s', (email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite4 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == favoriteToRemove:
        cursor.execute(
            'UPDATE favorites SET favorite4 = NULL WHERE email = %s', (email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite5 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == favoriteToRemove:
        cursor.execute(
            'UPDATE favorites SET favorite5 = NULL WHERE email = %s', (email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite6 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == favoriteToRemove:
        cursor.execute(
            'UPDATE favorites SET favorite6 = NULL WHERE email = %s', (email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite7 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == favoriteToRemove:
        cursor.execute(
            'UPDATE favorites SET favorite7 = NULL WHERE email = %s', (email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite8 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == favoriteToRemove:
        cursor.execute(
            'UPDATE favorites SET favorite8 = NULL WHERE email = %s', (email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite9 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == favoriteToRemove:
        cursor.execute(
            'UPDATE favorites SET favorite9 = NULL WHERE email = %s', (email, ))
        database.commit()
        return database, True
    cursor.execute(
        'SELECT favorite10 FROM favorites WHERE email = %s', (email, ))
    check = cursor.fetchone()
    if check[0] == favoriteToRemove:
        cursor.execute(
            'UPDATE favorites SET favorite10 = NULL WHERE email = %s', (email, ))
        database.commit()
        return database, True
    return database, False


def getFavorites(database, email):
    cursor = database.cursor();
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Invalid email")
        return database, False
    cursor.execute(
            'SELECT * FROM favorites WHERE email = %s', (email, ))
    account = cursor.fetchone()
    if not account:
        print("Account does not exist!")
        return database, False
    output = []
    for favorite in account:
        if (favorite != None and favorite != email):
            output.append(favorite)
    return database, output, True
