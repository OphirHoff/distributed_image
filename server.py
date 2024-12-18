import socket
import pickle
import error_msg
import tcp_by_size
import protocol
import random

IP = '0.0.0.0'
PORT = 1234
CLIENTS_NUM = 2
PIECE_SIZE_X = 50
PIECE_SIZE_Y = 50
IMG_SIZE_X = 200
IMG_SIZE_Y = 200

def where_is_point(x, y):
    if x < IMG_SIZE_X / 2 and y < IMG_SIZE_Y / 2:
        return 1
    elif x > IMG_SIZE_X / 2 and y < IMG_SIZE_Y / 2:
        return 2
    elif x > IMG_SIZE_X / 2 and y > IMG_SIZE_X / 2:
        return 3
    elif x < IMG_SIZE_X / 2 and y > IMG_SIZE_X / 2:
        return 4


class Server:
    
    def __init__(self) -> None:
        self.sock = socket.socket()
        self.port = PORT
        self.clients: dict[int:tuple[socket.socket, str]] = []
    
    
    def initialize_connection(self):
        self.sock.bind((IP, PORT))
        self.sock.listen(4)
        self.sock.settimeout(10)
        
        while len(self.clients) < CLIENTS_NUM:
            
            try:
                print("Server: waiting for clients")
                client_sock, addr = self.sock.accept()
                client_num = protocol.server_recieve_msg(tcp_by_size.recv_by_size(client_sock))
                if not client_num:
                    raise error_msg.ErrorMsg.connection_error(addr[0], addr[1])
                # Check that recieved num is in range
                if client_num <= CLIENTS_NUM and client_num > 0:
                    # Send connection acception
                    tcp_by_size.send_with_size(client_sock, protocol.create_msg(protocol.CONN_SUCCEED))
                    self.clients.append((client_sock, addr))
                    print(f"New client connected num: {client_num}.\nActive clients: {len(self.clients)}")
                
            except socket.timeout:
                error_msg.ErrorMsg.connect_timeout(addr[0], addr[1])
                return

        print("Connected to all clients successfully.")
            
    def point_in_area_1(self, end_point) -> tuple[tuple[int, int], tuple[int, int]]:
        
        print("Reached area 1")

        pass
    def point_in_area_2(self):
        pass
    def point_in_area_3(self):
        pass
    def point_in_area_4(self):
        pass

    def get_piece(self, coords, size: tuple[int, int]=(PIECE_SIZE_X, PIECE_SIZE_Y)):

        x, y = coords
        point_area = where_is_point(x, y)
        globals()[f'point_in_area_{point_area}']()

    def main(self, server):
        self.initialize_connection()

        while True:

            coords: tuple[int, int] = random.randint(0, 200), random.randint(0, 200)
            

if __name__ == "__main__":
    server = Server()
    server.main(server)