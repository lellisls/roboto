import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

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
        if direction == 0:
            p1_signal = p2_signal = GPIO.LOW
        else:
            p1_signal = GPIO.HIGH if direction > 0 else GPIO.LOW
            p2_signal = GPIO.LOW if direction > 0 else GPIO.HIGH
        GPIO.output(self.p1, p1_signal)
        GPIO.output(self.p2, p2_signal)
        if speed < 0:
            speed = 0
        elif speed > 100:
            speed = 100
        self.pwm.start(speed)