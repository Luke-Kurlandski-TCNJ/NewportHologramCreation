# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 09:09:37 2019

@author: laserlab
"""

from MotorControl import MotorControl #file with MotorControl class
from ShutterControl import ShutterControl

def testMotor():
    '''
    Testing indicates motor functionality, except for turn axis 1 on
    '''
    motor = MotorControl(port='COM10')
    motor.configureAxis(axis=1, velocity=1.0, acceleration=4, moveHome=True)
    motor.configureAxis(axis=2, velocity=1.0, acceleration=4, moveHome=True)
    motor.moveAbsolute(axis=1, goToPos=1)
    motor.moveAbsolute(axis=2, goToPos=1)
    motor.moveAbsolute(axis=1, goToPos=-1)
    motor.moveAbsolute(axis=2, goToPos=-1)
    motor.ser.close()
    
def testShutter():
    shutter = ShutterControl('COM11')
    shutter.toggle_shutter(1)
    shutter.toggle_shutter(2)
    shutter.toggle_shutter(3)    

def testBoth():
    motor = MotorControl(port='COM10')
    shutter = ShutterControl('COM11')
    motor.configureAxis(axis=1, velocity=1.0, acceleration=4, moveHome=True)
    motor.configureAxis(axis=2, velocity=1.0, acceleration=4, moveHome=True)
    
    motor.moveAbsolute(axis=1, goToPos=1)
    motor.moveAbsolute(axis=2, goToPos=1)
    shutter.toggle_shutter(1)
    motor.moveAbsolute(axis=1, goToPos=-1)
    motor.moveAbsolute(axis=2, goToPos=-1)
    shutter.toggle_shutter(2)
    
testBoth()
#testMotor()
