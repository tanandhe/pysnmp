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
    
    conn = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd=' ',
                db='test',
                charset='utf8'
                )
    d = netDevice(conn=conn,ip='61.138.72.2',community='public')
    print (d.name)
#    d.insertIf()
    d.insertMacInfo()
#    p = infoProcess(conn)
#    p.insertIf(interface)
    conn.close()
