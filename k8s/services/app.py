import socket

from flask import Flask

app = Flask(__name__)

counter = 0

@app.route("/")
def hello_world():
    return f"[v5] Hello, Kubernetes!. Host: {socket.gethostname()}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
