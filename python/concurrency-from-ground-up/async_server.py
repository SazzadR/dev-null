import socket

from collections import deque
from select import select

tasks = deque()
waiting_to_receive = {}
waiting_to_send = {}


def fibonacci(n):
    if n <= 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_handler(client):
    try:
        while True:
            yield "receive", client
            request = client.recv(1024)
            if not request:
                break

            request = request.strip()
            if not request:
                break

            n = int(request)
            result = fibonacci(n)
            response = str(result).encode("ascii") + b"\n"
            yield "send", client
            client.sendall(response)
    finally:
        client.close()


def fibonacci_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()

    while True:
        yield "receive", sock
        client, address = sock.accept()
        print("Connection", address)
        tasks.append(fibonacci_handler(client))


def run():
    while any([tasks, waiting_to_receive, waiting_to_send]):
        while not tasks:
            can_receive, can_send, _ = select(waiting_to_receive, waiting_to_send, [])

            for sock in can_receive:
                tasks.append(waiting_to_receive.pop(sock))
            for sock in can_send:
                tasks.append(waiting_to_send.pop(sock))

        task = tasks.popleft()
        try:
            why, what = next(task)
            if why == "receive":
                waiting_to_receive[what] = task
            elif why == "send":
                waiting_to_send[what] = task
            else:
                raise RuntimeError("Unknown ARG!")
        except StopIteration:
            print("Task completed.")


tasks.append(fibonacci_server("127.0.0.1", 25000))
run()
