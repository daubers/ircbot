"""
	This file contains functionality for loading a config file of
	key : value form and accessing values from it
"""
import re

class NoKey(Exception):
	pass

class Config:
	def __init__(self, filepath):
		self.__configfile = filepath
		self.__config = {}
		self.__load()
		
	def __load(self):
		cfgfile = open(self.__configfile, "r")
		for line in cfgfile:
			if not line[0] == "#":
				values = re.search(r"(?P<key>.*)\W?:\W?(?P<value>.*)", test).groupdict()
				if not values is none:
					self.__config[values['key']] = values['value']
		cfgfile.close()
	
	def getoption(self, option):
		if option in self.__config.keys():
			return self.__config['option']
		else:
			raise NoKey

	def setoption(self,option, value):
		self.__config['option'] = value
	
	def save(self):
		try:
			cfgfile = open(self.__configfile,"w")
			for key, value in self.__config:
				cfgfile.write("%s:%s\n".format(key, value))
			cfgfile.close()
		
		except IOError:
			raise

test = Config("test")		
