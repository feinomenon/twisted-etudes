from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.task import LoopingCall
from twisted.protocols.basic import LineReceiver

class ChatServer(LineReceiver):
    def __init__(self, factory, addr):
        self.factory = factory
        self.addr = addr
        self.username = None

    def connectionMade(self):
        # self.peer = self.transport.getPeer()
        print "Current users: "
        self.sendLine("What is your name?")

    def lineReceived(self, line):
        print "Received msg: %s" % (line)
        if not self.username:
            self.username = line
            self.factory.clients[self] = self.username
            self.sendLine("Hey " + self.username)
        else:
            for client in self.factory.clients:
                if client != self:
                    client.sendLine(line)

    def connectionLost(self, reason):
        del self.factory.clients[self]
        for client in self.factory.clients:
            client.sendLine("%s has left." % (self.addr))

class ChatFactory(Factory):
    def __init__(self):
        self.clients = dict()

    def buildProtocol(self, addr):
        print "%s wants to connect!" % (addr.host)
        return ChatServer(self, addr)


def main():
    reactor.listenTCP(8000, ChatFactory())
    print "Listening on port 8000..."
    reactor.run()

if __name__ == "__main__":
    main()
