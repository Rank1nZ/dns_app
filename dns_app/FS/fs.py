import socket
from flask import Flask, request

app = Flask(__name__)
def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    a, b = 0, 1

    for _ in range(2, n + 1):
        a, b = b, a + b

    return b

@app.route("/register", methods=["PUT"])
def register():
    data = request.get_json()

    if data is None:
        return "Bad Request", 400

    hostname = data.get("hostname")
    ip = data.get("ip")
    as_ip = data.get("as_ip")
    as_port = data.get("as_port")

    if not all([hostname, ip, as_ip, as_port]):
        return "Bad Request", 400

    try:
        as_port = int(as_port)
    except (ValueError, TypeError):
        return "Bad Request", 400

    message = (
        "TYPE=A\n"
        f"NAME={hostname} VALUE={ip} TTL=10\n"
    )

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        udp_socket.sendto(
            message.encode(),
            (as_ip, as_port)
        )
    finally:
        udp_socket.close()

    return "Registration successful", 201

@app.route("/fibonacci", methods=["GET"])
def get_fibonacci():
    number = request.args.get("number")

    if number is None:
        return "Bad Request", 400
    try:
        number = int(number)
    except ValueError:
        return "Bad Request", 400
    if number < 0:
        return "Bad Request", 400

    result = fibonacci(number)

    return str(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)