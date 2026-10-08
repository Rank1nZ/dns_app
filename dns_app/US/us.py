import socket
import requests
from flask import Flask, request

app = Flask(__name__)
def query_authoritative_server(hostname, as_ip, as_port):
    message = (
        "TYPE=A\n"
        f"NAME={hostname}\n"
    )
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(5)

    try:
        udp_socket.sendto(
            message.encode(),
            (as_ip, as_port)
        )
        response, _ = udp_socket.recvfrom(1024)
        response = response.decode().strip()
    finally:
        udp_socket.close()

    lines = response.splitlines()
    if len(lines) < 2:
        return None

    fields = lines[1].split()

    for field in fields:
        if field.startswith("VALUE="):
            return field.split("=", 1)[1]

    return None

@app.route("/fibonacci", methods=["GET"])
def get_fibonacci():
    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Bad Request", 400
    try:
        fs_port = int(fs_port)
        as_port = int(as_port)
    except ValueError:
        return "Bad Request", 400
    try:
        fs_ip = query_authoritative_server(
            hostname,
            as_ip,
            as_port
        )
    except socket.timeout:
        return "DNS query failed", 500
    if fs_ip is None:
        return "DNS record not found", 404
    try:
        response = requests.get(
            f"http://{fs_ip}:{fs_port}/fibonacci",
            params={"number": number},
            timeout=5
        )
    except requests.RequestException:
        return "Fibonacci Server unavailable", 500
    return response.text, response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)