from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
# from twisted.words.protocols import irc

# import sys

class EchoServer(Protocol):
    def dataReceived(self, data):
        print "Received msg: %s" % (data)
        self.transport.write("Client said: " + data)

    def connectionMade(self):
        self.transport.write("[Insert swag here]")

# def confirm():
#     print "Reactor running."

def main():
    # reactor.callWhenRunning(confirm)
    f = Factory()
    f.protocol = EchoServer
    reactor.listenTCP(8000, f)
    reactor.run()

if __name__ == "__main__":
    main()
