import socket
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Distance sensor pins
TRIG = 4
ECHO = 18

# Motor pins
out1 = 27
out2 = 17
out3 = 22
out4 = 23

# Setup pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)

time.sleep(0.5)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("172.20.10.2",1234))

# Vars for distance sensor
last_time = time.time()
start = 0
end = 0
sig_time = 0
distance = 0

# Vars for motor
i=0
positive=0
negative=0
y=0

try:
    while True:
      # Receive and decode the data
        msg = s.recv(4)
        msg = msg.decode("utf-8")
        pos = (int(msg) + 280) / 20
        
        GPIO.output(out1,GPIO.LOW)
        GPIO.output(out2,GPIO.LOW)
        GPIO.output(out3,GPIO.LOW)
        GPIO.output(out4,GPIO.LOW)
        
        # Check distance ever 0.05 seconds
        time_since_last = time.time() - last_time
        
        if time_since_last >= 0.05:
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
            
            while GPIO.input(ECHO) == False:
                start = time.time()

            while GPIO.input(ECHO) == True:
                end = time.time()
                
            sig_time = end-start

            distance = sig_time/0.000058
            last_time = time.time()
            print('Disctance: {} cm'.format(distance))
            print('Position: {}'.format(pos))
            
        # If the target position is less than the actual distance, move it closer
        if pos <= distance and distance >= 5 and not (distance - 0.5 <= pos and pos <= distance + 0.5):
            for y in range(40,0,-1):
                if negative==1:
                    if i==7:
                        i=0
                    else:
                        i=i+1
                    y=y+2
                    negative=0
                positive=1
                #print((x+1)-y)
                if i==0:
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==1:
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==2:  
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==3:    
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==4:  
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==5:
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==6:    
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==7:    
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(0.0003)
                  #time.sleep(1)
                if i==7:
                    i=0
                    continue
                i=i+1
            
        # Or move it further if the position is further away
        elif pos >= distance and distance <= 23 and not (distance + 0.5 >= pos and pos  >= distance - 0.5):
            #moveLeft()
            for y in range(40,0,-1):
                if positive==1:
                    if i==0:
                        i=7
                    else:
                        i=i-1
                    y=y+3
                    positive=0
                negative=1
                #print((x+1)-y) 
                if i==0:
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==1:
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==2:  
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==3:    
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.HIGH)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==4:  
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.LOW)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==5:
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.HIGH)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==6:    
                    GPIO.output(out1,GPIO.LOW)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(0.0003)
                  #time.sleep(1)
                elif i==7:    
                    GPIO.output(out1,GPIO.HIGH)
                    GPIO.output(out2,GPIO.LOW)
                    GPIO.output(out3,GPIO.LOW)
                    GPIO.output(out4,GPIO.HIGH)
                    time.sleep(0.0003)
                  #time.sleep(1)
                if i==0:
                    i=7
                    continue
                i=i-1

except KeyboardInterrupt:
    GPIO.cleanup()
        
