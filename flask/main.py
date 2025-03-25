from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/signup", methods=["POST", 'OPTIONS'])
def signupMethod():
    if request.method == 'OPTIONS':
        return '', 204
    data = request.get_json()
    print("Received data:", data["username"], data["password"])
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)