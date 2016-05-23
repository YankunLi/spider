#auth liyankun
#parse configure file
import sys, os
import ConfigParser


class ConfParser(object):
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.config_file_path)

    def __open_config(self, config_file_path, file_type=None):
        #read configure
        return open(config_file_path, "w")

    def get_keys(self, section):
        return self.cf.options(section)

    def get_int_value(self, section, key):
        return self.cf.getint(section, key)

    def get_string_value(self, section, key):
        return self.cf.get(section, key)

    def find_key(self, section, key):
        return True;

    def get_sections(self):
        return self.cf.sections()

    def get_config_file_path(self):
        return self.config_file_path

    def set_value(self, section, key, value):
        self.cf.set(section, key, value)

    def persist_config(self, config_file_path):
        self.cf.write(self.__open_config(config_file_path))

    def get_items(self, section):
        return self.cf.items(section)

    def add_section(self, section):
        self.cf.add_section(section)

    def get_ips(self, section, key):
        value = self.get_string_value(section, key)
        items = value.split(';')


if __name__ == "__main__":
    print os.getcwd()
    print os.path.abspath("..")
    current_path = os.path.abspath("..")#os.getcwd()
    print os.path.join(current_path, "installer.conf")
    config_file_path = os.path.join(current_path, "installer.conf")
 #   if os.path.exists(config_file_path):
    cf = ConfParser(config_file_path)
  #  else:
  #      print "don't found this file"
    print cf.get_sections()
    print cf.get_keys("default")
    print cf.get_int_value("server", "port")
    print cf.get_string_value("ustack", "username")
#     cf.set_value("ustack", "password", "78654321")
    print cf.get_items("ustack")
    cf.persist_config(config_file_path)
    print "hello world"
    print type(cf.get_string_value("ustack", "password"))
    print cf.get_string_value("ustack", "passwords")


