#Car Distance Sensor
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

trig_pin = 25
echo_pin = 12

print "Distance Measurement in Progress"

GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

GPIO.output(trig_pin, False)
print "Waiting for Sensor to settle"
time.sleep(2)

for i in range (0,5):
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    while GPIO.input(echo_pin)==0:
        pulse_start = time.time()
        #print "pulse_start : ",pulse_start

    while GPIO.input(echo_pin)==1:
        pulse_end = time.time()
        #print "pulse_end : ",pulse_end

    pulse_duration = pulse_end - pulse_start

    #print "pulse_duration : ",pulse_duration

    distance = round(pulse_duration * 17150,2)

    print "Distance ",i," : ",distance,"cm"

    time.sleep(3)

GPIO.cleanup()
    
