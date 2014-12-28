import ConfigParser

"""Config is used to retrieve variable information from the config file and pass it to other classes"""
class Config(object):
  def __init__(self, filepath):
    self.filepath = filepath
    self.config = None
    self.read_config_file()

  def read_config_file(self):
    self.config = ConfigParser.ConfigParser()
    self.config.read(self.filepath)
  
  def get(self, category, name):
    return self.config.get(category, name)

  def get_int(self, category, name):
    return self.config.getint(category, name)