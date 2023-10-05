import socket
from datetime import datetime
from time import sleep

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 65_000
server_socket.bind((host, port))
server_socket.listen(5)

print("Ready...")
client_socket, addr = server_socket.accept()
message = client_socket.recv(1024)
decoded_message = message.decode("utf-8")
print("Received message \"" + decoded_message + "\" at " + str(datetime.now()))

sleep(5)
received_bytes = client_socket.send(message)
if(received_bytes == len(decoded_message)):
    print("Everything's good")
else:
    print("Something went wrong...")

server_socket.close()