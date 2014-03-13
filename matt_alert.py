#!/bin/bash

import smtplib
from config import Config 
from os.path import expanduser, join

class MailAlert:
	"""
		Simple class to send an email alert on hilighting
	"""
	def __init__(self):
		self.__config = Config(join(expanduser("~",".matt_alert"))
	
	def send(self, message):
		try:
			server = smtplib.SMTP(self.__config.getoption('smtp_server'))  
			server.starttls()  
			server.login(self.__config.getoption('username'),self.__config.getoption('password'))  
			server.sendmail(self.__config.getoption('from_address'), self.__config.getoption('to_address'), message)  
			server.quit()	
		except:
			raise
	

