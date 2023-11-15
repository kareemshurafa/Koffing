from flask import Flask
app = Flask(__name__)

@app.route("/home")
def hello_world():
    return "<h2 style='color:red'>Hello Koffing! This is the final test!</h2>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')