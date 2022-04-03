from reportlab.pdfgen import canvas
from getSNMP import *
from updateRRD import *
from graphRRD import *
from CreateRRD import *
import os

oids = ['1.3.6.1.2.1.2.1.0',
        '1.3.6.1.2.1.4.9.0',
        '1.3.6.1.2.1.5.22.0',
        '1.3.6.1.2.1.6.11.0',
        '1.3.6.1.2.1.7.3.0']
titulos = ["Paquetes multicast que ha recibido una interfaz",
           "Paquetes recibidos exitosamente, entregado a protocolos IPv4",
           "Mensaje de respuesta ICMP que ha enviado el agente",
           "Segmentos enviados, incluyendo las conexciones actuales y excluyendo los que contienen solamente octetos restransmitidos",
           "Datagramas recibidos que no pudieron ser entregados por cuestiones distintas  a la falta de aplicacion en el puerto"]

def reporte():
    agentes = open("Agentes.txt", 'r')
    cont = 0
    print("Elige el agente del que deseas vel el reporte")

    ### Iteracion para mostrar los agentes registrados y seleccion

    for x in agentes:
        cont += 1
        print(str(cont) + ". " + x[:-1])
    agentes.close()

    # Busqueda de agente para generar reporte

    comunidad = input("Teclea la comunidad: ")
    consulta = open("Agentes.txt", 'r')
    for linea in consulta:
        if linea[:int(len(comunidad))] == comunidad:
            ver = linea[int(len(comunidad)) + 1:int(len(comunidad)) + 3]
            host = linea[int(len(comunidad)) + 4:-1]
            break

    ### Consulta de datos del sistema

    consultaSO = consultaSNMP(comunidad,host,'1.3.6.1.2.1.1.1.0')
    consultaInter = consultaSNMP(comunidad,host,'1.3.6.1.2.1.2.1.0')
    consultaTimeUp = consultaSNMP(comunidad,host,'1.3.6.1.2.1.1.3.0')
    consultaLoca = consultaSNMP(comunidad,host,'1.3.6.1.2.1.1.6.0')

    ### Generacion y llenado de reporte

    report = canvas.Canvas(comunidad + ".pdf")

    text = report.beginText(240, 820)
    text.setFont("Helvetica-Bold", 15)
    text.textLine("Reporte de agente")
    if consultaSO.find('Ubuntu') != -1:
        so = consultaSO.split()[2] + consultaSO.split()[5]
        ubi = consultaLoca.split()[2] + " " + consultaLoca.split()[3]
        inter = consultaInter.split()[2]
        tUp = consultaTimeUp.split()[2]
        report.drawImage("img/Ubuntu.jpg", 450, 710, width=75, height=75)
    elif consultaSO.find('Windows') != -1:
        so = consultaSO.split()[14] + " " + consultaSO.split()[15] + consultaSO.split()[16]
        ubi = consultaLoca.split()[2] + " " + consultaLoca.split()[3]
        inter = consultaInter.split()[2]
        tUp = str(int(consultaTimeUp.split()[2]) // 360000) + "hrs"
        report.drawImage("img/Windows.jpg", 450, 710, width=75, height=75)
    text.setTextOrigin(20, 789)

    text.setFont("Times-Roman", 12)
    text.textLine('Sistema Operativo: ' + so)
    text.textLine('Ubicacion: ' + ubi)
    text.textLine('Numero de interfaces: ' + inter)
    text.textLine('Tiempo de actividad: ' + tUp)
    text.textLine('Comunidad: ' + comunidad)
    text.textLine('Host: ' + host)

    report.line(0, 800, 595, 800)

    tamx = 250
    tamy = 100
    b= 100
    cont = 0
    for x in range(0, len(oids)):
        if cont == 0:
            createBase(comunidad)
            updateM1(comunidad, host, oids[x])
            cont = 1
            grafica(comunidad, titulos[x], str(x+1))
            os.remove(comunidad + ".rrd")
            os.remove(comunidad + ".xml")
        else:
            createBase(comunidad)
            updateM2(comunidad, host, oids[x])
            grafica(comunidad, titulos[x], str(x+1))
            os.remove(comunidad + ".rrd")
            os.remove(comunidad + ".xml")

    report.drawImage(comunidad + "1.png", 20, 600-b, width=tamx, height=tamy)
    report.drawImage(comunidad + "2.png", 300, 600-b, width=tamx, height=tamy)
    report.drawImage(comunidad + "3.png", 20, 470-b, width=tamx, height=tamy)
    report.drawImage(comunidad + "4.png", 300, 470-b, width=tamx, height=tamy)
    report.drawImage(comunidad + "5.png", 20, 340-b, width=tamx, height=tamy)

    report.drawText(text)
    report.save()