# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 23:02:20 2018

@author: Administrator
"""

from pysnmp.hlapi import *
OID = '1.3.6.1.2.1.17.4.3.1.1'
g=nextCmd(SnmpEngine(),
           CommunityData(comunity),
           UdpTransportTarget((ip, 161)),
           ContextData(),
           ObjectType(ObjectIdentity(OID)))
flag = True
while flag:
    errorIndication,errorStatus,errorIndex,varBinds =next(g)
    if errorIndication:
        print(errorIndication)
        break
    elif errorStatus:
        break
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    elif errorIndex:
        break
    else:
        for varBind in varBinds:
            if OID not in str(varBind[0]):
                flag = False
                break
            print(' = '.join([x.prettyPrint() for x in varBind]))

