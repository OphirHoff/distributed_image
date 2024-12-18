### client -> server ###
CLI_NUM = 'NUM'


### server -> client ###
CONN_SUCCEED = 'ACC'
REQUEST_CHUNK = 'GET'

def create_msg(code, data=''):
    
    return f"{code}~{data}" if data else code

def client_recieve_msg(msg: str):
    
    fields = msg.split('~')
    
    code = fields[0]
    data = fields[1]
    if code == CONN_SUCCEED:
        return True
    elif code == REQUEST_CHUNK:
        return data

def server_recieve_msg(msg: str):
    
    fields = msg.split('~')
    
    code = fields[0]
    
    if code == CLI_NUM:
        return int(fields[1])