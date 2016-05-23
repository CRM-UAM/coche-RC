# coding: utf-8
from __future__ import print_function

import RPi.GPIO as GPIO
import time

from collections import deque
from multiprocessing import Process, Event

#from unittest.mock import Mock
#GPIO = Mock()


class Timer(Process):

    def __init__(self, delay, function, args=[], kwargs={}):
        super(Timer, self).__init__()
        self.delay = delay
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()

    def run(self):
        self.finished.wait(self.delay)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()


class PerpetualTimer(Timer):

    def __init__(self, delay, interval, function, args=[], kwargs={}):
        super(PerpetualTimer, self).__init__(delay, function, args, kwargs)
        self.interval = float(interval)

    def run(self):
        try:
            self.finished.wait(self.delay)
            while not self.finished.is_set():
                self.function(*self.args, **self.kwargs)
                self.finished.wait(self.interval)
        except KeyboardInterrupt:
            self.cancel()


class BatSensor(object):

    def __init__(self, trigger, echo, rango, continuous=None, name=''):
        self.trigger = trigger
        self.echo = echo

        self.name = str(name)

        GPIO.setup(trigger, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)

        self._pulse_start = 0
        self._pulse_end = 0

        self._rango = rango
        self.__trigger_timer = None

        self._avgq = deque(maxlen=5)

        # setup events and callback
        GPIO.add_event_detect(self.echo, GPIO.BOTH)
        GPIO.add_event_callback(self.echo, self._set_times)
        # settle the sensor
        GPIO.output(self.trigger, GPIO.LOW)

        if continuous:
            self.continuous_read(float(continuous))

    def continuous_read(self, seconds):
        sec = float(seconds)
        if not sec > 0:
            raise ValueError('invalid time interval: {}'.format(seconds))

        if self.__trigger_timer is None:
            print("leyendo cada", seconds)
            self.__trigger_timer = PerpetualTimer(2, sec, self._trig)
            self.__trigger_timer.start()

    def stop(self):
        self.__trigger_timer.cancel()
        self.__trigger_timer.join()
        self.__trigger_timer = None

    def _trig(self):
        #print("triggering sensor {}".format(self.name))
        GPIO.output(self.trigger, GPIO.HIGH)
        time.sleep(10e-6)  # 10us
        GPIO.output(self.trigger, GPIO.LOW)

    def _set_times(self, channel):
        value = GPIO.input(channel)
        if value == 1:
            self._pulse_start = time.time()
            # empieza el intervalo, solo necesitamos este valor
            return
        elif value == 0:
            self._pulse_end = time.time()

        if self._pulse_end < self._pulse_start:
            # algo extraño ha pasado y vamos
            # a tener un intervalo negativo
            self._pulse_start = 0
            self._pulse_end = 0

            return

        # Calculate pulse length
        pulse_duration = self._pulse_end - self._pulse_start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s) divided
        # by 2 (RTT) [340 m/s = 17150 cm/s]
        distance = round(pulse_duration * 17150, 2)

        if max(self._rango) > distance > min(self._rango):
            self._avgq.append(distance)
        elif distance < min(self._rango):
            self._avgq.append(min(self._rango))
        else:
            self._avgq.append(max(self._rango))

    @property
    def avg(self):
        if len(self._avgq) == 0:
            return max(self._rango)
        return sum(self._avgq) / len(self._avgq)


if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)

    # trasero
    r_sensor = BatSensor(17, 27, rango=(5, 100), continuous=0.25, name='REAR')
    # izquierda
    fl_sensor = BatSensor(22, 10, rango=(
        5, 100), continuous=0.25, name='FRONT LEFT')
    # derecho
    fr_sensor = BatSensor(9, 11, rango=(
        5, 100), continuous=0.25, name='FRONT RIGHT')

    s = 0
    try:
        while True:
            #time.sleep(0.5)
            #time.sleep(12)
            print("Sensors RE({})\t, FL({})\t, FR({})".format(
                r_sensor.avg, fl_sensor.avg, fr_sensor.avg))
            #print("Sensors RE({})".format(r_sensor.avg))
            #s += 1
            # if s == 5:
            #break

    except KeyboardInterrupt:
        r_sensor.stop()
        fl_sensor.stop()
        fr_sensor.stop()
        pass
    else:
        r_sensor.stop()
        fl_sensor.stop()
        fr_sensor.stop()
        pass

    GPIO.cleanup()
