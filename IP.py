#!/usr/bin/python
# coding: utf-8

import re


class IP(object):
    __ip_string = ''
    __ip = ''
    __netmask = ''

    def get_ip_string(self):
        return self.__ip_string

    def get_ip(self):
        return self.__ip

    def get_netmask(self):
        return self.__netmask

    def __init__(self, ip_str):
        if ip_str is not None and len(ip_str.strip()) > 0:
            self.__ip_string = ip_str.strip()
        if not self.__check_ip():
            raise ValueError('ip string error, ip string: %s' % ip_str)

    def __check_ip(self):
        match = re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$', self.__ip_string)
        if match:
            ips = self.__ip_string.split('/')
            self.__ip = ips[0]
            if 0 < int(ips[1]) <= 32:
                self.__netmask = int(ips[1])
                return True
        return False

    def get_subnet(self):
        netmask = IP.netmask_to_string(self.__netmask)
        ip_array = self.__ip.split('.')
        netmask = netmask.split('.')
        newip_array = [0 for i in range(4)]
        for i in range(0, 4):
            newip_array[i] = str(int(ip_array[i]) & int(netmask[i]))
            subnet = str(newip_array[0]) + '.' + str(newip_array[1]) \
                + '.' + str(newip_array[2]) + '.' + str(newip_array[3])
        return subnet

    @staticmethod
    def netmask_to_string(netmask_num):
        if isinstance(netmask_num, int):
            if netmask_num <= 32:
                netmask_array = [0 for i in range(32)]
                for i in range(0, 32):
                    if i < netmask_num:
                        netmask_array[i] = '1'
                    else:
                        netmask_array[i] = '0'
                netmask1 = netmask_array[:8]
                netmask2 = netmask_array[8:16]
                netmask3 = netmask_array[16:24]
                netmask4 = netmask_array[24:32]
                netmask = str(int(''.join(netmask1), 2)) + '.' + str(int(''.join(netmask2), 2)) + '.' + \
                          str(int(''.join(netmask3), 2)) + '.' + str(int(''.join(netmask4), 2))
                return netmask
        return None

    @staticmethod
    def is_ip_in_same_subnet(ip1, ip2):
        if isinstance(ip1, IP) and isinstance(ip2, IP):
            if ip1.get_netmask() == ip2.get_netmask():
                if ip1.get_subnet() == ip2.get_subnet():
                    return True
        return False


if __name__ == '__main__':
    ip1 = IP('172.17.17.25/16')
    ip2 = IP('172.17.15.25/16')
    ip3 = IP('172.22.66.83/24')
    print(ip1.get_subnet())
    print(ip2.get_subnet())
    print(ip3.get_subnet())
    print(IP.is_ip_in_same_subnet(ip1, ip2))
