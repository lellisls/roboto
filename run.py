import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pwm1 = 13
p1 = 18
p2 = 17

pwm2 = 12
p3 = 27
p4 = 22

class Motor:
    def __init__(self, p1, p2, pwm):
        self.p1 = p1
        self.p2 = p2
        self.pwm_pin = pwm
        GPIO.setup(self.p1, GPIO.OUT)
        GPIO.setup(self.p2, GPIO.OUT)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwm_pin, 100)

    def stop(self):
        GPIO.output(self.p1, GPIO.LOW)
        GPIO.output(self.p2, GPIO.LOW)
        self.pwm.stop()

    def run(self, speed: float, direction: float):
        p1_signal = GPIO.HIGH if direction > 0 else GPIO.LOW
        p2_signal = GPIO.LOW if direction > 0 else GPIO.HIGH
        GPIO.output(self.p1, p1_signal)
        GPIO.output(self.p2, p2_signal)
        self.pwm.start(speed)

def run():
    m1 = Motor(p1, p2, pwm1)
    m2 = Motor(p3, p4, pwm2)
    speed = 40

    FW = 1
    BW = -1
    ST = 0

    commands = [
        (FW,FW, 1),
        (BW,BW, 1),
        (FW,BW, 1),
        (FW,FW, 1),
        (BW,FW, 1),
        (FW,FW, 1),
        (BW,FW, 1),
        (FW,FW, 1),
    ]

    while True:
        for (dir1, dir2, sleep_time) in commands:        
            m1.run(speed, dir1)
            m2.run(speed, dir2)

            time.sleep(sleep_time)

try:
    run()
finally:
    GPIO.cleanup()