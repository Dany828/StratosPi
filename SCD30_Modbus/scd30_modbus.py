from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from converter import Converter


class SCD30_Modbus:
    
    SLAVE = 0x61
    REG_READY = 0x27
    REG_READING = 0x28 


    def __init__(self,port):
        self.port = port
        self.readings = [0.0] * 3
        self.data = [0] * 4


    def initPort(self):
        self.client = ModbusClient(method='rtu', port=self.port, timeout=1, baudrate=19200)
        self.client.connect()    
        
    def closePort(self):
        self.client.close()    
    
    def dataReady(self):
        hr = self.client.read_holding_registers(self.REG_READY,1, unit=self.SLAVE)
        return hr.registers[0] == 1

    def readMeasurements(self):
        if self.dataReady():
            
            hr = self.client.read_holding_registers(self.REG_READING,6, unit=self.SLAVE)

            if len(hr.registers) == 6:

                word = hr.registers[0]
                self.data[0] = word >> 8
                self.data[1] = word & 0x00FF
                word = hr.registers[1]
                self.data[2] = word >> 8
                self.data[3] = word & 0x00FF
                self.readings[0] = Converter.bytesToFloat(True, self.data) 

                word = hr.registers[2]
                self.data[0] = word >> 8
                self.data[1] = word & 0x00FF
                word = hr.registers[3]
                self.data[2] = word >> 8
                self.data[3] = word & 0x00FF
                self.readings[1] = Converter.bytesToFloat(True, self.data) 
                
                word = hr.registers[4]
                self.data[0] = word >> 8
                self.data[1] = word & 0x00FF
                word = hr.registers[5]
                self.data[2] = word >> 8
                self.data[3] = word & 0x00FF
                self.readings[2] = Converter.bytesToFloat(True, self.data)                
                
                # print("CO2 : {0:.2f}".format(readings[0]))
                # print("Temperature : {0:.2f}".format(readings[1]))
                # print("R.H. : {0:.2f}".format(readings[2]))
                # print("")

        return self.readings
        


