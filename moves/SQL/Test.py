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

cnx, check = updateFavorite(cnx, "ab@caba.com", "should appear")
if check:
    print("favorite success")
else:
    print("favorite failure")

cnx, check = updateFavorite(cnx, "ab@caba.com", "should not appear")
if check:
    print("favorite success")
else:
    print("favorite failure")

cnx, check = deleteFavorite(cnx, "ab@caba.com", "should not appear")
if check:
    print("delete favorite success")
else:
    print("delete favorite failure")

cnx, output, check = getFavorites(cnx, "ab@caba.com")
if check:
    print("favorites list:")
    for favorite in output:
        print(favorite)
else:
    print("failed to get favorites list")