import socket
import json

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 1236))
    server_socket.listen(1)
    print("Server listening on port 1234")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} established")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            heartrate = data.decode('utf-8')
            print(f"Received heart rate: {heartrate}")
            write_variable(heartrate)
        client_socket.close()

def write_variable(heartrate):
    with open("shared_data.json", "w") as f:
        json.dump({"hr": heartrate}, f) 

if __name__ == "__main__":
    start_server()
