import socket

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    try:
        client_socket, address = server_socket.accept()
        print(f"Client connected from {address}")
        # client.send('THank you'.encode())
        client_socket.sendall(b"HTTP/1.0 200 OK\r\n\r\n")

    except KeyboardInterrupt:
        print("Server stopped")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()