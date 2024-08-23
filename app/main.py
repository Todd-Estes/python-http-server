import socket
import io

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, address = server_socket.accept()

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
      print("in header loop")
      line = request_file.readline().decode('utf-8').strip()
      if not line: break
      header_key, header_value = line.split(': ')
      request_headers[header_key] = header_value


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