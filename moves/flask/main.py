import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
from SQL.Login import getDatabaseForAccountTable, testLogin, createAccount

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api/users', methods=['GET', 'POST'])
def users():
    db = getDatabaseForAccountTable("root", "1qaz@WSX3edc")
    if db is None:
        return jsonify({"message": "Database connection failed."}), 500

    if request.method == 'GET':
        inputdata = request.args
        username = inputdata.get("username")
        email = inputdata.get("email")
        password = inputdata.get("password")

        _, success = testLogin(db, username, email, password)
        if success:
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"message": "Login failed."}), 401

    elif request.method == 'POST':
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        _, success = createAccount(db, username, email, password)
        if success:
            return jsonify({"message": "Account created!"}), 201
        else:
            return jsonify({"message": "Account creation failed."}), 400

@app.route("/signup", methods=["POST", "OPTIONS"])
def signupMethod():
    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json()
    print("Received data:", data["username"], data["email"], data["password"])

    db = getDatabaseForAccountTable("root", "1qaz@WSX3edc")
    print(db)
    if db is None:
        return jsonify({"message": "Database connection failed."}), 500

    _, success = createAccount(db, data["username"], data["email"], data["password"])

    if success:
        return jsonify({"message": "Account created!"}), 201
    else:
        return jsonify({"message": "Account creation failed."}), 400
    
@app.route("/login", methods=["POST", "OPTIONS"])
def loginMethod():
    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json()
    print("Login attempt:", data["email"], data["password"])

    db = getDatabaseForAccountTable("root", "1qaz@WSX3edc")
    if db is None:
        return jsonify({"message": "Database connection failed."}), 500

    _, success = testLogin(db, data["email"], data["password"])  # ✅ updated call

    if success:
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid login credentials."}), 401



if __name__ == '__main__':
    app.run(port=5555, debug=True)
