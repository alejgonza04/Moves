from flask import Flask, request
from flask import request\

from flask_sqlalchemy import SQLAlchemy
from moves.SQL.Login import *

app = Flask(__name__)

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
    #Gets all the json data from frontend, used like a map: name["item"]
    data = request.get_json()
    print("Received data:", data["username"], data["password"])
    return '', 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
