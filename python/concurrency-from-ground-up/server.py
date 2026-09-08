import socket


def fibonacci(n):
    if n <= 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_handler(client):
    try:
        while True:
            request = client.recv(1024)
            if not request:
                break

            request = request.strip()
            if not request:
                break

            n = int(request)
            result = fibonacci(n)
            response = str(result).encode("ascii") + b"\n"
            client.sendall(response)
    finally:
        client.close()


def fibonacci_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()

    while True:
        client, address = sock.accept()
        print("Connection", address)
        fibonacci_handler(client)


fibonacci_server("127.0.0.1", 25000)
