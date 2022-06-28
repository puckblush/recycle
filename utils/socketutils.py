def receive_all(connection,bufsize=4096):
        full = b""
        while True:
            data = connection.recv(bufsize)
            full += data
            if len(data) < bufsize:
                break
        return full
