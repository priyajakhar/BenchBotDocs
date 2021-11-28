from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
PUL = 17
DIR = 27
ENA = 22
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

revs = 3
pulses = 3200 #pusles that the stepper motor driver is working with
delay = 0.0001 #final speed that we want
acctime = int(pulses/20)  #the bigger the division term, the faster the acceleration
durationFwd = (pulses*revs)-(acctime*9) #we take out 9 times of acctime to get true revs

def move():
    GPIO.output(DIR, GPIO.HIGH)
    GPIO.output(ENA, GPIO.HIGH)
    sleep(.5)
    accdelay = delay*10 #speed that we start with
    
    while (accdelay>=delay): #loop for acceleration
        for x in range(acctime): 
            GPIO.output(PUL, GPIO.HIGH)
            sleep(accdelay)
            GPIO.output(PUL, GPIO.LOW)
            sleep(accdelay)
        accdelay=accdelay-delay
    
    for x in range(durationFwd): #loop for moving at desired speed
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    sleep(.5)
    return

print('Motor moving now...')
move()

GPIO.cleanup()
print('Motion Completed')