import socket
import pickle
import error_msg

IP = '0.0.0.0'
PORT = 1234
CLIENTS_NUM = 1


class Server:
    
    def __init__(self) -> None:
        self.sock = socket.socket()
        self.port = PORT
        self.clients: list[tuple[socket.socket, str]] = []
    
    
    def initialize_connection(self):
        self.sock.bind((IP, PORT))
        self.sock.listen(4)
        self.sock.settimeout(5)
        
        while len(self.clients) < CLIENTS_NUM:
            
            try:
                sock, addr = self.sock.accept()
                self.clients.append((sock, addr))
                print(f"New client connectd.\nActive clients: {self.clients}")
            except socket.timeout:
                error_msg.ErrorMsg.connect_timeout(addr[0], addr[1])
                return

        print("Connected to all clients successfully.")
            

    def main(self):
        self.initialize_connection()
    


if __name__ == "__main__":
    server = Server()
    server.main()