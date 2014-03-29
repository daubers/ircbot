from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
from config import Config
from os.path import join, expanduser
from matt_alert import MailAlert
import sys


class IrcBot(irc.IRCClient):
    """
        Simple irc bot
    """
    def __init__(self):
        self.nickname = "MattBot"
        self.cfg = Config(join(expanduser("~", ".matt_alert")))
        #self.cfg = Config("test_config")
        self.mail = MailAlert()

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

        self.mail.send("IRC Connection Made")

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.mail.send("Connection Lost")

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def privmsg(self, user, channel, message):
        """
            Recieved a private message
        """
        user = user.split('!', 1)[0]
        # Check to see if they're sending me a private message
        for nick in self.cfg.getoption("nicknames"):
            if message.find(nick) > -1:
                self.mail.send("Nickname " + nick + " Mentioned by "+ user + " in channel " + channel + "\n" + message)

        if channel == self.nickname:
            self.mail.send("PM Recieved From " + user + " - " + message)
            self.msg(user, self.cfg.getoption("pm_reply"))

        # Otherwise check to see if it is a message directed at me
        if message.find(self.nickname) > -1:
            self.mail.send("Mentioned by " + user + " in channel " + channel + "\n" + message)


class IRCBotFactory(protocol.ClientFactory):
    """
        Factory for ircbot
    """

    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        p = IrcBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    f = IRCBotFactory(sys.argv[1])

    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()
