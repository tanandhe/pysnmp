# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 17:52:07 2018

@author: Administrator
"""
from func import *

class netDevice(object):
    def __init__(self,ip,community,nameoid="1.3.6.1.2.1.1.5.0"):
        self.ip = ip
        self.community = community
        self.name = snmpGet(self.ip,self.community,nameoid)[0][1]
        if self.name != None:
            self.status = 'online'
        else:
            self.status = 'offline'
        
if __name__ == '__main__':
    ip="61.138.72.2"
    community="#DZ1SW1K!"
    myDevice = netDevice(ip,community,nameoid='1.3.6.1.2.1.1.5.0')
    print (myDevice.name)
    print (myDevice.status)