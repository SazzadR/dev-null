from flask import Flask

app = Flask(__name__)

counter = 0

@app.route("/")
def hello_world():
    global counter
    counter += 1
    if counter > 3:
        raise Exception("Too many requests")

    return "[v3] Hello, Kubernetes!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
