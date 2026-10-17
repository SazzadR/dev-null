import os
import socket

from flask import Flask

app = Flask(__name__)

counter = 0

@app.route("/api")
def api():
    return f"[v8] ConfigMap: {os.getenv('MESSAGE', 'Default configmap')}, Secret: {os.getenv('SECRET_KEY', 'Default secret')}, Host: {socket.gethostname()}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
