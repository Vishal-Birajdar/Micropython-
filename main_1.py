import network
import json
from umqtt.robust import MQTTClient
from machine import Pin
import ubinascii
import time
import neopixel
import ssl
import os
buffer = {"D":'10',"FD":"01","S1":'01',"S2":'02',"S3":'03',"S4":'04',"R1":'0101',"R2":'0102',"R3":'0103',"R4":'0104',"HB":'1'}
buffer_json={}
active_sensor=[0,0,0,0]

string_json = json.dumps(buffer)
f = open('config.json',"r")
config = json.load(f)
sensor_delay =config["device_info"]["sensor_delay"]

R1State = Pin(2,Pin.OUT)
R2State = Pin(3,Pin.OUT)
R3State = Pin(4,Pin.OUT)
R4State = Pin(5,Pin.OUT)

s1_pin= Pin(6,Pin.IN,Pin.PULL_UP)
s2_pin= Pin(7,Pin.IN,Pin.PULL_UP)
s3_pin= Pin(8,Pin.IN,Pin.PULL_UP)
s4_pin= Pin(9,Pin.IN,Pin.PULL_UP)
sensor_pin=[s1_pin,s2_pin,s3_pin,s4_pin]

#----------------------------------------------------------------____LED LIGHT____ ------------------------------------------------------------------------------------------
pixPin = 22
Pixsize = 5
pix = neopixel.NeoPixel(Pin(pixPin),Pixsize)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
ORANGE = (255,165,0)

topic_json = config['device_info']['c_code']+'/'+config['device_info']['a_code']+'/'+config['device_info']['s_code']+'/'+config['device_info']['s_topic']+'/'+config['device_info']['device_id']
topic_cmd = config['device_info']['c_code']+"/"+config['device_info']['a_code']+"/"+config['device_info']['s_code']+"/CC/"+config['device_info']['device_id']
topic_hb = config['device_info']['c_code']+"/"+config['device_info']['a_code']+"/"+config['device_info']['s_code']+"/HB/"
s_topic = ["D","FD","R1","R2","R3","R4","RR"]
#--------------------------------------------____________________________-----------------------------------___________-------------------------------------

arm_status = True
act_sensor_cnt=0
FG_Arm = False
client = None
net_connect = False
#wlan = 0
interval = 1000
previousMillis = time.ticks_ms()
#--------------------------------------------------------____________________________------------------------------------
pix[4] = RED
pix.write()
time.sleep(10)
pix[4] = GREEN
pix.write()

#-------------------------------___________wifi_connection_________________-----------------------------------------------------------------------------
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
def connect_wifi():
    global net_connect,wlan
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
        restart_and_reconnect()
        time.sleep(1)
#--------------------------------------------_______File_Reading________________________-----------------------------------------------------------
def read_certificate(file_path):
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

key_data = read_certificate('privkey4.pem')
cert_data = read_certificate('cert4.pem')
ca_data = read_certificate('chain4.pem')

# Ensure none of the certificates are None
if not key_data or not cert_data or not ca_data:
    print("One or more certificates are invalid.")
    exit(1)

# Put them in a dict
ssl_params = {
    "certfile": cert_data,
    "keyfile": key_data,
    "cadata": ca_data,
    "server_hostname": config['mqtt']['broker'],
    "cert_reqs": ssl.CERT_REQUIRED
}

#-------------------------------mqtt-connection----------------------------------------------------------------------------------------
def mqtt_connect():
    global client
    print("Attempting to connect to MQTT broker...")
    try:
        client = MQTTClient(config['device_info']['device_id'],config['mqtt']['broker'],user=config['mqtt']['user'],password=config['mqtt']['password'],keepalive=60,ssl=True)
        client.set_callback(callback)
        client.set_last_will(topic_hb,'-1',False,qos=0)
        client.connect()
        print('Connected to %s MQTT Broker' % config['mqtt']['broker'])
        client.publish(topic_hb,'1')
        client.subscribe(topic_cmd+"/D")
        client.subscribe(topic_cmd+"/FD")
        client.subscribe(topic_cmd+"/R1")
        client.subscribe(topic_cmd+"/R2")
        client.subscribe(topic_cmd+"/R3")
        client.subscribe(topic_cmd+"/R4")
        client.subscribe(topic_cmd+"/RR")
        pix[3] = GREEN
        pix.write()
        return client  
    except:
        print('Failed to connect to MQTT broker. Reconnecting...')
        client = None
        return client
        restart_and_reconnect()
#----------------------------_____________Reset______________________------------------------------------------------------------------------------------    
def restart_and_reconnect():
    pix[3] = RED
    pix.write()
    time.sleep(4)
    machine.reset()
