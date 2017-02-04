import RPi.GPIO as GPIO
import time

# Variables

# delay = 0.0055
# steps = 5000

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Enable GPIO pins for  ENA and ENB for stepper
# a Green, A1 Dark Blue, A2 Purple - Turning
enable_a = 4
# b Orange, B1 Red, B2 Yellow
enable_b = 18

# Enable pins for IN1-4 to control step sequence

coil_A_1_pin = 27
coil_A_2_pin = 22
coil_B_1_pin = 23
coil_B_2_pin = 24

# Set pin states

GPIO.setup(enable_a, GPIO.OUT)
GPIO.setup(enable_b, GPIO.OUT)

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

# Set ENA and ENB to high to enable stepper

GPIO.output(enable_a, True)
GPIO.output(enable_b, True)

tspeedpwm = GPIO.PWM(enable_a, 50)
tspeedpwm.start(20)

speedpwm = GPIO.PWM(enable_b, 20)
speedpwm.start(20)

# Function for step sequence
def tsetStep(w1, w2):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)

# Right
tsetStep(1,0)
time.sleep(1)

# speedpwm.start(80)
# Left
tsetStep(0,1)
time.sleep(1)

# print "STOP"

def setStep(w1, w2):
    GPIO.output(coil_B_1_pin, w1)
    GPIO.output(coil_B_2_pin, w2)

# Back
setStep(1,0)
time.sleep(15)
# Front
setStep(0,1)
time.sleep(5)


# def setStep(w1, w2, w3, w4):
#  GPIO.output(coil_A_1_pin, w1)
#  GPIO.output(coil_A_2_pin, w2)
#  GPIO.output(coil_B_1_pin, w3)
#  GPIO.output(coil_B_2_pin, w4)

# loop through step sequence based on number of steps

# for i in range(0, steps):
#    setStep(1,0)
#    time.sleep(delay)
#    setStep(0,1)
#    time.sleep(delay)

# for i in range(0, steps):
#    setStep(1,0,1,0)
#    time.sleep(delay)
#    setStep(0,1,1,0)
#    time.sleep(delay)
#    setStep(0,1,0,1)
#    time.sleep(delay)
#    setStep(1,0,0,1)
#    time.sleep(delay)

# Reverse previous step sequence to reverse motor direction

# for i in range(0, steps):
#    setStep(1,0,0,1)
#    time.sleep(delay)
#    setStep(0,1,0,1)
#    time.sleep(delay)
#    setStep(0,1,1,0)
#    time.sleep(delay)
#    setStep(1,0,1,0)
#    time.sleep(delay)

GPIO.output(enable_a, False)
GPIO.output(enable_b, False)
tspeedpwm.stop()
speedpwm.stop()

GPIO.cleanup()
