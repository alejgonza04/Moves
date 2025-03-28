from Login import getDatabaseForAccountTable, testLogin, createAccount

# Attempt to connect to the database
cnx = getDatabaseForAccountTable("root", "1qaz@WSX3edc")

# If connection fails, don't continue
if cnx is None:
    print("Cannot run tests: Database connection failed")
    exit(1)

# First login attempt (should fail if user doesn't exist)
cnx, check = testLogin(cnx, "a", "b@c.com", "d")
if check:
    print("Login success (existing user)")
else:
    print("Login failed (user not found yet)")

# Attempt to create the user
cnx, check = createAccount(cnx, "a", "b@c.com", "d")
if check:
    print("Account creation success")
else:
    print("Account creation failed")

# Second login attempt (should succeed now)
cnx, check = testLogin(cnx, "a", "b@c.com", "d")
if check:
    print("Login success after account creation")
else:
    print("Login failed after account creation")
