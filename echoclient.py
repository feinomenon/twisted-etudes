from twisted.internet import protocol, reactor

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write("Hello, world!")
        self.getMsg()

    def dataReceived(self, data):
        print "Server said:", data
        # self.transport.loseConnection()

    def getMsg(self):
        msg = raw_input("Enter message: \n")
        print "Sending msg"
        self.transport.write(msg)
        # self.getMsg() # ???

class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed."
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost."
        reactor.stop()

# Creates instance of EchoFactory upon connection
reactor.connectTCP("localhost", 8000, EchoFactory())

reactor.run()