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
                values = re.search(r"(?P<key>.*)\W?:\W?(?P<value>.*)", line).groupdict()
                if not values is None:
                    if len(values['value'].strip().split(",")) > 1 and values['value'].strip().startswith("["):
                        channels = [i.strip("[").strip("]") for i in values['value'].split(",")]
                        self.__config[values['key'].strip()] = [i for i in channels if i != ""]
                    else:
                        self.__config[values['key'].strip()] = values['value'].strip()
        cfgfile.close()

    def getoption(self, option):
        if option in self.__config.keys():
            return self.__config[option]
        else:
            raise NoKey

    def setoption(self, option, value):
        self.__config['option'] = value

    def save(self):
        try:
            cfgfile = open(self.__configfile, "w")
            for key, value in self.__config:
                cfgfile.write("%s:%s\n".format(key, value))
            cfgfile.close()

        except IOError:
            raise


#test = Config("test")
