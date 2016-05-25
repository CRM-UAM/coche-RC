# coding: utf-8
from __future__ import print_function

import RPi.GPIO as GPIO
from servo import Servo
from dcmotor import DCMotor
#from batsensor import BatSensor


class RCCar(object):

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.direction = Servo(27, (-45, 45), (72.5, 162.5))  # board pin: 13
        self.direction.trim = -1
        self.front_motor = DCMotor(20, 6, 13)  # board pin: 38, 31, 33
        self.rear_motor = DCMotor(21, 19, 26)  # board pin: 40, 35, 37

        self.speed = 0
        self.w_angle = self.direction.angle
        self.mov = 'quieto'

        """
        self.rear_sensor = BatSensor(17, 27, rango=(10, 80), continuous=0.2)  # board pin: 11, 13
        self.front_left_sensor = BatSensor(22, 10, rango=(10, 80), continuous=0.2)  # board pin: 15, 19
        self.front_right_sensor = BatSensor(9, 11, rango=(10, 80), continuous=0.2)  # board pin: 21, 23
        """

    def stop(self):
        self.in_use = False

        # dejar el coche frenando

    def turn_left(self):
        if self.survival_instinct():
            return -self.direction.angle

        print("Izquierda:", self.direction.angle)
        return -self.direction.update(-5)

    def turn_right(self):
        if self.survival_instinct():
            return -self.direction.angle

        print("Derecha:", self.direction.angle)
        return -self.direction.update(5)

    def forward(self):
        self.mov = 'adelante'
        if self.survival_instinct():
            return self.speed

        if self.speed != 1:
            self.speed = 1
        
        self.front_motor.forward()
        self.rear_motor.forward()
        print("Acelero hacia delante")
        return self.speed

    def backward(self):
        self.mov = 'atras'
        if self.survival_instinct():
            return self.speed

        if self.speed != -1:
            self.speed = -1
        
        self.front_motor.backward()
        self.rear_motor.backward()
        print("Acelero hacia atras")
        return self.speed

    def decelerate(self):
        if self.mov != 'quieto':
            print("Desacelero")
            #self.mov = 'quieto'
            self.front_motor.release()
            self.rear_motor.release()

    def survival_instinct(self):
        return False
    
    def survival_instinct_not_in_use(self):
        """ esta funcion no es ta en uso """
        limit = 0.8 * max(self.front_left_sensor._rango)
        
        rear = self.rear_sensor.avg
        left = self.front_left_sensor.avg
        right = self.front_right_sensor.avg

        print("sensores R({}), FL({}), FR({})".format(rear, left, right))
        
        if self.mov == 'atras' and rear < limit:
            self.brake()
            return True

        elif self.mov == 'adelante':
            if right < limit and left < limit:
                self.brake()
                return True
            elif right < limit:
                self.brake()
                return True
            elif left < limit:
                self.brake()
                return True

        return False

    def straight(self):
        if self.survival_instinct():
            return -self.direction.angle

        self.direction.update(-self.direction.angle)
        return -self.direction.angle

    def brake(self):
        print("Freno")
        self.mov = 'quieto'
        self.front_motor.brake()
        self.rear_motor.brake()
