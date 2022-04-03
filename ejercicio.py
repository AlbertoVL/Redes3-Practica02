import sys
import rrdtool
import time

def grafica(comunidad, titulo, cont):
    tiempo_actual = int(time.time())
    #Grafica desde el tiempo actual menos diez minutos
    tiempo_inicial = tiempo_actual - 900

    ret = rrdtool.graph(comunidad + str(cont) + ".png",
                         "--start",str(tiempo_inicial),
                         "--end","N",
                         "--vertical-label=Bytes/s",
                         "--title=" + titulo,
                         "DEF:inoctets=" + comunidad + ".rrd:inoctets:AVERAGE",
                         "DEF:outoctets=" + comunidad + ".rrd:outoctets:AVERAGE",
                         "AREA:inoctets#00FF00:Tráfico",
                         "LINE3:outoctets#0000FF:Tráfico")
