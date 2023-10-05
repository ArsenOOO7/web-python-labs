import socket

server_data = ('localhost', 65_000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_data)

message = input("Plase enter message: ")
client.sendall(message.encode('utf-8'))
client.close()