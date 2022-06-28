import utils.socketutils
verbs = [b"GET",b"POST",b"PUT",b"OPTIONS",b"PATCH",b"DELETE"]
global constant_host
constant_host = None
def identify_http(message):
    for verb in verbs:
        if message.startswith(verb + b" "):
            return "HTTP_REQ"
    return "HTTP_REP"
def get_host(message):
    global constant_host
    for line in message.split(b"\r\n"):
        if line.startswith(b"Host:"):
            stored_host = line.split(b"Host:")[1].strip()
            if not constant_host:
                constant_host = stored_host
            return stored_host
    return None
def get_info(data):
    data = data.split(b"\r\n")[0]
    verb = data.split(b" ")[0]
    path = data.split(b" ")[1]
    return verb,path
def replace_host(data,newhost):
    old_host = get_host(data) 
    if old_host != None:
        new_message = data.replace(old_host,newhost)
        return new_message
    else:
        return data
    
def replace_urls(data,old_host):
    global constant_host
    return data.replace(old_host,constant_host)
    
def connection_handler(fromSocket,toSocket,logger,extra_arguments):
        host = extra_arguments[0]
        verbose = extra_arguments[1]
        while True:
            data = utils.socketutils.receive_all(fromSocket)
            if data != b'':
                logger.log(f"[HTTP] Received Data")
                msg_type = identify_http(data)
                print(f"[HTTP] Type : {msg_type}")
                if msg_type == "HTTP_REQ":
                    data = replace_host(data,host.encode())
                    verb,path = get_info(data)
                    print(f"[HTTP] {verb.decode()} {path.decode()}")
                    print("[HTTP] Modified Message")
                elif msg_type == "HTTP_REP":
                    data = replace_urls(data,host.encode())
                    print("[HTTP] Modified Response")
                if verbose:
                    logger.log_http_message(data)
                toSocket.send(data)
