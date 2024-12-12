import socket
import pickle
import error_msg
import tcp_by_size
import protocol

IP = '0.0.0.0'
PORT = 1234
CLIENTS_NUM = 1


class Server:
    
    def __init__(self) -> None:
        self.sock = socket.socket()
        self.port = PORT
        self.clients: dict[int:tuple[socket.socket, str]] = []
    
    
    def initialize_connection(self):
        self.sock.bind((IP, PORT))
        self.sock.listen(4)
        self.sock.settimeout(5)
        
        while len(self.clients) < CLIENTS_NUM:
            
            try:
                client_sock, addr = self.sock.accept()
                client_num = protocol.server_recieve_msg(tcp_by_size.recv_by_size(client_sock))
                print(client_num)
                # Check that recieved num is in range
                if client_num <= CLIENTS_NUM and client_num > 0:
                    # Send connection acception
                    tcp_by_size.send_with_size(client_sock, protocol.create_msg(protocol.CONN_SUCCEED))
                self.clients.append((client_sock, addr))
                print(f"New client connected num: {client_num}.\nActive clients: {self.clients}")
            except socket.timeout:
                error_msg.ErrorMsg.connect_timeout(addr[0], addr[1])
                return

        print("Connected to all clients successfully.")
            

    def main(self):
        self.initialize_connection()
    


if __name__ == "__main__":
    server = Server()
    server.main()