#--------------------------------------------------------____________callback_______________----------------------------------------------------------    
def callback(topic_cmd,msg):
    global arm_status,buffer,string_json,active_sensor,FG_Arm
    decoded_topic = topic_cmd.decode('utf-8').strip()
    decoded_msg = msg.decode('utf-8').strip()
    print("decoded_topic:"+decoded_topic)
    print("decoded_msg:"+decoded_msg)
    if decoded_topic.endswith("FD"):
        print("decoded_topic:"+decoded_topic)
        if decoded_msg == '12':
            buffer["FD"] = '12'
            FG_Arm = True
            print("FG_Arm ",FG_Arm)
            string_json = json.dumps(buffer)
        elif decoded_msg == '01':
            buffer["FD"] == '01'
            FG_Arm = False
            print("FG_Arm ",FG_Arm)
            string_json = json.dumps(buffer)
        else:
            print("Invalid Input !")
    elif decoded_topic.endswith("D"):
        print("decoded_topic:"+decoded_topic)
        if decoded_msg == '00':
            buffer["D"] = decoded_msg
            arm_status = False
            string_json = json.dumps(buffer)
            pix[0] = RED
            pix.write()
        elif decoded_msg == '10':
            buffer["D"] = decoded_msg
            arm_status = True
            string_json = json.dumps(buffer)
            pix[0] = GREEN
            pix.write()
            print("Arm_status is ", arm_status)
        else:
            print("Invalid input!!")
    elif decoded_topic.endswith("RR"):
        if decoded_msg == '05':
            R1State.value(0)
            R2State.value(0)
            R3State.value(0)
            R4State.value(0)
            active_sensor =[0,0,0,0]
            buffer["R1"] = '0101'
            buffer["R2"] = '0102'
            buffer["R3"] = '0103'
            buffer["R4"] = '0104'
            string_json = json.dumps(buffer)
    elif decoded_topic.endswith("R1"):
        if decoded_msg == '0101':
            buffer["R1"] = decoded_msg
            R1State.value(0)
            string_json = json.dumps(buffer)
            print("R1 state ",R1State.value())
        elif decoded_msg == '1101' and arm_status:
            buffer["R1"] = decoded_msg
            string_json = json.dumps(buffer)
            R1State.value(1)
        else:
            print("Invalid input")
        
    elif decoded_topic.endswith("R2"):
        if decoded_msg == '0102':
            buffer["R2"] = decoded_msg
            string_json = json.dumps(buffer)
            R2State.value(0)
        elif decoded_msg == '1102' and arm_status:
            buffer["R2"] = decoded_msg
            string_json = json.dumps(buffer)
            R2State.value(1)
        else:
            print("Invalid input")
    elif decoded_topic.endswith("R3"):
        if decoded_msg == '0103':
            buffer["R3"] = decoded_msg
            R3State.value(0)
            string_json = json.dumps(buffer)
        elif decoded_msg == '1103' and arm_status:
            buffer["R3"] = decoded_msg
            string_json = json.dumps(buffer)
            R3State.value(1)
        else:
            print("Invalid input")
    elif decoded_topic.endswith("R4"):
        if decoded_msg == '0104':
            buffer["R4"] = decoded_msg
            string_json = json.dumps(buffer)
            R4State.value(0)
        elif decoded_msg == '1104' and arm_status:
            buffer["R4"] = decoded_msg
            string_json = json.dumps(buffer)
            R4State.value(1)
        else:
            print("Invalid input")       
    string_json = json.dumps(buffer)
    client.publish(topic_json,string_json)
#----------------------------------------------------------------------------------_______________main_Function______________________________----------------------------------------
def main():
    global act_sensor_cnt,active_sensor,arm_status,sensor_pin,FG_Arm
    global previousMillis,interval
    connect_wifi()
    time.sleep(0.5)
    client = mqtt_connect()
    while True:
        currentMillis = time.ticks_ms()
        try:
            time.sleep(1)
            client.check_msg()
            for i, s_pin in enumerate(sensor_pin):
                buffer["S"+str(i+1)] = str(s_pin.value())+str(i+1)
                if s_pin.value()==1 and arm_status :active_sensor[i]=1
            act_sensor_cnt=active_sensor.count(1)
            print("active sensor",act_sensor_cnt)
            print("sensor buffer",active_sensor)
            
            if arm_status == True:
                pix[0] = GREEN
                pix.write()
                time.sleep(1)
                if act_sensor_cnt == 0:
                    pix[2] = GREEN
                    pix.write()
                if act_sensor_cnt == 1:
                    R1State.value(1)
                    pix[2] = YELLOW
                    pix.write()
                    buffer["R1"] = "1101"
                elif act_sensor_cnt == 2:
                    pix[2] = BLUE
                    pix.write()
                    R2State.value(1)
                    buffer["R2"] = "1102"
                elif act_sensor_cnt == 3:
                    pix[2] = PURPLE
                    pix[1] = ORANGE
                    pix.write()
                    R3State.value(1)
                    buffer["R3"] = "1103"
                elif act_sensor_cnt >= 3:
                    if FG_Arm == True:
                        print("FG status ",FG_Arm)
                        pix[2] = CYAN
                        pix[1] = RED
                        pix.write()
                        R4State.value(1)
                        buffer["R4"] = "1104"
                        buffer["FD"] = "12"
                        
                buffer_json[config['device_info']['device_id']]=buffer
                string_json = json.dumps(buffer_json)
                client.publish(topic_json,string_json)
            else:
                FG_Arm = False
                R1State.value(0)
                R2State.value(0)
                R3State.value(0)
                R4State.value(0)
                buffer["R1"] = '0101'
                buffer["R2"] = '0102'
                buffer["R3"] = '0103'
                buffer["R4"] = '0104'
                buffer["FD"] = '01'
                pix[1] = RED
                pix.write()
                buffer_json[config['device_info']['device_id']]=buffer
                string_json = json.dumps(buffer_json)
                client.publish(topic_json,string_json)
            if time.ticks_diff(currentMillis,previousMillis)>=interval:
                previousMillis = currentMillis
                if not wlan.isconnected():
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
                            client.reconnect()
                            print('client reconnected')
                            break
                        time.sleep(5)
                    
        except :
            print("Connection failed with error:")
            restart_and_reconnect()
            
if __name__ == "__main__":
    main()
