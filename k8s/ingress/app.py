import socket

from flask import Flask

app = Flask(__name__)

counter = 0

@app.route("/api")
def api():
    return f"[v6] Hello, Kubernetes API!. Host: {socket.gethostname()}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
