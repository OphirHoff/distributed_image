import socket
import pickle
import error_msg
import tcp_by_size
import protocol
import random
import numpy as np
import threading
from graphics import ImageLoad, Graphics

IP = '0.0.0.0'
PORT = 1234
CLIENTS_NUM = 4
PIECE_SIZE_X = 50
PIECE_SIZE_Y = 50
IMG_SIZE_X = 200
IMG_SIZE_Y = 200

X = 0
Y = 1




def where_is_point(point: tuple[int, int]):
    
    x, y = point
    if x <= IMG_SIZE_X / 2 and y <= IMG_SIZE_Y / 2:
        return 1
    elif x > IMG_SIZE_X / 2 and y <= IMG_SIZE_Y / 2:
        return 2
    elif x > IMG_SIZE_X / 2 and y > IMG_SIZE_X / 2:
        return 3
    elif x <= IMG_SIZE_X / 2 and y > IMG_SIZE_X / 2:
        return 4


def area1(start: tuple[int, int], end: tuple[int, int], start_area, end_area) -> tuple[tuple[int, int], tuple[int, int]] | bool:


    if start_area != 1:
        return False
    
    if end_area == 1:
        return start, end
    if end_area == 2:
        return start, (int(IMG_SIZE_X / 2), end[Y])
    if end_area == 3:
        return start, (int(IMG_SIZE_X / 2), int(IMG_SIZE_Y / 2))
    if end_area == 4:
        return start, (end[X], int(IMG_SIZE_Y / 2))


def area2(start: tuple[int, int], end: tuple[int, int], start_area, end_area) -> tuple[tuple[int, int], tuple[int, int]] | bool:

    if start_area == 1:
        if end_area == 2:   
            return (int(IMG_SIZE_X / 2) + 1, start[Y]), end
        elif end_area == 3:
            return (int(IMG_SIZE_X / 2) + 1, start[Y]), (end[X], int(IMG_SIZE_Y / 2))
    elif start_area == 2:
        if end_area == 2:
            return start, end
        elif end_area == 3:
            return start, (end[X], int(IMG_SIZE_Y / 2) + 1)
    return False
    

def area3(start: tuple[int, int], end: tuple[int, int], start_area, end_area) -> tuple[tuple[int, int], tuple[int, int]] | bool:

    if start_area == 1:
        if end_area == 3:
            return (int(IMG_SIZE_X / 2) + 1, int(IMG_SIZE_Y / 2) + 1), end
    elif start_area == 2:
        if end_area == 3:
            return (start[X], int(IMG_SIZE_Y / 2) + 1), end
    elif start_area == 3:
        return start, end
    elif start_area == 4:
        if end_area == 3:
            return (int(IMG_SIZE_X / 2) + 1, start[Y]), end
        
    return False


def area4(start: tuple[int, int], end: tuple[int, int], start_area, end_area) -> tuple[tuple[int, int], tuple[int, int]] | bool:
    
    if start_area == 2 or start_area == 3:
        return False
    if start_area == 1:
        if end_area == 3:
            return (int(IMG_SIZE_X / 2), int(IMG_SIZE_Y / 2) + 1), (start[X], end[Y])
        if end_area == 4:
            return (start[X], int(IMG_SIZE_Y / 2) + 1)
    if start_area == 4:
        if end_area == 3:
            return start, (int(IMG_SIZE_X / 2), end[Y])
        if end_area == 4:
            return start, end

    return False


funcs = [func[1] for func in globals().items() if 'area' in func[0]]

class Server:
    
    def __init__(self) -> None:
        self.sock = socket.socket()
        self.port = PORT
        self.clients: dict[int:tuple[socket.socket, str]] = {}
    
    
    def initialize_connection(self):
        self.sock.bind((IP, PORT))
        self.sock.listen(4)
        self.sock.settimeout(10)
        
        try:
            while len(self.clients) < CLIENTS_NUM:
                
                
                    print("Server: waiting for clients")
                    client_sock, addr = self.sock.accept()
                    client_num = protocol.server_recieve_msg(tcp_by_size.recv_by_size(client_sock))
                    if not client_num:
                        raise error_msg.ErrorMsg.connection_error(addr[0], addr[1])
                    # Check that recieved num is in range
                    if client_num <= CLIENTS_NUM and client_num > 0:
                        # Send connection acception
                        tcp_by_size.send_with_size(client_sock, protocol.create_msg(protocol.CONN_SUCCEED))
                        self.clients[client_num] = (client_sock, addr)
                        print(f"New client connected num: {client_num}.\nActive clients: {len(self.clients)}")
                
        except socket.timeout:
            error_msg.ErrorMsg.connect_timeout(addr[0], addr[1])
            return

        print("Connected to all clients successfully.")
            

    def get_window(self, start_point: tuple[int ,int], end_point: tuple[int, int]):

        start_area = where_is_point(start_point)
        end_area = where_is_point(end_point)

        pieces = []
        cli_num = 1

        for func in funcs:  # Call the 'area' functions
            if cli_num > CLIENTS_NUM:
                break

            d = func(start_point, end_point, start_area, end_area)
            if not d:
                cli_num += 1
                pieces.append(False)
                continue
            curr_start_point, curr_end_point = d
            curr_client_sock: socket.socket = self.clients[cli_num][0]
            tcp_by_size.send_with_size(curr_client_sock, protocol.create_msg(protocol.REQUEST_CHUNK, str(curr_start_point[0]), str(curr_start_point[1]), str(curr_end_point[0]), str(curr_end_point[1])))
            response = protocol.server_recieve_msg(tcp_by_size.recv_by_size(curr_client_sock)) # recieve pickled object
            response = eval(response)
            data = pickle.loads(response)
            pieces.append(ImageLoad.img_pillow_from_arr(data))
            cli_num += 1

        return pieces


    def main(self):

        self.initialize_connection()
        
        # Grill random start point on screen
        # start_point = random.randint(0, IMG_SIZE_X - 1), random.randint(0, IMG_SIZE_Y - 1)
        # end_point = (start_point[X] + PIECE_SIZE_X, start_point[Y] + PIECE_SIZE_Y)

        graphics = Graphics()
        graphics_thread = threading.Thread(target=graphics.start)
        graphics.pieces = self.get_window(graphics.start_pos, graphics.end_pos)
        graphics_thread.start()
        print("started graphics")

        while True:

            graphics.pieces = self.get_window(graphics.start_pos, graphics.end_pos)


if __name__ == "__main__":
    server = Server()
    server.main()