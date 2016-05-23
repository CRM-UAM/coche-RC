# coding: utf-8
from __future__ import print_function

import RPi.GPIO as GPIO
import time


class DCMotor(object):
    """
    ENA 	IN1 	IN2 	Description
    0 		N/A 	N/A 	Motor is off
    1 		0 		0 		Motor is stopped (brakes)
    1 		0 		1 		Motor is on and turning backwards
    1 		1 		0 		Motor is on and turning forwards
    1 		1 		1 		Motor is stopped (brakes)
    """

    def __init__(self, enable_pin, in1, in2):
        GPIO.setup(enable_pin, GPIO.OUT)
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)

        self.enable = enable_pin
        self.in1 = in1
        self.in2 = in2

        self.power = 0

    def forward(self):  # velocidad en porcentaje
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        self.power = 1
        GPIO.output(self.enable, GPIO.HIGH)
        return self.power

    def backward(self):  # velocidad en porcentaje
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)
        self.power = -1
        GPIO.output(self.enable, GPIO.HIGH)
        return self.power

    def brake(self):
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.HIGH)
        self.power = 0
        GPIO.output(self.enable, GPIO.HIGH)
        return self.power

    def release(self):
        self.power = 0
        GPIO.output(self.enable, GPIO.LOW)
        return self.power


if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)

    s = DCMotor(20, 6, 13)

    try:
        while True:
            instr = input('New speed: ')
            if instr == 'quit':
                break

            sp = float(instr)
            if sp > 0:
                s.forward()
            elif sp < 0:
                s.backward()
            else:
                s.release()

            print("Speed:", sp)

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
