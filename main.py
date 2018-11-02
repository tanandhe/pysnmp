# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 17:22:15 2018

@author: Administrator
"""
from func import *
from infoProcess import *
from netDevice import *

import pymysql

if __name__ == "__main__":
    
#    interface = snmpWalk('61.138.72.2','#DZ1SW1K!','1.3.6.1.2.1.31.1.1.1.1')
    conn = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd=' ',
                db='test',
                charset='utf8'
                )
    d = netDevice(conn=conn,ip='61.138.72.2',community='#DZ1SW1K!')
    print (d.name)
#    d.insertIf()
    d.addDotIndex()
#    p = infoProcess(conn)
#    p.insertIf(interface)
    conn.close()