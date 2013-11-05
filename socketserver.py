"""Chat server with only select."""

import select, socket, sys

class ChatServer(object):
    # TODO: Do something better than crashing when client disconnects
    def __init__(self, addr, name="server"):
        self.addr = addr
        self.name = name
        self.listener = None # listening socket
        self.clients = []
        self.rooms = set()
        self.rqueues = dict()   # Maps clients to messages they want to send
        self.wqueues = dict()   # Maps clients to messages they need to receive

    @property
    def readers(self):
        return self.clients + [self.listener]

    @property
    def writers(self):
        return [client for client in self.wqueues if self.wqueues[client]]

    # Make private?
    def make_listener(self):
        """Creates listening socket and binds it to self.addr"""
        listener = socket.socket()
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.setblocking(0)
        listener.bind(self.addr)
        return listener

    def get_msg(self, client):
        msg = client.sock.recv(10).decode()
        self.update_rqueues(client, msg)

    def update_rqueues(self, client, msg):
        """Gets messages from clients and adds them to their read queues"""
        if client in self.rqueues:
            self.rqueues[client] = "".join((self.rqueues[client], msg))
        else:
            self.rqueues[client] = msg
        print("Received", self.rqueues[client])

    def handle_request(self):
        """Handles connection requests"""
        sock, addr = self.listener.accept()
        client = Client(sock, addr)
        self.add(client)

    def add(self, client):
        self.clients.append(client)
        self.wqueues[client] = "" #"Server: Welcome, {}!\n".format(client.name)
        print("{} has connected.".format(client.name))

    def dispatch_msgs(self):
        # Moves new message in the read queues to the proper write queues
        # Currently only supports broadcasts
        for sender, msg in list(self.rqueues.items()): # Hackish?
            for receiver in self.clients:
                if receiver is not sender:
                    self.wqueues[receiver] += msg
            self.rqueues.pop(sender)    # Should rqueues be modified during iteration?

    def start(self):
        self.listener = self.make_listener()
        self.listener.listen(5)
        print("Listening on {}:{}...".format(*self.addr))

        # Main event loop
        while True:
            # Determine whom to send queued messages to
            self.dispatch_msgs()
            rlist, wlist, _ = select.select(self.readers, self.writers, [])

            for rclient in rlist:
                if rclient is self.listener:
                    # Listener received connection request
                    self.handle_request()
                else:
                    # Someone is sending a message
                    self.get_msg(rclient)

            for wclient in wlist:
                # Send as much of the first queued message as possible; add the
                # remaining back to the read queue
                if self.wqueues[wclient]:
                    next_msg = self.wqueues[wclient]
                    amt_sent = wclient.sock.send(next_msg.encode())
                    self.wqueues[wclient] = next_msg[amt_sent:]

    def remove(self, client):
        client.sock.close()
        self.clients.remove(client)
        self.wqueues.pop(clients, None)


class Room(object):
    def __init__(self, name):
        self.name = name
        self.clients = set()

    # def add_client(self):
    #     pass

    def kick_client(self):
        pass


class Client(object):
    def __init__(self, sock, addr, name="anon"):
        self.sock = sock
        self.addr = addr
        self.name = name
        self.room = None

    def set_name(self, name):
        self.name = name

    def join_room(self, room):
        room.clients.add(self)
        self.rooms.add(room)

    def leave_room(self, room):
        room.clients.remove(self)
        self.rooms.remove(room)

    def fileno(self):
        return self.sock.fileno()


def main():
    """
    Run the server
    """
    addr = ('127.0.0.1', 8000)

    server = ChatServer(addr)
    server.start()

if __name__ == '__main__':
    main()
