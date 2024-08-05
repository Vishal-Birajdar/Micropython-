import network
import json
from umqtt.robust import MQTTClient
from machine import Pin
from esecurity import call_loop
import neopixel
import ssl
import time
import shared
from ota import OTAUpdater


s1_pin= Pin(6,Pin.IN,Pin.PULL_UP)
s2_pin= Pin(7,Pin.IN,Pin.PULL_UP)
s3_pin= Pin(8,Pin.IN,Pin.PULL_UP)
s4_pin= Pin(9,Pin.IN,Pin.PULL_UP)
sensor_pin=[s1_pin,s2_pin,s3_pin,s4_pin]

f = open('config.json',"r")
config = json.load(f)

interval = 1000
previousMillis = time.ticks_ms()
wlan = 0
x = call_loop()

#-------------------------------------___________POWER_ON____________---------------------------------------------------------------
shared.pix[4] = shared.RED
shared.pix.write()
time.sleep(6)
shared.pix[4] = shared.GREEN
shared.pix.write()

#---------------------------------------------_________________CONNECTION__________________-----------------------------------------------------------------
class Connection:
    def __init__(self):
        pass
        
    def wifi_connect(self):
        global wlan
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        for _ in range(30):
            print('Connecting to network....')
            wlan.connect(config['wifi']['ssid'],config['wifi']['password'])
            time.sleep(1)
            if wlan.isconnected():
                net_connect = True
                print("Connected")
                print("IP",wlan.ifconfig())
                break
            time.sleep(6)
        else:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
            machine.reset()
            time.sleep(1)

#---------------------------------------------____________READ_CERTIFICATE_______________--------------------------------------------
    def read_certificate(self,file_path):
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            if not data:
                print(f"Error: {file_path} is empty.")
                return None
            print(f"{file_path} read successfully.")
            return data
        except OSError as e:
            print(f"Error reading {file_path}: {e}")
            return None
#------------------------------------------------------------_______________MQTT_CONNECTION________________--------------------------------------------------------        
    def mqtt_connect(self):
        print("Attempting to connect to MQTT broker...")
        try:
            shared.client = MQTTClient(config['device_info']['device_id'],config['mqtt']['broker'],user=config['mqtt']['user'],password=config['mqtt']['password'],keepalive=60,ssl=True)
            shared.client.set_callback(x.callback)
            shared.client.set_last_will(shared.topic_hb,'-1',False,qos=0)
            shared.client.connect()
            print('Connected to %s MQTT Broker' % config['mqtt']['broker'])
            shared.client.publish(shared.topic_hb,'1')
            shared.client.subscribe(shared.topic_cmd+"/D")
            shared.client.subscribe(shared.topic_cmd+"/FD")
            shared.client.subscribe(shared.topic_cmd+"/R1")
            shared.client.subscribe(shared.topic_cmd+"/R2")
            shared.client.subscribe(shared.topic_cmd+"/R3")
            shared.client.subscribe(shared.topic_cmd+"/R4")
            shared.client.subscribe(shared.topic_cmd+"/RR")
            shared.pix[3] = shared.GREEN
            shared.pix.write()
            return shared.client  
        except:
            print('Failed to connect to MQTT broker. Reconnecting...')
            shared.client = None
            shared.pix[3] = shared.RED
            shared.pix.write()
            return shared.client
            machine.reset()
#----------------------------------------------------__________VERSION_UPDATE_______________--------------------------------------------
       
firmware_url = "https://github.com/Vishal-Birajdar/Micropython-/"
files = ["shared.py", "esecurity.py", "config.json"]
ota_updater = OTAUpdater('DataMann','Datamann@2022' , firmware_url, files)
ota_updater.download_and_install_update_if_available()   
   
p1 = Connection()       
p1.wifi_connect()
   

key_data = p1.read_certificate('privkey4.pem')
cert_data = p1.read_certificate('cert4.pem')
ca_data = p1.read_certificate('chain4.pem')
ssl_params = {
    "certfile": cert_data,
    "keyfile": key_data,
    "cadata": ca_data,
    "server_hostname": config['mqtt']['broker'],
    "cert_reqs": ssl.CERT_REQUIRED
}
p1.mqtt_connect()

#-----------------------------------------------------------__________CONNECTION_CHECKING________________---------------------------------------------

while True:
    currentMillis = time.ticks_ms()
    for i, s_pin in enumerate(sensor_pin):
        shared.buffer["S"+str(i+1)] = str(s_pin.value())+str(i+1)
        if s_pin.value()==1:shared.active_sensor[i]=1
    shared.act_sensor_cnt=shared.active_sensor.count(1)
    print("active sensor",shared.act_sensor_cnt)
    print("sensor buffer",shared.active_sensor)
    time.sleep(1)
    x.main()
    if time.ticks_diff(currentMillis,previousMillis)>=interval:
        previousMillis = currentMillis
        if not wlan.isconnected():
            shared.pix[1] = shared.YELLOW
            shared.pix.write()
            #time.sleep(.4)
            wlan.disconnect()
            time.sleep(.5)
            for _ in range(10):
                print('Retrying wifi...')
                wlan.connect(config['wifi']['ssid'],config['wifi']['password'])
                #connect_wifi()
                time.sleep(1)
                if wlan.isconnected():
                    time.sleep(.3)
                    shared.client.reconnect()
                    print('client reconnected')
                    shared.pix[1] = shared.WHITE
                    shared.pix.write()
                    break
                time.sleep(5)
    time.sleep(1)
    
    




