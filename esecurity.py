import time
import neopixel
from machine import Pin
import shared
import machine
import json

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


class call_loop:
    def __init__(self):
        pass
    
    def callback(self,topic_cmd,msg):
        decoded_topic = topic_cmd.decode('utf-8').strip()
        decoded_msg = msg.decode('utf-8').strip()
        print("decoded_topic:"+decoded_topic)
        print("decoded_msg:"+decoded_msg)
        if decoded_topic.endswith("FD"):
            print("decoded_topic:"+decoded_topic)
            if decoded_msg == '12':
                shared.buffer["FD"] = '12'
                shared.FG_Arm = True
                print("shared.FG_Arm ",shared.FG_Arm)
                shared.string_json = json.dumps(shared.buffer)
            elif decoded_msg == '01':
                shared.buffer["FD"] == '01'
                shared.FG_Arm = False
                print("shared.FG_Arm ",shared.FG_Arm)
                shared.string_json = json.dumps(shared.buffer)
            else:
                print("Invalid Input !")
        elif decoded_topic.endswith("D"):
            print("decoded_topic:"+decoded_topic)
            if decoded_msg == '00':
                shared.buffer["D"] = decoded_msg
                shared.arm_status = False
                shared.string_json = json.dumps(shared.buffer)
                pix[0] = RED
                pix.write()
            elif decoded_msg == '10':
                shared.buffer["D"] = decoded_msg
                shared.arm_status = True
                shared.string_json = json.dumps(shared.buffer)
                pix[0] = GREEN
                pix.write()
                print("shared.arm_status is ", shared.arm_status)
            else:
                print("Invalid input!!")
        elif decoded_topic.endswith("RR"):
            if decoded_msg == '05':
                shared.R1State.value(0)
                shared.R2State.value(0)
                shared.R3State.value(0)
                shared.R4State.value(0)
                shared.active_sensor =[0,0,0,0]
                shared.buffer["R1"] = '0101'
                shared.buffer["R2"] = '0102'
                shared.buffer["R3"] = '0103'
                shared.buffer["R4"] = '0104'
                shared.string_json = json.dumps(shared.buffer)
        elif decoded_topic.endswith("MR"):
            if decoded_msg == '06':
                machine.reset()
        elif decoded_topic.endswith("R1"):
            if decoded_msg == '0101':
                shared.buffer["R1"] = decoded_msg
                shared.R1State.value(0)
                shared.string_json = json.dumps(shared.buffer)
                print("R1 state ",shared.R1State.value())
            elif decoded_msg == '1101' and shared.arm_status:
                shared.buffer["R1"] = decoded_msg
                shared.string_json = json.dumps(shared.buffer)
                shared.R1State.value(1)
            else:
                print("Invalid input")
            
        elif decoded_topic.endswith("R2"):
            if decoded_msg == '0102':
                shared.buffer["R2"] = decoded_msg
                shared.string_json = json.dumps(shared.buffer)
                shared.R2State.value(0)
            elif decoded_msg == '1102' and shared.arm_status:
                shared.buffer["R2"] = decoded_msg
                shared.string_json = json.dumps(shared.buffer)
                shared.R2State.value(1)
            else:
                print("Invalid input")
        elif decoded_topic.endswith("R3"):
            if decoded_msg == '0103':
                shared.buffer["R3"] = decoded_msg
                shared.R3State.value(0)
                shared.string_json = json.dumps(shared.buffer)
            elif decoded_msg == '1103' and shared.arm_status:
                shared.buffer["R3"] = decoded_msg
                shared.string_json = json.dumps(shared.buffer)
                shared.R3State.value(1)
            else:
                print("Invalid input")
        elif decoded_topic.endswith("R4"):
            if decoded_msg == '0104':
                shared.buffer["R4"] = decoded_msg
                shared.string_json = json.dumps(shared.buffer)
                shared.R4State.value(0)
            elif decoded_msg == '1104' and shared.arm_status:
                shared.buffer["R4"] = decoded_msg
                shared.string_json = json.dumps(shared.buffer)
                shared.R4State.value(1)
            else:
                print("Invalid input")       
        shared.string_json = json.dumps(shared.buffer)
        shared.client.publish(shared.topic_json,shared.string_json)
    
        
        
    def main(self):
        time.sleep(0.5)
        try:
            time.sleep(1)
            shared.client.check_msg()
            if shared.arm_status == True:
                shared.pix[0] = shared.GREEN
                shared.pix.write()
                time.sleep(1)
                if shared.act_sensor_cnt == 0:
                    sared.pix[2] = shared.GREEN
                    shared.pix.write()
                if shared.act_sensor_cnt == 1:
                    shared.R1State.value(1)
                    shared.pix[2] = shared.YELLOW
                    shared.pix.write()
                    shared.buffer["R1"] = "1101"
                elif shared.act_sensor_cnt == 2:
                    shared.pix[2] = shared.BLUE
                    shared.pix.write()
                    shared.R2State.value(1)
                    shared.buffer["R2"] = "1102"
                elif shared.act_sensor_cnt == 3:
                    shared.pix[2] = shared.PURPLE
                    shared.pix[1] = shared.ORANGE
                    shared.pix.write()
                    shared.R3State.value(1)
                    shared.buffer["R3"] = "1103"
                elif shared.act_sensor_cnt >= 3:
                    if shared.FG_Arm == True:
                        print("FG status ",shared.FG_Arm)
                        shared.pix[2] = shared.CYAN
                        shared.pix[1] = shared.RED
                        shared.pix.write()
                        shared.R4State.value(1)
                        shared.buffer["R4"] = "1104"
                        shared.buffer["FD"] = "12"
                        
                shared.buffer_json[shared.config['device_info']['device_id']]=shared.buffer
                shared.string_json = json.dumps(shared.buffer_json)
                shared.client.publish(shared.topic_json,shared.string_json)
            else:
                shared.FG_Arm = False
                shared.R1State.value(0)
                shared.R2State.value(0)
                shared.R3State.value(0)
                shared.R4State.value(0)
                shared.buffer["R1"] = '0101'
                shared.buffer["R2"] = '0102'
                shared.buffer["R3"] = '0103'
                shared.buffer["R4"] = '0104'
                shared.buffer["FD"] = '01'
                shared.pix[1] = shared.RED
                shared.pix.write()
                shared.buffer_json[shared.config['device_info']['device_id']]=shared.buffer
                shared.string_json = json.dumps(shared.buffer_json)
                shared.client.publish(shared.topic_json,shared.string_json)
        except Exception as e:
            print("Connection failed with error:",e)
            shared.pix[3] = shared.RED
            shared.pix.write()
            time.sleep(4)
            machine.reset()	


#p2.main()
