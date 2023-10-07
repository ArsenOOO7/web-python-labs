import threading
import socket
from datetime import datetime

class Server:

    HOST = "localhost"
    PORT = 65_000

    def __init__(self) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((Server.HOST, Server.PORT))
        server_socket.listen(5)
        self.__serverSocket = server_socket
        self.__clients = []
        print("Chat room is ready...")
        self.listener()
    
    def getServerSocket(self):
        return self.__serverSocket
    
    def addClient(self, client):
            self.__clients.append(client)
            self.broadcast(Formatter.welcomeMessage(client.getName()))
            threading.Thread(target=self.handle, args=(client,)).start()

    def handle(self, client):
        client_socket = client.getClientSocket()
        client_name = client.getName();
        while True:
            client_message = client_socket.recv(1024).decode('utf-8')
            if client_message:
                if len(client_message.strip()) > 0:
                    self.broadcast(Formatter.formatMessage(client_name, client_message))
            else:
                self.broadcast(Formatter.exitMessage(client_name))
                self.removeClient(client)
                client_socket.close()
                print(str(datetime.now()) + " User left: " + client_name)
                break

    def listener(self):
        while True:
            try:
                client_socket, addr = self.__serverSocket.accept()
                name = client_socket.recv(1024).decode('utf-8')
                clientObj = Client(client_socket, addr, name)
                self.addClient(clientObj)
                print(str(datetime.now()) + " New user: " + name)
            except:
                self.__serverSocket.close()
                break
    
    def removeClient(self, client):
            self.__clients.remove(client)
    
    def broadcast(self, message):
        print(message)
        for client in self.__clients:
            client.sendMessage(message)

class Client:
    def __init__(self, client_socket, addr, name) -> None:
        self.__client_socket = client_socket
        self.__addr = addr
        self.__name = name

    def getClientSocket(self) -> socket:
        return self.__client_socket
    
    def getAddr(self) -> tuple:
        return self.__addr
    
    def getName(self) -> str:
        return self.__name
    
    def sendMessage(self, message: str):
        self.__client_socket.send(message.encode('utf-8'))

    def disconnect(self):
        self.__client_socket.disconnect()

class Formatter:

    MESSAGE_TEMPLATE = "({0}): {1}"
    GREETINGS_TEMPLATE = "Welcome, {0}"
    EXIT_TEMPLATE = "Goodbye, {0}"

    @staticmethod
    def formatMessage(sender_name: str, message: str):
        return Formatter.MESSAGE_TEMPLATE.format(sender_name, message)

    @staticmethod
    def welcomeMessage(client_name: str):
        return Formatter.GREETINGS_TEMPLATE.format(client_name)

    @staticmethod
    def exitMessage(client_name: str):
        return Formatter.EXIT_TEMPLATE.format(client_name)

if(__name__ == "__main__"):
    Server()
