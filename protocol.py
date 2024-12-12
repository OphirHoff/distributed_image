### client -> server ###
CLI_NUM = 'NUM'


### server -> client ###
CONN_SUCCEED = 'ACC'

def create_msg(data='', code):
    
    return f"{code}~{data}" 

def client_recieve_msg(msg: str):
    
    fields = msg.split('~')
    
    code = fields[0]
    
    if code == CONN_SUCCEED:
        return int(fields[1])