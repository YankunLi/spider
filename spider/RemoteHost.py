#RemoteHost.py

class RemoteHost(object):
    def __init__(self, ip, port, path_provide_key):
        self.address = ip
        self.port = port 
        self.private_key = path_provide_key
        self.hostname = None
        self.devices = None
#         self.user = user
        # self.user


    def set_devices(self, devices):
        self.devices = devices
    
    def get_address(self):
        return self.address


    def get_hostname(self):
        if self.hostname:
            return self.hostname
        else:
            return self.hostname

    def get_devices(self):
        if self.devices != None:
            return self.devices

    def get_network(self):
        return self.ip

    def get_privatekey(self):
        return self.privatekey

    def set_hostname(self, hostname):
        self.hostname = hostname


class HostUser(object):
    def __init__(self, login, password, privatekey=None):
        self.login = login
        self.password = password
        self.privatekey = privatekey if privatekey else None

    def get_login(self):
        return self.login

    def get_password(self):
        return self.password

    def get_privatekey(self):
        return self.privatekey

    def set_login(self, name):
        self.login = name

    def set_password(self, password):
        self.password = password

    def set_privatekey(self, privatekey):
        self.privatekey = privatekey



if __name__ == "__main__":
    ll = []
    if ll != None:
        print "hello world"

