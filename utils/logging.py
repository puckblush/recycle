class logger:
    def __init__(self,isactive):
        self.isactive = isactive
    def log(self,message):
        if self.isactive:
            print(message)
    def log_http_message(self,message):
        for line in message.split(b"\r\n"):
            print(line)
