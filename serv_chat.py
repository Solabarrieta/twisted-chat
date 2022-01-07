#!/usr/bin/env python3

from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

MAX_USERS = 100
MAX_MSG_LENGTH = 255
MAX_USER_LENGTH = 16
PORT = 8000


class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None

    def connectionMade(self):
        self.sendLine("FTR0 0 0 0".encode())
        usarios = "USR" + " ".join(self.factory.users.keys())
        self.sendLine(usuarios.encode())

    def connectionLost(self, reason):
        del self.factory.users[self.name]
        self.broadcast("OUT"+self.name)

    def lineReceived(self, line):
        mensaje = line.decode()

        if mensaje[:3] == 'NME' and not self.name:
            self.name = mensaje[3:]
            self.factory.users[self.name] = self
            self.sendLine(b"+")
            self.broadcast("INN"+self.name)
        elif mensaje[:3] == 'MSG':
            self.broadcast("MSG")


def broadcast(self, line):
    for protocol in self.factory.users.values():
        if protocol != self:
            protocol.sendLine(line.encode())


class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)


if __name__ == "__main__":
    reactor.listenTCP(PORT, ChatFactory())
    reactor.run()
