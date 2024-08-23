import socket
import sys

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_socket, address = server_socket.accept()
        print(f"Client connected from {address}")
        data = client_socket.recv(4096)
        request_line = data.split(b'\r\n')[0].decode('utf-8') # Decode the bytes to a string
        method, request_target, _ = request_line.split(' ') # Split the request line


        if request_target == "/":
          client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n") # .encode() at end of string acts same as 'b' prefix
        elif request_target.split("/")[1:][0] == "echo":

          return_string = request_target.split("/")[1:][1]
          content_length = len(return_string.encode())
          response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{return_string}".encode()
          client_socket.sendall(response)
        else:
          client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

if __name__ == "__main__":
    main()