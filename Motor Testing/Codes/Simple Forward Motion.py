from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
PUL = 17
DIR = 27
ENA = 22
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

revs = 2
#3200 with pulse 0.0001/0.001/0.01 with V=12.5 gives perfect 1 rotation
durationFwd = 3200*revs # duration motor spin
# delay = 0.0001 gives 
delay = 0.0001 # set the time between pulses, the lower the faster the motor

def move():
    GPIO.output(DIR, GPIO.HIGH)
    GPIO.output(ENA, GPIO.HIGH)
    sleep(.5)
    
    for x in range(durationFwd): 
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    
    #GPIO.output(ENA, GPIO.LOW)
    sleep(.5)
    return

#sleep(2)
print('Motor moving now...')
move()

GPIO.cleanup()
print('Motion Completed')