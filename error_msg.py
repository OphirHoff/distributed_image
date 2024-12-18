class ErrorMsg:
    
    def connect_timeout(ip: str, port: int):
        print(f"""Connection Timeout: Could not connect to: ({ip}, {port})""")

    def connection_error(ip: str, port: int):
        print(f"""Connection Error. Could not communicate with ({ip}, {port}).""")

    def invalid_point(x, y):
        print(f"Invalid point coordinates ({x}, {y}).")