import requests
import json
import base64
import datetime
import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from os import system, name

#Gives Pi Time to boot
time.sleep(15)

#UAA Details
UAA_token = ''
app_URL = 'https://stratos-proxy.run.aws-usw02-pr.ice.predix.io/'
app_UAA_URL = 'https://aa15a2d0-bfc0-4ae7-b864-8f196004bdcb.predix-uaa.run.aws-usw02-pr.ice.predix.io/'
asset_Path = 'asset/pace'
timeseries_Path = 'ingest/timeseries'
SLAVE = 247

#Client Details
client_id = 'OG_PACE_INGEST'
client_password = 'Z[;eH+ZR6\,":`*$'

def getUAAToken():
    global UAA_token
    return UAA_token

def obtainNewUAAToken():
    while True:
        try:
            global UAA_token
            #UAA Authorisation
            UAA_authorization = 'Basic ' + base64.b64encode((client_id + ':' + client_password).encode('utf-8')).decode('utf-8')

            #Python Dictionaries for headers and parameters
            UAA_header =  {'Pragma': 'no-cache' ,'content-type': 'application/x-www-form-urlencoded','Cache-Control':'no-cache','authorization': UAA_authorization}
            UAA_params = {'client_id':client_id,'grant_type':'client_credentials'}
            UAA_issuer_id = app_UAA_URL + 'oauth/token'

            #Obtain access token
            r_UAA = requests.get(UAA_issuer_id,headers = UAA_header,params=UAA_params, timeout=60)
            UAA_token = r_UAA.json()['access_token']
            print('Token Obtained from Stratos')
            return

        except:
            print('Cannot Obtain UAA Token..Trying Again...')
            time.sleep(5)

startTime = 0

def getStartTime_STR():
    return startTime_STR

def setStartTime_STR(time):
    global startTime_STR
    startTime_STR = time
    return startTime_STR
    
def timeSeriesPost(json_data):
    y = 0
    while True:
        try:
            #If running time > 8 Hours then this needs changing to read token exp time.
            runningTime = time.time() - getStartTime_STR()
            if(runningTime > 28800): ##8 hours 
                setStartTime_STR(time.time())
                obtainNewUAAToken()
        
            #Get details
            timeseries_uri = app_URL + timeseries_Path
            UAA_header_2 = {'authorization': "Bearer " + getUAAToken(), 'content-type' : 'application/json'}

            #Post request
            r = requests.post(timeseries_uri, headers=UAA_header_2, data=json_data, timeout=60)
            return

        except requests.ConnectionError:
            y += 1
            if y < 5:
                print('Stratos Waiting for network connection...')
                time.sleep(1)
            else:
                y = 0
                break #will continue to CP if it can't post the data

            
def stratosPost():

    #Modbus connection and reads registers
    client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=1, baudrate=9600)
    client.connect()
    hr = client.read_holding_registers(7,3, unit=SLAVE)


    sensor1 = temperature = hr.registers[0] / 10.0 
    sensor2 = humidity = hr.registers[1] / 10.0 
    timeTS = int(time.time()*1000)
  
    
    print("Formatting and Posting Time Series Data")

    dataStratos = {
        "messageId": str(timeTS),
        "body": [
                {
                "name": 'BHGE_DS_MC_LEIC_UKAS_TEMP' ,
                "datapoints": [
                    [
                        timeTS,
                        sensor1
                        ]
                    ]
                },

                {
                "name": 'BHGE_DS_MC_LEIC_UKAS_HUMIDITY' ,
                "datapoints": [
                    [
                        timeTS,
                        sensor2
                        ]
                    ]
                },

            ]
        }

    json_dataStratos = json.dumps(dataStratos)
 
    #Post json data to Predix
    timeSeriesPost(json_dataStratos)
    
    return

i=0    

def main():
    global i
    print("\nObtaining UAA Token")
    setStartTime_STR(time.time()) # New token start time for Stratos.
    obtainNewUAAToken() #8 hour exp. time
    assetTimer = time.time()
    
    while True:        
        print("\n\n************** Loop " + str(i) + " **************\n")
        stratosPost()
        runningTime = time.time() - startTime
        print('Successfully Posted')
        time.sleep(30) #30 second delay
        i += 1

main()




                
