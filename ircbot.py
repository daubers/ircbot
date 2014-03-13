from  twisted.words.protocols import irc
from  twisted.internet import reactor, protocol
from  twisted.python import log
from  config import Config
from  os import join
from  matt_alert import MailAlert 

class IrcBot(irc.IRCClient):
	"""
		Simple irc bot
	"""
	nickname = "MattBot"
	self.cfg = Config(join(expanduser("~",".matt_alert"))
        
        def connectionMade(self):
		irc.IRCClient.connectionMade(self)
		self.mail = MailAlert()
		self.mail.send("IRC Connection Made")

	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)
		self.mail.send("Connection Lost: " + " " + reason)
	
	def  
