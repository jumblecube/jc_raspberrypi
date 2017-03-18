import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Enable GPIO pins for  ENA and ENB for stepper
# a Green, A1 Dark Blue, A2 Purple - Turning
enable_a = 4
# b Orange, B1 Red, B2 Yellow
enable_b = 18
# Enable GPIO pins for IN1-4 to control step sequence
coil_A_1_pin = 27
coil_A_2_pin = 22
coil_B_1_pin = 23
coil_B_2_pin = 24
# Enable GPIO pins for Ultrasonic Sensor
trig_pin = 25
echo_pin = 12

# Set pin states
#GPIO.setup(enable_a, GPIO.OUT)
GPIO.setup(enable_b, GPIO.OUT)
#GPIO.setup(coil_A_1_pin, GPIO.OUT)
#GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# Set ENA and ENB to high to enable stepper

#GPIO.output(enable_a, True)
GPIO.output(enable_b, True)

# Set PWM for turing and speed motors
#tspeedpwm = GPIO.PWM(enable_a, 100)
speedpwm = GPIO.PWM(enable_b, 100)

# Set Trigger to low and wait for Sensor to settle
GPIO.output(trig_pin, False)
time.sleep(2)

speedpwm.start(50)

# Function for step sequence
#def tsetStep(w1, w2):
    #GPIO.output(coil_A_1_pin, w1)
    #GPIO.output(coil_A_2_pin, w2)

def setStep(w1, w2):
    GPIO.output(coil_B_1_pin, w1)
    GPIO.output(coil_B_2_pin, w2)

i=0

while True:  
    i=i+1
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    while GPIO.input(echo_pin)==0:
        pulse_start = time.time()

    while GPIO.input(echo_pin)==1:
        pulse_end = time.time()    

    pulse_duration = pulse_end - pulse_start
    distance = round(pulse_duration * 17150,2)
    print "Distance ",i," : ",distance,"cm"

    if i==25:
        break

    if distance <= 15:
        setStep(0,0)
        print "In distance <=15 if statement :",i
        continue
    else:
        setStep(0,1)
        time.sleep(0.2)
        print "In distance <=15 else statement :",i
        continue

#GPIO.output(enable_a, False)
GPIO.output(enable_b, False)
speedpwm.stop()

GPIO.cleanup()
