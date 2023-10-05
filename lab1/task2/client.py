import threading
import socket


class Client:

    SERVER_HOST = "localhost"
    SERVER_PORT = 65_000

    def __init__(self, name) -> None:
        self.__name = name
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
    
    def connect(self):
        self.__client.connect((Client.SERVER_HOST, Client.SERVER_PORT))
        self.__client.send(self.__name.encode("utf-8"))
        self.runThreads()
    
    def disconnect(self):
        self.__client.close()

    def runThreads(self):
        send_thread = threading.Thread(target=self.send)
        recv_thread = threading.Thread(target=self.recv)
        send_thread.start()
        recv_thread.start()

    def send(self):
        while True:
            message = input("")
            self.__client.send(message.encode('utf-8'))

    def recv(self):
        while True:
            received_message = self.__client.recv(1024).decode('utf-8')
            print(received_message)

if(__name__ == "__main__"):
    Client(input("Enter your name: "))