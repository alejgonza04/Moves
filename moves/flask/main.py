import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SQL.Login import getDatabaseForAccountTable, testLogin, createAccount

from flask import Flask, request
from flask_cors import CORS
from SQL.Login import *

app = Flask(__name__)
CORS(app)

@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        db = getDatabaseForAccountTable("root", "1qaz@WSX3edc")
        inputdata = request.args
        return testLogin(db, inputdata.get("username"), inputdata.get("email"), inputdata.get("username"))
    elif request.method == 'POST':
        db = getDatabaseForAccountTable("root", "1qaz@WSX3edc")
        inputdata = request.args
        return testLogin(db, inputdata.get("username"), inputdata.get("email"), inputdata.get("username"))

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/signup", methods=["POST", 'OPTIONS'])
def signupMethod():
    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json()
    print("Received data:", data["username"], data["email"], data["password"])

    db = getDatabaseForAccountTable("root", "1qaz@WSX3edc")
    _, success = createAccount(db, data["username"], data["email"], data["password"])
    
    if success:
        return {"message": "Account created!"}, 201
    else:
        return {"message": "Account creation failed."}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
