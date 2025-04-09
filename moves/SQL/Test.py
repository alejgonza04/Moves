import mysql.connector
from Login import *

cnx = getDatabaseForAccountTable("root", "1qaz@WSX3edc")
cnx, check = testLogin(cnx, "b@caba.com", "d")
if check:
    print("login success")
else:
    print("login failure")

cnx, check =  createAccount(cnx, "a", "b@caba.com", "d")
if check:
    print("creation success")
else:
    print("creation failure")

cnx, check =  createAccount(cnx, "a", "ab@caba.com", "d")
if check:
    print("creation success")
else:
    print("creation failure")

cnx, check = updatePassword(cnx, "ab@caba.com", "something random")
if check:
    print("change success")
else:
    print("change failure")


cnx, check = updateUsername(cnx, "ab@caba.com", "something random")
if check:
    print("change success")
else:
    print("change failure")

cnx, check = updateEmail(cnx, "ab@caba.com", "b@caba.com")
if check:
    print("change success")
else:
    print("change failure")

cnx, check = testLogin(cnx, "b@caba.com", "d")
if check:
    print("login success")
else:
    print("login failure")

cnx, check = removeAccount(cnx, "b@caba.com")
if check:
    print("deletion success")
else:
    print("deletion failure")

cnx, check = testLogin(cnx, "b@caba.com", "d")
if check:
    print("login success")
else:
    print("login failure")