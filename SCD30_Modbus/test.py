from scd30_modbus import SCD30_Modbus
from time import sleep
from os import system, name

def clearScreen():
    
    if name == 'nt':
        system('cls')
    else:
        system('clear')
    

def run_sync_client():

    clearScreen()

#    sensor = SCD30_Modbus('/dev/ttyAMA0')
    sensor = SCD30_Modbus('/dev/serial0')

    sensor.initPort()

    running = True

    print("SCD30 Test Program")
    print("------------------\n")

    while running:
        readings = sensor.readMeasurements()
        print("CO2 : {0:.2f}".format(readings[0]))
        print("Temperature : {0:.2f}".format(readings[1]))
        print("R.H. : {0:.2f}\n".format(readings[2]))

        sleep(3)

    sensor.closePort()



if __name__ == "__main__":
    run_sync_client()
