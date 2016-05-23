#utils.py
import os
import paramiko

SHELL_CMD_GET_DEVICE_INFOR = "lsblk -rfnto name,mountpoint"

# lsblk -rno name,mountpoint
# sda
# sda1
# sda2
# sdb
# sdb1
# sdb2 /boot
# sdb3 [SWAP]

def make_directory(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def check_file_exist(path):
    return os.path.isfile(path)


#def write_to_file(path, content):
#    file_object = open(path, 'a')
#    try:
#        file_object.write(content)
#    finally:
#        file_object.close()
#

def ip_split(ip):
    i = len(ip) - 2
    while True:
        if ip[i] == '.':
            i += 1
            return ip[:i], int(ip[i:])
        elif i - 1:
            i -= 1
            continue
        else:
            break
        #raise


def format_ip(value):
    '''value format is string: 172.16.34.45:67;192.68.24.56:78
    convert it to ip list'''
    ip_sect = value.strip().split(';')
    ip_list = []
    for item in ip_sect:
        temp_list = item.split(':')
        host_num = int(temp_list[1])
        start_ip = temp_list[0]
        prefix, start = ip_split(start_ip)
#         print("ip_split", prefix, start)
        for i in range(start, host_num + start):
#             print(i)
            ip_list.append(prefix + str(i))

    return ip_list


class SSHClient(object):
    def __init__(self, ip, port, privatekey, conn_timeout=None, *args, **kwargs):
        self.ip = ip
        self.port = port if port else 22
        self.conn_timeout = conn_timeout if conn_timeout else None
        self.path_to_private_key = privatekey
        self.password = None
        self.login = None
#         if not self.password and not self.path_to_private_key:
#            pass#  raise Exception, "must private password or privatekey"
        self.ssh = None
        self.sftp = None

    def get_ip(self):
        return self.ip

    def connect_for_command(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        look_for_keys = True
        if self.path_to_private_key:
            self.path_to_private_key = os.path.expanduser(
                    self.path_to_private_key)
            look_for_keys = False
        elif self.password:
            look_for_keys = False

        i = 3
        while True:
            try:
                print("connecting")                
                #import pdb
                #pdb.set_trace()
                ssh.connect(
                            hostname=self.ip,                           
                            port=self.port if self.port else 22,
                            username="root", #self.login if self.login else 'root',
                            password="1111111",
                            key_filename=self.path_to_private_key,
                            look_for_keys=look_for_keys,
                            timeout=self.conn_timeout)
                if self.conn_timeout:
                    transport = ssh.get_transport()
                    transport.sock.settimeout(None)
                    transport.set_keepalive(self.conn_timeout)

                self.ssh = ssh
                break
            except Exception as e:
                i -= 1
                if i:
                    continue
                else:
                    raise e

    def exec_command(self, command):
        return self.ssh.exec_command(command)

    def __obtain_raw_devices(self, devices_info_stream):
        '''fetch raw disk, this function only deal with sda ... sdz,
        if you have more than 24 disk, it cann't resolve please contact'''
        device_list = []
        while True:
            try:
                device_map = devices_info_stream.next().strip().split()
#                 print "spider map is: ", device_map
                length = len(device_map)
                if length == 1 and 3 == len(device_map[0]):
                    device_list.extend(device_map)
                elif length > 0 and len(device_map[0]) > 3:
                    if device_list.count(device_map[0][:3]):
                        device_list.remove(device_map[0][:3])
                else:
                    pass #don't care for
            except Exception as e:
                break
#         print device_list
        return device_list


    def get_host_devices(self):
        cmd = SHELL_CMD_GET_DEVICE_INFOR
        stdin, stdout, stderr = self.exec_command(cmd)
        # device_list = []
        return self.__obtain_raw_devices(stdout)



    def close_connect(self):
        self.ssh.close()


class MGSSH(object):
    hosts_count_num = 0

    @staticmethod
    def increase_hosts():
        MGSSH.hosts_count_num += 1

    @staticmethod
    def get_hosts_num():
        return MGSSH.hosts_count_num

    @staticmethod
    def create_ssh_client(host):
        '''building connection with remote host, there are tow way to 
        building connection, one is using username and password, the other
        is using private key'''
#         if host.auth_type = "password":
#             return SSHClient(host.address, host.port, host.user.name, host.user.passworld)
#         elif host.aut_type = "key":
#             return SSHClient(host.address, host.port, host.private_key)
        client = SSHClient(host.address, host.port, host.private_key)
        return client


if __name__ == "__main__":
    print "test ssh remote"
#     E:\\workplace\\unitedstack\\collect-host-info\\id_rsa
    sshclt = SSHClient("172.16.0.220", 22, "../id_rsa")
#     conn = sshclt.create("172.16.0.220", privatekey="~/.ssh/id_rsa")
    try:
        sshclt.connect_for_command()
    except Exception as e:
        print "hello world"
        raise e
    stdin, stdout, stderr = sshclt.exec_command("lsblk")
    print stdout.readlines()
    # print stdin.readlines()
    print stderr.readlines()
    sshclt.close_connect()
