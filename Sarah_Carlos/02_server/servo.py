# coding: utf-8
from __future__ import print_function

import RPi.GPIO as GPIO


class Servo(object):

    def __init__(self, pin, input_range, servo_range, freq=100, trim=0.0):
        self.pin = pin
        self._trim = float(trim)

        GPIO.setup(pin, GPIO.OUT)

        self.input_range = input_range
        self.servo_range = servo_range

        self.pwm = GPIO.PWM(pin, freq)
        self.angle = 0.0
        self.start()

    @property
    def trim(self):
        """
        value: float. Corrige la posicion del servo
        """
        return self._trim

    @trim.setter
    def trim(self, value):
        self._trim = float(value)
        self.update(0.0)

    def start(self):
        self.pwm.start(self._duty())

    def stop(self):
        self.pwm.stop()

    def _duty(self):
        effective_angle = self._map(self.angle)
        return float(effective_angle) / 10.0 + 2.5

    def update(self, angle):
        new_angle = self.angle + angle

        # si ya estamos al maximo/minimo, no se hace nada
        if new_angle < self.input_range[0] or new_angle > self.input_range[1]:
            return self.angle

        effective_angle = float(new_angle + self.trim)

        maxi = self.input_range[1] + self.trim
        mini = self.input_range[0] + self.trim
        if effective_angle > maxi:  # max
            self.angle = maxi
        elif effective_angle < mini:
            self.angle = mini
        else:
            self.angle = effective_angle

        self.pwm.ChangeDutyCycle(self._duty())
        return self.angle

    def _map(self, x):
        inmin = self.input_range[0]
        inmax = self.input_range[1]

        outmin = self.servo_range[0]
        outmax = self.servo_range[1]
        return (x - inmin) * (outmax - outmin) / (inmax - inmin) + outmin

if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)

    s = Servo(18, (-45, 45), (72.5, 162.5))

    try:
        while True:
            instr = input('New angle: ')
            if instr == 'q':
                break

            ang = float(instr)
            s.update(-s.angle + ang)  # vuelve a 0, mas el angulo

            print("Angle:", s.angle)

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
