# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 23:02:20 2018

@author: Administrator
"""
from pysnmp.hlapi import *

def macConvert(mac='0.29.128.3.180.152'):
    '''
    MAC地址转换功能：把十进制形式的mac地址转换为16进制
    '''
    tmp = "-".join('{:0>4}'.format(hex(int(i))).replace('0x', '') for i in mac.split('.'))
    return tmp.lower()

def snmpGet(ip,comunity,oid):
    '''
    函数用来实现snmpget的功能
    community ：读团体字
    oid ： 设备OID
    返回值：interface 形式['oid','value']
    '''
    result=[]
    g=getCmd(SnmpEngine(),
               CommunityData(comunity),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))

    errorIndication,errorStatus,errorIndex,varBinds =next(g)
    if errorIndication:
        print(errorIndication)
#        return errorIndication
        return None
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
#        return errorStatus
        return None
    elif errorIndex:
        print (errorIndex)
#        return errorIndex
        return None
    else:
        for varBind in varBinds:
            result.append([str(x.prettyPrint()) for x in varBind])
            print(' = '.join([x.prettyPrint() for x in varBind]))
    return result

def snmpWalk(ip,comunity,oid):
    '''
    函数用来实现snmpwalk的功能
    community ：读团体字
    oid ： 设备OID
    返回值：interface 形式['oid','value']
    '''
    flag = True
    result=[]
    g=nextCmd(SnmpEngine(),
               CommunityData(comunity),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)),
               ignoreNonIncreasingOid=True
               )
    
    while flag:
        errorIndication,errorStatus,errorIndex,varBinds =next(g)
        if errorIndication:
            print(errorIndication)
            return errorIndication
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            return errorStatus
            break
        elif errorIndex:
            print (errorIndex)
            return errorIndex
            break
        else:
            for varBind in varBinds:
                if oid not in str(varBind[0]):
                    flag = False                  
                    break
                result.append([str(x) for x in varBind])
                print(' = '.join([x.prettyPrint() for x in varBind]))
    return result

if __name__ == '__main__':
#    interface = snmpWalk('110.19.8.13','','1.3.6.1.4.1.2011.5.25.123.1.17.1')
#    interface = snmpWalk('61.138.72.2',test','1.3.6.1.2.1.17.4.3.1.2')
    print (interface)
        

