# -*- coding: utf-8 -*-
"""
Sample program demonstrating the Motor Control class.

Created on 9/16/19

@author: Luke Kurlandski
"""

from MotorControl import MotorControl

def f1():
    motor = MotorControl(port = 'COM7')
    motor.configureAxis(axis=1, velocity=4, acceleration=4, moveHome=True)
    motor.moveAbsolute(axis=1, goToPos=-1, delay=1000)
    motor.moveAbsolute(axis=1, goToPos=1, delay=1000)
    motor.moveAbsolute(axis=1, goToPos=-1, delay=1000)

f1()
    