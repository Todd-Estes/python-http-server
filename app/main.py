import socket

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
      try:
          client_socket, address = server_socket.accept()
          print(f"Client connected from {address}")
          data = client_socket.recv(4096)
          # Decode the bytes to a string
          request_line = data.split(b'\r\n')[0].decode('utf-8')
          # Split the request line
          method, request_target, _ = request_line.split(' ')

          if request_target == "/":
            client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n") # .encode() at end of string acts same as 'b' prefix
          else:
            client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

      except KeyboardInterrupt:
          print("Server stopped")
      finally:
          server_socket.close()

if __name__ == "__main__":
    main()