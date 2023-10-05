import socket

class Client:

    SERVER_HOST = "localhost"
    SERVER_PORT = 65_000

    def __init__(self) -> None:
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
    
    def connect(self):
        self.__client.connect((Client.SERVER_HOST, Client.SERVER_PORT))
        self.run()
    
    def disconnect(self):
        self.__client.close()

    def run(self):
        while True:
            message = input("Please enter message: ")
            self.__client.sendall(message.encode('utf-8'))
            response = self.__client.recv(1024)
            print("Received message from server: " + response.decode("utf-8"))
            if(message == "Stop"):
                break
        self.disconnect()

if(__name__ == "__main__"):
    Client()