import time
import sys
import ibmiotf.application
import ibmiotf.device
import random


organization = "i2kxvc"
deviceType = "nodemcu"
deviceId = "1001"
authMethod = "token"
authToken = "1234567890"

# Initialize GPIO
def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='contact':
                print("Inform to Doctor")
try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli = ibmiotf.device.Client(deviceOptions)
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

deviceCli.connect()

while True:
        name = "ABC"
        contact = "1234567890"
        drname = "XYZ"
        temp = 95
        tempc ="{:.2f}".format((temp - 32) / 1.8)
        pulse = 72

        
        

        #Send Value  to IBM Watson
        
        data = {'d':{'temp' : temp,'tempc' : tempc, 'pulse' : pulse,'name' : name,'contact' : contact,'drname' : drname}}
        
        #print (data)
        def myOnPublishCallback():
            print ("Your Body Temperature = %s F" % temp,"Your Body Temperature = %s C" % tempc,"Your Pulse Rate = %s Beats/minute" % pulse,)    
        if temp >= 99 :
                print("Your Body temerature is High.....Please Contact Your Doctor")
        if temp < 97 :
                print("Your Body temerature is Low.....Please Contact Your Doctor")
        if pulse >100 :
                print("Your Pulse rate is High.....Please Contact Your Doctor")
        if pulse <60 :
                print("Your Pulse rate is Low.....Please Contact Your Doctor")
        
        
        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(5)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()


