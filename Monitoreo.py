import selectors, sys
from time import sleep
from typing import Dict
import rrdtool
import getSNMP
import getpass
import updateRRD
import CreateRRD
import graphRRD
from reportlab.pdfgen import canvas

nombresDina = [
    "Numero total de segmentos recibidos: ",
    "Numero total de segmentos enviados excluyendo aquellos con octetos retransmitidos: ",
    "Numero total de segmentos restransmitidos que contiene uno o mas octetos previos ",
    "Numero total de segmentos recibidos por error: ",
    "Numero total de segmentos enviados con una bandera RST: ",
    "Numero de veces de conexiones TCP de una conexion directa al estado SYN-SENT desd estado Closed: ",
    "Numero de veces de conexiones TCP de una conexion directa al estado SYN-RCVD desd estado Listen: ",
    "Suma de conexiones directas entre estado SYN-SENT & SYN-RCVD desde Closed y Listen: ",
    "Conexiones desde el estado Closed a cualquier establecido o CLOSE-WAIT: ",
    "Numero de conexiones TCP las que su estado es Establecido o Close-Wait: "
]
oidsDina = [
    "1.3.6.1.2.1.6.10",
    "1.3.6.1.2.1.6.11",
    "1.3.6.1.2.1.6.12",
    "1.3.6.1.2.1.6.14",
    "1.3.6.1.2.1.6.15",
    "1.3.6.1.2.1.6.5",
    "1.3.6.1.2.1.6.6",
    "1.3.6.1.2.1.6.7",
    "1.3.6.1.2.1.6.8",
    "1.3.6.1.2.1.6.9"
]

nombreStatic = [
    "Algoritmo para retransmision de octetos no reconocidos: ",
    "Val Min permitido para tiempo de espera de retransmision (mili): ",
    "Val Min permitido para tiempo de espera de retransmision (mili): ",
    "Limite en el numero total de conexiones TCP que la entidad puede soportar: ",
]

oidStatic = [
    "1.3.6.1.2.1.6.1",
    "1.3.6.1.2.1.6.2",
    "1.3.6.1.2.1.6.3",
    "1.3.6.1.2.1.6.4"
]

def reporteMoni():
    report = canvas.Canvas("Monitoreo.pdf")
    text = report.beginText(240, 820)
    text.setFont("Helvetica-Bold", 15)
    text.textLine("Reporte de Monitoreo")
    text.setTextOrigin(20, 789)

    fecha = getSNMP.consultaSNMP("comunidadASNMP2", "192.168.1.172", "1.3.6.1.2.1.1.1.0")
    fecha = fecha.split()[7:13]
    fechaF = ''
    for x in fecha:
        fechaF = fechaF + ' ' + x

    text.setFont("Times-Roman", 12)
    text.textLine("Device: Servidor 1")
    text.textLine("Description: Contabilidad servidor 1")
    text.textLine("Date: " + fechaF)
    text.textLine("DefaultProtocol: Radius")
    text.textLine("rdate: " + fechaF)
    text.textLine("Numero de puerto: 22")
    text.textLine("User-Name: " + getpass.getuser())
    text.textLine("IP: 192.168.1.172")
    for x in range(1, len(oidStatic)+1):
        dato = getSNMP.snmpwalk("comunidadASNMP2", "192.168.1.172",oidStatic[x-1], 22)
        text.textLine(nombreStatic[x-1] + dato[0])
    text.textLine(" ")
    for x in range(1, len(oidsDina)+1):
        CreateRRD.createBaseMon()
        updateRRD.updateM(oidsDina[x-1])
        dato = graphRRD.grafMon()
        print(dato['print[0]'])
        text.textLine(nombresDina[x-1] + dato['print[0]'])
        CreateRRD.rm()
    report.drawText(text)
    report.save()