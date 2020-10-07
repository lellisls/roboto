import RPi.GPIO as GPIO
import time


p1 = 18
p2 = 17
p3 = 27
p4 = 22

def setup():        
    GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)

    GPIO.setup(p1, GPIO.OUT)
    GPIO.setup(p2, GPIO.OUT)
    GPIO.setup(p3, GPIO.OUT)
    GPIO.setup(p4, GPIO.OUT)

def run():
    # Drive motor clockwise
    GPIO.output(p1, GPIO.LOW)
    GPIO.output(p2, GPIO.HIGH)
    GPIO.output(p3, GPIO.LOW)
    GPIO.output(p4, GPIO.HIGH)

    # GPIO.output(p3, GPIO.HIGH)
    # GPIO.output(p4, GPIO.LOW)

    time.sleep(1000)

    # GPIO.output(p3, GPIO.LOW)
    # GPIO.output(p4, GPIO.LOW)

try:
    setup()
    run()
finally:
    GPIO.cleanup()