import numpy as np
from graphics import ImageLoad
import socket
import tcp_by_size, protocol
import pickle
import error_msg
import loadImage
import sys

PORT = 1234
PIC_NAME = "pic.jpg"
PORTION_SIZE = 100


client_start_pos = {
    1: (0, 0),
    2: (100, 0),
    3: (100, 100),
    4: (0, 100)
}

class Client:
    def __init__(self, client_num):
        self.client_num = client_num
        self.sock = socket.socket()
        self.port = PORT
        
    def init_connection(self, server_ip):
        """Initialize connection with server."""
        try:
            self.sock.connect((server_ip, PORT))
            tcp_by_size.send_with_size(self.sock, protocol.create_msg(protocol.CLI_NUM, data=self.client_num))
            response = protocol.client_recieve_msg(tcp_by_size.recv_by_size(self.sock))
            if not response:
                error_msg.ErrorMsg.connection_error(server_ip, PORT)
            else:
                print(f"Connection to server succeeded (addr.: {server_ip}, {PORT}). Waiting for requests.")
            
        except socket.timeout:
            error_msg.ErrorMsg.connect_timeout(server_ip, PORT)

    def Handle_request(request):
        """Handle server's request and respond with proper data."""
        pass
        
def partOfSquare(array, start_coord: tuple[int, int], end_coord: tuple[int, int]):
    """Cut the right area from picture."""
    size_of_squarex = end_coord[0] - start_coord[0]
    size_of_squarey = end_coord[1] - start_coord[1]
    newsquare = array[start_coord[0]:start_coord[0] + size_of_squarex, start_coord[1]:start_coord[1] + size_of_squarey]
    return newsquare

class Square:
    def __init__(self, array: np.array, start_pos: tuple[int, int]):
        self.array: np.array = partOfSquare(array, start_pos, (start_pos[0] + PORTION_SIZE, start_pos[1] + PORTION_SIZE))
        self.start_pos = start_pos
     

def main(server_ip, client_num: int):
    """
    Main function:
    1. Load image/data
    2. Create connection
    3. Wait & respond for server requests
    """
    try:
        client_num = int(client_num)
    except:
        print("Client num must be an integer between 1-4.")
        exit(1)

    # Open image and load using loadImage module
    img_data = ImageLoad.load_pic_arr(PIC_NAME)
    square = Square(img_data, client_start_pos[client_num])

    # Connect to server
    client = Client(client_num)
    client.init_connection(server_ip)

    
    while True:
        # Wait for server request
        request = protocol.client_recieve_msg(tcp_by_size.recv_by_size(client.sock))

        # Cut requested area
        area = partOfSquare(square.array, request[0], request[1])
        # Use pickle for transferring
        pickled_data = pickle.dumps(area)

        # Send to Server
        tcp_by_size.send_with_size(client.sock, protocol.create_msg(protocol.SEND_SQUARE, data=pickled_data))

if __name__ == "__main__":    
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Missing an argument(s). Should be like so: <script_name> <server_ip> <client_num>")
    