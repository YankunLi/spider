#Collector.py
#collect the information of host spider
import os
import re

from spider.utils import MGSSH
from spider import utils
from spider.RemoteHost import RemoteHost
# from spider.RemoteHost import HostUser
from spider.ConfParser import ConfParser 


PREFIX = "sunfire::ceph::store::"

puppet_directory = "/tmp/puppet/"

OSD_HOSTS_TYPE = ['sata_hosts', 'ssd_hosts']

host_map = {'mon_hosts': [], 'ssd_hosts': [], 'sata_hosts': [], 'client_hosts': [], 'mds_hosts': [], 'rgw_hosts': []}

HOSTS_TYPE = ['sata_hosts', 'ssd_hosts', 'mon_hosts', 'mds_hosts', 'rgw_hosts', 'client_hosts'] #host_map.keys()

service_map = {'mon_hosts': 'enable_mon: true',
               'osd_hosts': 'enable_osd: true',
               'mds_hosts': 'enable_mds: true',
               'rgw_hosts': 'enable_rgw: true',
               'client_hosts': 'enable_client: true'}

host_map_service = {'sata_hosts': 'osd_hosts',
                    'ssd_hosts' : 'osd_hosts',
                    }


def enable_service(fd, service):
    global  PREFIX, service_map
    #structure content
    entity = PREFIX + service_map.get(service) + "\n"
    #persist to file
    try:
        fd.write(entity)
    except IOError as e:
        raise e


def specified_device_type(fd, device_type):
    global PREFIX
    entity = PREFIX + 'disk_type: ' + device_type + "\n"
    try:
        fd.write(entity)
    except IOError as e:
        raise e


def provide_osd_disk(fd, devices):
    global PREFIX
    device_dict = PREFIX + 'osd_device_dict:\n'
    for device in  devices:
        item = "\"" + "/dev/" + device + "\":" + " \"\""
        device_dict += "  " + item + "\n"
    try:
        fd.write(device_dict)
    except IOError as e:
        raise e


def __get_hostname(host):
    ip = host.get_address()
    tmp = ip.split('.')
    hostname = "server-" + tmp[-1]
    return hostname

#def persist_mds_hosts(hosts):
#    global puppet_directory
#    for host in hosts:
#        hostname = __get_hostname(host)
#        path = os.path.join(puppet_directory, hostname)
#        fd = open(path, 'a')
#        try:
#            enable_service(fd, service_map.get('mds'))
#        except Exceptin as e:
#            raise e


def persist_hosts(hosts, service_type, osd_type=None):
    global puppet_directory, host_map_service
    print type(hosts),service_type
    for host in hosts:
        print("perseit for")
        hostname = __get_hostname(host) + ".yaml"
#         print "hostname: " + hostname
        path = os.path.join(puppet_directory, hostname)
        print path
        fd = open(path, 'a')
        try:
            #enable service
            if service_type in host_map_service.keys():
                enable_service(fd, host_map_service.get(service_type))
            else:
                enable_service(fd, service_type)
            #for osd host to persist spider
            if osd_type:
                #specified spider type
                specified_device_type(fd, osd_type)
                #provied osd_device_dict
                devices = host.get_devices()
#                 print("hello world")
                print(devices)
                provide_osd_disk(fd, devices)
        except Exception:
            #should log Exception to log file
            print("wirte error on %s" % host.get_address())
        finally:
                fd.close()


#def persist_osd_hosts(hosts, osd_type):
#    global puppet_directory
#
#    for host in hosts:
#        hostname = __get_hostname(host)
#        path = os.path.join(puppet_directory, hostname)
#        #enable_osd
#        fd = open(path, 'a')
#        try:
#            enable_service(fd, 'osd')
#            #specfied spider type
#            specified_device_type(fd, osd_type)
#            #provide osd_device_dict: "/dev/sdb": ""
#            devices = host.get_devices()
#            provide_osd_disk(fd, devices)
#        finally:
#            fd.close()


#def persist_ssd_hosts():
#    pass
#
#def persist_mon_hosts():
#    pass


