import utils.socketutils
def connection_handler(fromSocket,toSocket,logger,extra_arguments):
        verbose = extra_arguments[0]
        while True:
            data = utils.socketutils.receive_all(fromSocket)
            if data != b'':
                print(f"[MISC] Received Data; Length : {len(data)}")
                if verbose:
                        logger.log(data)
                toSocket.send(data)
