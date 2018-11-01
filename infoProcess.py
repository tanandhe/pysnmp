# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 15:56:57 2018

@author: Administrator
"""

class infoProcess(object):
    '''
    采集到的数据入库出库功能
    '''
    def __init__(self,conn):
        self.conn = conn
    
    def insertIf(self,device,oid='1.3.6.1.2.1.31.1.1.1.1'):
        cur = self.conn.cursor()
        sql = 'insert into interface(ifName,ifIndex) values (%s,%s)'
        for d in device:
            sql = "insert into interface(ifIndex,ifName) values ('%s','%s')" % (d[0].replace(oid+".",''),d[1])
            res = cur.execute(sql)
            if res:
                self.conn.commit()
            else:
                self.conn.rollback()
        print(res)
        cur.close()             
if __name__ == '__main__':
    conn = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd=' ',
                db='test',
                charset='utf8'
                )
    p = infoProcess(conn)
    device =[['g1/0/1','11'],['g1/0/2','12']]
    p.insertDevice(device)
    conn.close()