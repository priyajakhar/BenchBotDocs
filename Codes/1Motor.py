from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
PUL = 17
DIR = 27
ENA = 22
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

revs = 1
pulses = 3200 #pusles that the stepper motor driver is working with
timeperiod = 0.0001 #0.0001 #final speed that we want
ac_dac_period = timeperiod*5 #speed that we start with
ac_dac_time = int(pulses/30)  #the bigger the division term, the faster the acceleration, acceleration rate
durationFwd = (pulses*revs)-(ac_dac_time*12) #we take out 9 times of acctime to get true revs

def start():
    GPIO.output(DIR, GPIO.HIGH)
    GPIO.output(ENA, GPIO.HIGH)
    sleep(.5)
    
    ac_period = ac_dac_period
    while (ac_period>=timeperiod): #loop for acceleration
        for x in range(ac_dac_time): 
            GPIO.output(PUL, GPIO.HIGH)
            sleep(ac_period)
            GPIO.output(PUL, GPIO.LOW)
            sleep(ac_period)
        ac_period=ac_period-timeperiod
    return
       
def move():   
    for x in range(durationFwd): #loop for moving at desired speed
        GPIO.output(PUL, GPIO.HIGH)
        sleep(timeperiod)
        GPIO.output(PUL, GPIO.LOW)
        sleep(timeperiod)
    return

def stop():    
    dac_period = timeperiod
    while (dac_period<=ac_dac_period): #loop for deacceleration
        for x in range(ac_dac_time): 
            GPIO.output(PUL, GPIO.HIGH)
            sleep(dac_period)
            GPIO.output(PUL, GPIO.LOW)
            sleep(dac_period)
        dac_period=dac_period+timeperiod
    
    GPIO.output(ENA, GPIO.LOW)
    sleep(.5)        
    return


#sleep(5)
print('Motor moving now...')
start()
move()
stop()

GPIO.cleanup()
print('Motion Completed')