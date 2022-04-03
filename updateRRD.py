import time
import rrdtool
from getSNMP import *
total_input_traffic = 0
total_output_traffic = 0

def updateM1(comunidad,host,oid1):
    for x in range (0, 3):
        consultaInter = consultaSNMP(comunidad, host ,oid1)
        print(consultaInter.split()[2])
        for x in range(1, int(consultaInter.split()[2]) +1):
            totaltraffic =consultaSNMP(comunidad, host,
                             '1.3.6.1.2.1.2.2.1.12.'+str(x))

            valor = "N:" + str(totaltraffic.split()[2]) + ":" + str(totaltraffic.split()[2])
            print (valor)
            rrdtool.update(comunidad + '.rrd', valor)
            rrdtool.dump(comunidad + '.rrd',comunidad+'.xml')
            time.sleep(1)

def updateM2(comunidad,host,oid1):
    for x in range(0, 100):
        consultaInter = consultaSNMP(comunidad, host ,oid1)
        totaltraffic = consultaInter

        valor = "N:" + str(totaltraffic.split()[2]) + ":" + str(totaltraffic.split()[2])
        print (valor)
        rrdtool.update(comunidad + '.rrd', valor)
        rrdtool.dump(comunidad + '.rrd',comunidad+'.xml')
        time.sleep(1)

def updateM(oid):
    for x in range(0,100):
        dato = snmpwalk("comunidadASNMP2", "192.168.1.172", oid, 22)

        valor = "N:" + str(dato[0])
        print(valor)
        rrdtool.update('Monitoreo.rrd', valor)
        rrdtool.dump('Monitoreo.rrd', 'Monitoreo.xml')

#updateM2("comunidadWind1", "192.168.1.80", '1.3.6.1.2.1.5.22.0')
#updateM('1.3.6.1.2.1.6.15')
#time.sleep(120)
# '1.3.6.1.2.1.2.1.0'
