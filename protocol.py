### client -> server ###
CLI_NUM = 'NUM'
SEND_SQUARE = 'SQR'

### server -> client ###
CONN_SUCCEED = 'ACC'
REQUEST_CHUNK = 'GET'

def create_msg(code, *args, data=''):

    if not args:
        return f"{code}~{data}" if data else code
    
    to_return = f"{code}"
    for x in args:
        to_return += f"~{str(x)}"
        
    print(to_return)
    return to_return


def client_recieve_msg(msg: str):
    
    fields = msg.split('~')
    
    code = fields[0]
    if code == CONN_SUCCEED:
        return True
    elif code == REQUEST_CHUNK:
        start_point = (int(fields[1]), int(fields[2]))
        end_point = (int(fields[3]), int(fields[4]))
        return start_point, end_point
        

def server_recieve_msg(msg: str):

    fields = msg.split('~')
    
    code = fields[0]
    
    if code == CLI_NUM:
        return int(fields[1])
    
    elif code == SEND_SQUARE:
        return fields[1]