import numpy as np
import socket
import pickle
import error_msg
import sys


PORT = 1234

class Client:
    def __init__(self):
        self.sock = socket.socket()
        self.port = PORT
        
    def init_connection(self, ip):
        try:
            self.sock.connect((ip, PORT))
        except socket.timeout:
            error_msg.ErrorMsg.connect_timeout(ip, PORT)
            



class Square:
    def __init__(self, array, x, y):
        self.array = array
        self.x = x #x coordinate of left corner
        self.y = y #y coordinate of left corner
        
    def PartOfSquare(self, xi, yi, xf, yf):
        pass
        
        
def main(server_ip):
    client = Client()
    client.init_connection(server_ip)

if __name__ == "__main__":

    
    if len(sys.argv) > 1:
        main(sys.argv[1])
    print("Missing an argument. Should be like so: <script_name> <server_ip>")
    