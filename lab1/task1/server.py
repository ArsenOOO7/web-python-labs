import socket
from datetime import datetime

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 65_000
server_socket.bind((host, port))
server_socket.listen(5)

print("Ready...")
client_socket, addr = server_socket.accept()
message = client_socket.recv(1024)
decoded_message = message.decode("utf-8")
print("Message \"" + decoded_message + "\" at " + str(datetime.now()))
server_socket.close()