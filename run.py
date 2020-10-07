import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

p1 = 18
p2 = 17
p3 = 27
p4 = 22

class Motor:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        GPIO.setup(self.p1, GPIO.OUT)
        GPIO.setup(self.p2, GPIO.OUT)
        self.pwm = None
    
    def stop(self):
        if self.pwm is not None:
            self.pwm.stop()
            self.pwm = None
        GPIO.output(self.p1, GPIO.LOW)
        GPIO.output(self.p2, GPIO.LOW)

    def run(self, speed: float, direction: float):
        self.stop()
        if direction != 0 and speed != 0:
            speed_pin = self.p1 if direction > 0 else self.p2
            direction_pin = self.p2 if direction > 0 else self.p1
            self.pwm = GPIO.PWM(speed_pin, 100)
            GPIO.output(direction_pin, GPIO.LOW)
            self.pwm.start(speed)

def run():
    m1 = Motor(p1, p2)
    m2 = Motor(p3, p4)
    speed = 100

    m1.run(speed, 1)
    m2.run(speed, -1)

    time.sleep(5)

    m1.stop()
    m2.stop()

    time.sleep(.1)

    m1.run(speed, -1)
    m2.run(speed, 1)

    time.sleep(5)

try:
    run()
finally:
    GPIO.cleanup()