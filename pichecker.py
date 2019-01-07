import os
from datetime import datetime,timedelta
import time


def piwatchdog():
    txtfile= "/home/pi/StratosPi/SCD30_Modbus/successful_post.txt"
    with open(txtfile, 'r') as myfile:
        data=myfile.read().replace('\n', '')
    a = datetime.strptime(data,'%Y-%m-%d %H:%M:%S.%f')
    b = datetime.now()
    c = b-a
    d = timedelta(seconds=600)
    rebootfile= "/home/pi/StratosPi/SCD30_Modbus/reboot_log.txt"
    if c > d:
        print ("blah blah")
        with open(rebootfile, 'a') as the_file:
            the_file.write(('\n Crashed at:'+ str(datetime.now())))
        os.system("sudo reboot")
          
if __name__ == "__main__":
    print("Watchdog - Started")
    time.sleep(60)
    while True:
        piwatchdog()
        time.sleep(30)


##    print(a)
##    print(b)
##    print(c.total_seconds())
##    print(d)
