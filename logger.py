import time
import machine

rtc = machine.RTC()


f = open('log.txt','w')

def log(event):
    timestamp = rtc.datetime()
    timestring = "%04d-%02d-%02d-%02d-%02d-%02d"%(timestamp[0:3] + timestamp[4:7])
    try:
        log = timestring + "\n"
        with open('log.txt','at') as f
        f.write(log)
    except:
        print("Problem saving a file")
    
    

msg = "some Information"
log(msg)