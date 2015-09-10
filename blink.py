import RPi.GPIO as GPIO  
import time  
import sys

def blink(pin):  
        GPIO.output(pin,GPIO.HIGH)  
        time.sleep(0.1)  
        GPIO.output(pin,GPIO.LOW)  
        time.sleep(0.1)  
        return  

GPIO.setmode(GPIO.BCM)  
GPIO.setup(5, GPIO.OUT)  
GPIO.setup(6, GPIO.OUT)  
GPIO.setup(12, GPIO.OUT)  

colors = {
	'blue': 5,
	'red': 6,
	'green': 12
}

for i in range(0,50):  
        blink(colors.get(sys.argv[1]))  
GPIO.cleanup()
