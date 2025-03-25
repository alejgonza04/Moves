import mysql.connector
from Login import *

cnx = getDatabaseForAccountTable("root", "1qaz@WSX3edc")
cnx, check = testLogin(cnx, "a", "b@c.com", "d")
if check:
    print("login success")
else:
    print("login failure")

cnx, check =  createAccount(cnx, "a", "b@c.com", "d")
if check:
    print("creation success")
else:
    print("creation failure")

cnx, check = testLogin(cnx, "a", "b@c.com", "d")
if check:
    print("login success")
else:
    print("login failure")