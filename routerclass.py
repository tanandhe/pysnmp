# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 17:22:10 2018

@author: Administrator
"""

from netDevice import *

class hwSR(netDevice):
    def arpInsert(self,oid='1.3.6.1.4.1.2011.5.25.123.1.17.1.11'):
        if self.status != 'online':
            return
        arp = snmpWalk(self.ip,self.community,oid)
        print(arp)
        currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return arp
    
if __name__ == '__main__':
    conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd=' ',
            db='test',
            charset='utf8'
            ) 
    ip="192.168.1.1"
    community="public"
    myDevice = hwSR(conn,ip,community,nameoid='1.3.6.1.2.1.1.5.0')
    print (myDevice.name)   
    arp = myDevice.arpInsert()
