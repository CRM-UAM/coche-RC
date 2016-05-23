# coding: utf-8
from __future__ import print_function


import Pyro4

#from MockRCCar import MockRCCar as RCCar
from RCCar import RCCar as RCCar


def main():

    # make an instance of the object
    rccar = RCCar()

    ip = '192.168.12.2'
    #ip = 'localhost'

    # make a Pyro daemon
    daemon = Pyro4.Daemon(host=ip, port=55555)
    uri = daemon.register(rccar, "rccar")

    print("Ready. Object uri =", uri)

    # start the event loop of the server to wait for calls
    daemon.requestLoop()


if __name__ == '__main__':
    main()
