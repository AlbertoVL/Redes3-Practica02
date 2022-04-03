import os
from getSNMP import *

def estadoInterfaz(val):
    if val == '2':
        estado = 'down'
    else:
        estado = 'up'
    return estado


class Agente():
    ip = ''
    version = ''
    comunidad = ''
    tamcom = ''
    def __init__(self):
        self.ip = ''
        self.version = ''
        self.comunidad = ''
        self.puerto = 161

def agregarAg():
    print("\t\tPara poder agregar un agente necesito los siguientes datos")
    agente = Agente()
    agente.ip = input("Nombre del host o IP: ")
    agente.version = input("Ingrese la version de la MIB: ")
    agente.comunidad = input("Ingrese el nombre de la comunidad: ")
    datos = agente.comunidad + " " +\
            "v" + agente.version + " " +\
            agente.ip + "\n"

    libro = open("Agentes.txt", 'a')
    libro.write(datos)
    libro.close()

def eliminarAg():
    com = input("Ingrese el nombre de la comunidad para eliminar el agente: ")
    libro = open("AgentesN.txt", 'w')
    consulta = open("Agentes.txt", 'r')

    for linea in consulta:
        if linea[:int(len(com))] != com:
            libro.write(linea)

    libro.close()
    consulta.close()

    os.remove("Agentes.txt")
    os.rename("AgentesN.txt", "Agentes.txt")

    if os.path.exists(com + ".pdf"):
        os.remove(com + ".pdf")
        for x in range(1,6):
            os.remove(com + str(x) + ".png")
    else:
        pass

def resumen():
    numAgentes = open("Agentes.txt").readlines()
    print("Numero de agentes: {} \n".format(len(numAgentes)))
    estado = ''
    cont = 0
    for x in numAgentes:
        cont += 1
        consultaInter = consultaSNMP(x.split()[0],x.split()[2],'1.3.6.1.2.1.2.1.0')
        estado = estadoInterfaz(consultaInter)
        if estado == 'up':
            num = consultaInter.split()[2]
        else:
            num = None

        print("\nAgente {} Comunidad: {}"
              "\nEstado del agente: {}"
                "\nNumero de interfaces: {} "
                "\nDescripcion de interfaces: \n".format(cont, x.split()[0], estadoInterfaz(consultaInter), num))

        if consultaInter != '2' and consultaInter.split()[2] != '40':
            for y in range(1,int(consultaInter.split()[2])+1):
                consultaInter2 = consultaSNMP(x.split()[0],x.split()[2],'1.3.6.1.2.1.2.2.1.2.' + str(y))
                consultaInterSta = consultaSNMP(x.split()[0],x.split()[2],'1.3.6.1.2.1.2.2.1.7.' + str(y))
                print("Interfaz {} -> '{}'"
                      "\t\tEstado de interfaz -> {} ".format(str(y),consultaInter2.split()[2],estadoInterfaz(consultaInterSta.split()[2])))
        else:
            if estadoInterfaz(consultaInter) == 'up':
                consultaInter2 = consultaSNMP(x.split()[0],x.split()[2],'1.3.6.1.2.1.2.2.1.2.18')
                consultaInterSta = consultaSNMP(x.split()[0],x.split()[2],'1.3.6.1.2.1.2.2.1.7.18')
                print("Interfaz {} -> '{}'"
                      "\t\tEstado de interfaz -> {} ".format('1',consultaInter2.split()[2],estadoInterfaz(consultaInterSta.split()[2])))
            else:
                pass