class Collector(object):
#     def __init__(self, app, args):
#         self.app = app
#         self.args = args
#         self.host_list = []
#         self.config = None
        
    def __init__(self, config=None):
        self.config = config

    # def __call__(self, environ, start_response):
        # print "run some collection action"
        # self.app(environ, start_response)

    def __call__(self, config=None):
        if not self.config and not config:
            raise Exception("don't have config file") 
        #1.parse config file
        self.config = config if config else self.config
        #2.load hosts from config to create host instances
        self.load_hosts()
        #3.make connection with remote hosts
        #4.capture information about hosts from remote hosts
        #5.update host instances
        self.do_collect() # 3/4/5
        #6.map hosts instances to puppet config for every host
        self.persist_to_file()

    def load_config(self):
        return self.config.get_string_value('default', 'host_privatekey')

    def __check_ip_format(self, value):
        '''value format is {ip}:{num}'''
        pattern = re.compile("^(((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.)\
{3}(?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?)):\d+;?)+$")
        if not pattern.match(value):
            raise Exception("value format is error")
        '''check ip value format {ip}:{num} {ip} is first ip, num is following ip  TODO'''
        if value == '':
            #log warning
            return None
        #raise exception("ip value format is error")
        return value


    def load_hosts(self):
        '''convert *_hosts config to RemoteHost instances'''
        global host_map, OSD_HOSTS_TYPE, HOSTS_TYPE
#         username = self.config.get('default', 'host_username')
#         password = self.config.get('default', 'host_password')
        privatekey = self.load_config()
#         user = HostUser(username, password, privatekey)

        for item in HOSTS_TYPE:
            try:
                tmp_value = self.config.get_string_value('default', item)
            except Exception as e:
                #log warning
                #raise e
                tmp_value = ''
                continue
            decide = self.__check_ip_format(tmp_value)
            if not decide:
                continue
            ip_list = utils.format_ip(tmp_value)
            ip_list = list(set(ip_list))
            for ip in ip_list:
                remote_host = RemoteHost(ip, 22 , privatekey)
                host_map[item].append(remote_host)

    def capture_info(self):
        '''capture host's spider info from remote host'''
        global host_map, HOSTS_TYPE

    def do_collect(self):
        '''collect information from every host by running command lsblk'''
        global host_map, OSD_HOSTS_TYPE
        #creaet connection with remote host
        for item in OSD_HOSTS_TYPE:
            host_list = host_map.get(item)
#             print("host_list length", len(host_list))
#             hosts = host_list
#             print(type(hosts))
            for host in host_list:
#                 import pdb
#                 pdb.set_trace()
#                 print("host_list " + host.address)
                client = MGSSH.create_ssh_client(host)
#                 print(dir(client))
                try:
                    print("start connecting {ip}".format(ip = host.address))
                    client.connect_for_command()
                    devices = client.get_host_devices()
                    host.set_devices(devices)
                except Exception as e:
                    #log error todo
                    raise e
                finally:
#                     client.close_connect()
                    del client


    def persist_to_file(self):
        '''persist host info to file'''
        global host_map, HOSTS_TYPE, OSD_HOSTS_TYPE
        print("enter persist")
        for host_type in HOSTS_TYPE:
            host_list = host_map.get(host_type)
#             if len(host_list):
#                 print host_list[0].get_devices()
            if host_type in OSD_HOSTS_TYPE:
                print("start persist for osd")
                if host_type == 'sata_hosts':
                    print("persist sata")
                    persist_hosts(host_list, host_type, 'sata')
                else:
                    persist_hosts(host_list, host_type, 'ssd')
            else:
                print("start persist or no osd")
                persist_hosts(host_list, host_type)


    def check_result_of_devices(self):
        pass

    def pre_process_devices_info(self):
        pass

    def process_devices(self):
        pass

    def store_to_host(self):
        pass

    def format_output(self):
        pass

import sys

def main():
    global puppet_directory
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            path_config_file = os.path.abspath(sys.argv[1])
    else:
        if not os.path.isfile("/etc/spider/spider.conf"):
            print("ERROR:don't found config file in /etc/spider/")
        path_config_file = "/etc/spider/spider.conf"

    conf = ConfParser(path_config_file)
    if conf.is_exist_config_key('default', 'result_path'):
        puppet_directory = conf.get_string_value('default', 'result_path')

    if not os.path.isdir(puppet_directory):
        os.makedirs(puppet_directory)

    collector = Collector(conf)
    collector()


if __name__ == "__main__":
#     path_config_file = sys.argv[1]
#     if sys.argv[2]:
#         path_log_file =  sys.argv[2]
#
#
#     conf = ConfParser(path_config_file)
    path_config_file = "../../etc/spider/spider.conf"
    conf = ConfParser(path_config_file)
    collector = Collector(conf)
    collector()
    
