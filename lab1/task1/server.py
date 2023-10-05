import socket
from datetime import datetime
from time import sleep

class Server:

    HOST = "localhost"
    PORT = 65_000

    def __init__(self) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((Server.HOST, Server.PORT))
        server_socket.listen(5)
        self.__serverSocket = server_socket
        print("Ready...")
        self.run()

    def run(self):
        while True:
            client_socket, addr = self.__serverSocket.accept()
            print("Client " + str(addr) + " has connected! (" + str(datetime.now()) + ")")
            while True:
                message = self.getClientMessage(client_socket)
                if(message == "Hello"):
                    self.sendMessage(client_socket, "Hello!")
                elif(message == "Stop"):
                    self.sendMessage(client_socket, "Thank you for using our services!")
                    break
                else:
                    self.sendMessage(client_socket, "Unknown command...")
            print("Client " + str(addr) + " has disconnected! (" + str(datetime.now()) + ")")
            client_socket.close()


    def sendMessage(self, client_socket: socket, message: str):
        client_socket.send(message.encode('utf-8'))

    def getClientMessage(self, client_socket: socket) -> str:
        return client_socket.recv(1024).decode('utf-8')

if(__name__ == "__main__"):
    Server()