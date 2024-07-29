from machine import Pin
import json
import ota
client = None
wlan = 0
arm_status = True
FG_Arm = False
act_sensor_cnt = 0

R1State = Pin(2,Pin.OUT)
R2State = Pin(3,Pin.OUT)
R3State = Pin(4,Pin.OUT)
R4State = Pin(5,Pin.OUT)
active_sensor=[0,0,0,0]

f = open('config.json',"r")
config = json.load(f)

buffer = {"D":'10',"FD":"01","S1":'01',"S2":'02',"S3":'03',"S4":'04',"R1":'0101',"R2":'0102',"R3":'0103',"R4":'0104',"HB":'1'}
string_json = json.dumps(buffer)
buffer_json ={}

topic_json = config['device_info']['c_code']+'/'+config['device_info']['a_code']+'/'+config['device_info']['s_code']+'/'+config['device_info']['s_topic']+'/'+config['device_info']['device_id']
topic_cmd = config['device_info']['c_code']+"/"+config['device_info']['a_code']+"/"+config['device_info']['s_code']+"/CC/"+config['device_info']['device_id']
topic_hb = config['device_info']['c_code']+"/"+config['device_info']['a_code']+"/"+config['device_info']['s_code']+"/HB/"



