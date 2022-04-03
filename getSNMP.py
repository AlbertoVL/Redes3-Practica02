from pysnmp.hlapi import *

def consultaSNMP(comunidad, host, oid) -> str:
    try:
        resultado = False
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(comunidad),
                   UdpTransportTarget((host, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid))))

        if errorIndication:
            # print(errorIndication)
            return '2'
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            return ''
        else:
            for varBind in varBinds:
                varB = (' = '.join([x.prettyPrint() for x in varBind]))
                resultado = varB
        return resultado
    except:
        return ''  # PAra cuando exste un error

def consultaSNMP2(comunidad, host, oid) -> str:
    errorIndication, errorStatus,errorIndex, varBinds = nextCmd(
        SnmpEngine(),
        CommunityData(comunidad),
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid)))
    if errorIndication:
        print("errorIndication, file=sys.stderr")
    elif errorStatus:
        print("'%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?')")
    else:
        for varBind in varBinds:
            print(varBind)
    return ''

def snmpwalk(comunidad,host,oid, port:int, raw:bool=False):
    try:
        valor = []
        for (errorIndication,
            errorStatus,
            errorIndex,
            varBinds) in nextCmd(SnmpEngine(),
                                CommunityData(comunidad),
                                UdpTransportTarget((host, 161)),
                                ContextData(),
                                ObjectType(ObjectIdentity(oid)),
                                lexicographicMode=False):
            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break
            else:
                for varBind in varBinds:
                    aux = ' = '.join([x.prettyPrint() for x in varBind])
                    #print(aux)
                    if raw:
                        valor+=[aux]
                    else:
                        valor += [aux.split(' ')[-1]]
        return valor
    except Exception as ex:
        print('Error en SNMPWalk', ex)
        return None
