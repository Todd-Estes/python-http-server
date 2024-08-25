import socket
import threading

def handle_client(client_socket):
    # Create a file-like object from the socket
    request_file = client_socket.makefile('rb')

    request_line = request_file.readline().decode('utf-8').strip() # Decode the bytes to a string

    print(f"REQUEST LINE {request_line}")
    method, request_target, _ = request_line.split(' ') # Split the request line
    print(f"Request Method: {method}")
    print(f"Request Target: {request_target}")

    # create request headers hash
    request_headers = {}
    while True:
      line = request_file.readline().decode('utf-8').strip()
      if not line: break
      header_key, header_value = line.split(': ')
      request_headers[header_key] = header_value

    if request_target == "/":
      client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n") # .encode() at end of string acts same as 'b' prefix
    elif request_target == "/user-agent":
      response_body = request_headers["User-Agent"]
      content_length = len(response_body.encode())
      response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{response_body}".encode()
      client_socket.sendall(response)
    elif request_target.split("/")[1:][0] == "echo":
      return_string = request_target.split("/")[1:][1]
      content_length = len(return_string.encode())
      response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{return_string}".encode()
      client_socket.sendall(response)
    else:
      client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    
    client_socket.close()

def run_server():
  print("Logs from your program will appear here!")
  server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
  print("Server is running on port 4221...")

  while True:
    client_socket, address = server_socket.accept()
    print(f"Accepted connection from {address}")

    # Create a new thread for each client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

if __name__ == "__main__":
  run_server()