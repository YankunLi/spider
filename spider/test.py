import paramiko


#ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.connect("172.16.1.134", 22, "yankunli", "Liyankun0309")
#stdin, stdout, stderr = ssh.exec_command("lsblk -rno name,mountpoint")
#device_list = []
#while 1:
#    try:
#        ll = stdout.next().strip().split()
#        length = len(ll)
#        if length == 1 and 3 == len(ll[0]):
#            device_list.extend(ll)
#        elif length > 1 or len(ll[0]) > 3:
#            # print ll[0]
#            if device_list.count(ll[0][:3]):
#                device_list.remove(ll[0][:3])
#            # print len(ll[0])
#        else:
#            print "error"
#
#        print(ll)
#    except Exception as e:
#        break
#print(device_list)


def ip_split(ip):
    i = len(ip) - 2
    print(i)
    while True:
        print(ip[i])
        if ip[i] == '.':
            i += 1
            return ip[:i], int(ip[i:])
        if i - 1:
            i -= 1
            continue
        else:
            break
        #raise Exception
import os
ip = '172.28.29.34'
print(ip_split(ip))
print(__file__)
print(os.path.basename(__file__))
print(__name__)
print range(2,12)

import re
pattern = re.compile("^(((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.)\
{3}(?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?)):\d+;?)+$")
print pattern.match("10.0.3.68:3;")


