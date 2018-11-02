# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 17:52:07 2018

@author: Administrator
"""
from func import *
import datetime

class netDevice(object):
    def __init__(self,conn,ip,community,nameoid="1.3.6.1.2.1.1.5.0"):
        '''
        初始化设备类，获取设备名称，如果获取成功status为online，反之offline
        （网络不可达、团体字错误）
        '''
        self.conn = conn
        self.ip = ip
        self.community = community
        self.name = snmpGet(self.ip,self.community,nameoid)[0][1]
        if self.name != None:
            self.status = 'online'
        else:
            self.status = 'offline'
    def insertIf(self,oid='1.3.6.1.2.1.31.1.1.1.1'):
        '''
        获取设备端口名称和索引，入库
        '''
        if self.status != 'online':
            return
        interface = snmpWalk(self.ip,self.community,oid)
        currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur = self.conn.cursor()

        for d in interface:
            #先根据设备IP地址和端口索引，判断数据库中是否存在索引            
            sql = "select id,ifName from interface where deviceIp='%s' and ifIndex='%s'" % (self.ip,d[0].replace(oid+".",''))
            try:
                res = cur.execute(sql)
                if res:
                    id =  cur.fetchall()[0][0]
            except:
                print ("查询端口失败")
            if res:
                #如果存在，更新端口名称和时间信息
                sql = "UPDATE interface SET ifName='%s',time='%s' WHERE id = %d" % (d[1],currentTime,id)
                try:
                    cur.execute(sql)
                    self.conn.commit()
                except:
                    self.conn.rollback()
                    print ("更新端口失败")
            else:
                sql = "insert into interface(deviceIp,ifIndex,ifName,time) values ('%s','%s','%s','%s')" %\
                 (self.ip,d[0].replace(oid+".",''),d[1],currentTime)
                try:
                    cur.execute(sql)
                    self.conn.commit()
                except :
                    self.conn.rollback()
                    print ("插入端口失败")
        cur.close()  
        
    def addDotIndex(self,oid='1.3.6.1.2.1.17.1.4.1.2'):
        '''
        查询mac地址的dotIndex和ifIndex对应关系，更新interface数据库
        '''
        if self.status != 'online':
            return
        cur = self.conn.cursor()
        index = interface = snmpWalk(self.ip,self.community,oid)
        for i in index:
            sql = "UPDATE interface SET dot1Index='%s' WHERE ifIndex = '%s' and deviceIp='%s'" % (i[0].replace(oid+".",''),i[1],self.ip)
            try:
                cur.execute(sql)
                self.conn.commit()
            except:
                print ("更新索引失败")
        cur.close()
    def insertMacInfo(self,oid='1.3.6.1.2.1.17.4.3.1.2'):
        
        if self.status != 'online':
            return  
        res = None
        cur = self.conn.cursor()
        currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mac = interface = snmpWalk(self.ip,self.community,oid)
#        mac = [['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.64.204', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.75.224', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.81.22', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.111.132', '11'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.120.148', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.126.102', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.130.108', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.131.52', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.134.184', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.134.214', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.139.34', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.141.101', '4'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.143.26', '121'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.148.116', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.154.154', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.160.227', '4'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.162.96', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.162.186', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.164.103', '4'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.183.40', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.188.70', '13'], ['1.3.6.1.2.1.17.4.3.1.2.252.246.71.191.191.82', '13']]
        for m in mac:
             #先根据设备IP地址和端口索引，判断数据库中是否存在索引            
            sql = "select id from macinfo where deviceIp='%s' and dot1Index='%s' and mac ='%s'" % (self.ip,m[1],macConvert(m[0].replace(oid+".",'')))
            try:
#                print (sql)
                res = cur.execute(sql)
                if res:
                    id =  cur.fetchall()[0][0]
            except:
                print ("MAC地址查询失败")
            if res == 0:
                sql = "insert into macinfo(deviceIp,dot1Index,mac,time) values ('%s','%s','%s','%s')" %\
                 (self.ip,m[1],macConvert(m[0].replace(oid+".",'')),currentTime)
                try:
                    cur.execute(sql)
                    self.conn.commit()
                except :
                    self.conn.rollback()
                    print ("插入MAC地址失败")
        cur.close()  
      
        
if __name__ == '__main__':  
#    ip="61.138.72.2"
#    community="#DZ1SW1K!"
#    myDevice = netDevice(ip,community,nameoid='1.3.6.1.2.1.1.5.0')
#    print (myDevice.name)
    print (myDevice.status)