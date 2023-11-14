from flask import Flask
app = Flask(__name__)

@app.route("/home")
def hello_world():
    return "<h1 style='color:green'>Hello World! This is the final test!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')