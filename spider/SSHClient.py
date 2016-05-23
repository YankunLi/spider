#SSHClient.py
class SSHClient(object):
    def __init__(self, ip, port, conn_timeout, login, password=None,
            privatekey=None, *args, **kwargs):
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password
        self.conn_timeout = conn_timeout if conn_timeout else None
        self.path_to_private_key = privatekey

    def get_connect(self, ip, port=None):
        pass
