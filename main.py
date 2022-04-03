from agente import *
from reporte import *
from Monitoreo import *
import os

def limpiar():
    # Limpiar la consola
    if os.name == "posix":
        print('hola')
        os.system("clear") #3
# Para linux
    elif os.name == "ce" or os.name == "nt" or os.name == "dos": # Para windows
        os.system("cls")

def main():
    print("\t\tBienvenido a la monitarizacion de agentes "
          "\nSelecciona una de las siguientes opciones")
    resumen()
    while(True):
        opc = int(input("1. Agregar agente"
                    "\n2. Eliminar agente"
                    "\n3. Reporte de informacion del agente"
                    "\n4. Resumen"
                    "\n5. Monitoreo"
                    "\n6. Salir"
                    "\nQue opcion desea: "))

        if opc == 1:
            limpiar()
            agregarAg()
        elif opc == 2:
            limpiar()
            eliminarAg()
        elif opc == 3:
            limpiar()
            reporte()
        elif opc == 4:
            limpiar()
            resumen()
        elif opc == 5:
            limpiar()
            reporteMoni()
        elif opc == 6:
            limpiar()
            exit()


main()

