"""
Chat server without Twisted.
"""

import select, socket, sys

class ChatServer():
    def __init__(self, listener, name = "server"):
        self.listener = listener # listening socket
        self.name = name
        self.socks = [self.listener]
        self.rooms = []

    def start(self):
        while True:
            rlist, wlist, _ = select.select(self.socks, self.socks[1:], [])
                
            for sock in rlist:
                if sock is self.listener:
                    # Listener received connection request
                    client, (ip, port) = sock.accept() # Can this be an existing client?
                    self.socks.append(client)
                    print("{} has connected.".format(ip))
                else:
                    msg = self.get_msg(sock)
                    self.send_msg(sock, msg, wlist)
    
    def get_msg(self, sock):
        cache = []

        while True:
            msg = sock.recv(10)
            if not msg:
                self.remove(sock)
                break
            else:
                cache.append(str(msg))
                print("".join(cache))
                if msg.endswith("\n"):
                    break

        return "".join(cache)

    def send_msg(self, sender, msg, wlist): # sender = socket
        print("Client says:", msg)
        for sock in wlist:
            if sock is not sender:
                sock.sendall(msg)

    def remove(self, sock):
        sock.close()
        self.socks.remove(sock)


def main():
    addr = ('127.0.0.1', 8000)

    # Create listening socket
    listener = socket.socket()
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.setblocking(0)
    listener.bind(addr)
    listener.listen(5)

    print("Listening at", addr)

    server = ChatServer(listener)
    server.start()

if __name__ == '__main__':
    main()