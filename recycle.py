import socket
import threading
import utils.logging
import handlers.misc
import handlers.http
import argparse
class relayer:
    def __init__(self,receive_host,send_host,handler,verbose=True,extra_args=()):
        self.handler = handler
        self.receive_host = receive_host[0]
        self.send_host = send_host[0]
        self.receive_port = receive_host[1]
        self.send_port = receive_host[1]
        self.verbose = verbose
        self.clients = []
        self.logger = utils.logging.logger(self.verbose)
        self.extra_args = extra_args
        

    def log(self,message):
        if self.verbose:
            print(message)
    def handle_client(self,receiver,sender,handler):
        receiver_handler = threading.Thread(target=handler,args=(receiver,sender,self.logger,self.extra_args))
        sender_handler = threading.Thread(target=handler,args=(sender,receiver,self.logger,self.extra_args))

        receiver_handler.start()
        sender_handler.start()
        
    def _start(self,recvip,recvport,sendip,sendport):
        receiver_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver_object.bind((recvip,recvport))
        self.logger.log("Binded")
        receiver_object.listen()
        while True:
            receiver,addr = receiver_object.accept()
            self.logger.log(f"Connection From : {addr[0]}")
        
            self.clients.append((receiver,addr))

            sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sender.connect((sendip,sendport))
            self.logger.log(f"Connected To : '{sendip}' on port '{sendport}'")
            self.logger.log("Handling connections...")
            self.handle_client(receiver,sender,self.handler)
    def start(self):
        self._start(self.receive_host,self.receive_port,self.send_host,self.receive_port)
def main():
    arg_parser = argparse.ArgumentParser(prog="Relayer",description="Relayer options")
    arg_parser.add_argument("--local-ip","-li",default="0.0.0.0",help="The local IP Address To listen On",metavar="lHost",type=str)
    arg_parser.add_argument("--local-port","-lp",default=80,help="The local port to listen on",required=True,metavar="lPort",type=int)
    arg_parser.add_argument("--relay-ip","-ri",help="The IP Address to relay to",required=True,metavar="rHost",type=str)
    arg_parser.add_argument("--relay-port","-rp",help="The remote port to relay to",required=True,metavar="rPort",type=int)
    
    arg_parser.add_argument("--verbose","-v",help="Display all relay messages",action="store_true",default=False)   

    handler_args = arg_parser.add_argument_group(description="Connection Handler Options")
    handler_args.add_argument("--handler","-rh",default="MISC",choices=["misc","http"])
    
    arguments = arg_parser.parse_args()
    
    lHost = arguments.local_ip
    lPort = arguments.local_port
    rHost = arguments.relay_ip
    rPort = arguments.relay_port
    handler = arguments.handler
    verbose = arguments.verbose

    extra_args = ()

    if handler.upper() == "MISC":
        handler = handlers.misc.connection_handler
        extra_args = (verbose,)
    elif handler.upper() == "HTTP":
        handler = handlers.http.connection_handler
        extra_args = (rHost,verbose)
    
    relay = relayer((lHost,lPort), (rHost,rPort),handler,extra_args=extra_args)
    relayer.start(relay)
main()
