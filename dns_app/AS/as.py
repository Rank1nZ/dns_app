import socket
AS_IP = "0.0.0.0"
AS_PORT = 53533
DNS_FILE = "dns_records.txt"

def save_record(name, value, ttl):
    with open(DNS_FILE, "w") as file:
        file.write(f"TYPE=A\n")
        file.write(f"NAME={name} VALUE={value} TTL={ttl}\n")

def read_record(name):
    try:
        with open(DNS_FILE, "r") as file:
            lines = file.readlines()

        if len(lines) < 2:
            return None
        record = lines[1].strip().split()
        saved_name = record[0].split("=")[1]
        saved_value = record[1].split("=")[1]
        saved_ttl = record[2].split("=")[1]

        if saved_name == name:
            return saved_value, saved_ttl

    except FileNotFoundError:
        return None
    return None

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((AS_IP, AS_PORT))

    print(f"Authoritative Server is running on UDP port {AS_PORT}")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        message = data.decode().strip()

        print(f"Received from {client_address}:")
        print(message)

        lines = message.splitlines()

        if len(lines) < 2:
            continue

        if "VALUE=" in lines[1] and "TTL=" in lines[1]:
            fields = lines[1].split()
            name = fields[0].split("=")[1]
            value = fields[1].split("=")[1]
            ttl = fields[2].split("=")[1]

            save_record(name, value, ttl)

            print(f"Registered: {name} -> {value}")

        else:
            name = lines[1].split("=")[1]
            record = read_record(name)

            if record is not None:
                value, ttl = record

                response = (
                    "TYPE=A\n"
                    f"NAME={name} VALUE={value} TTL={ttl}"
                )

                server_socket.sendto(
                    response.encode(),
                    client_address
                )

                print(f"DNS response sent: {name} -> {value}")

if __name__ == "__main__":
    main()