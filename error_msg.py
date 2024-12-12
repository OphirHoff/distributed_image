class ErrorMsg:
    
    def connect_timeout(ip: str, port: int):
        print(f"""Connection Timeout: Could not connect to client: ({ip}, {port})""")