# -*- coding: utf-8 -*-
"""
Motor Control class. Provide functional control of Newport Universal 
Motion Controller/Driver through a USB->Serial Port connection.

Created on 9/16/19
Last Update on 9/16/19

@author: Luke Kurlandski
"""

import serial #Library of the Serial-Port
#import serial.tools.list_ports #Library for listing the COM ports
import time

class MotorControl:
    '''
    ser: serial port (serial object)
    '''
    
    ser = serial.Serial()
    
    def __init__(self, port, baudrate=19200, timeout=.1, stopbits=1, bytesize=8):
        '''
        Construct an object and configure the serial port.
        '''
        
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = timeout
        self.ser.stopbits = stopbits
        self.ser.bytesize = bytesize
        
    def writeCommand(self, command, closeAfter=False):
        '''
        Send any command to a serial port.
        (arg1) self 
        (arg2) command: the command to send to the motor (string)
        (arg3) closeAfter: close port after command, if true (boolean)
        '''
        
        if command.find('\r') == -1:
            command = command + '\r'
        if self.ser.is_open == False:
            self.ser.open()
        self.ser.write(command.encode())
        if closeAfter == True:
            self.ser.close()   
            
    def moveAbsolute(self, axis, goToPos, delay=100):
        '''
        Move the stage to an absolute location. Wait until motion is complete.
        (arg1) self
        (arg2) axis: axis of operation (int)
        (arg3) goToPos: position to navigate to (double)
        (arg4) delay: additional time to wait in milliseconds (int)
        '''
        
        strAxis = str(axis)
        strGoToPos = str(goToPos)
        self.writeCommand(strAxis + 'PA' + strGoToPos)
        self.waitMotionDone(axis, delay)
    
    def waitMotionDone(self, axis, milliseconds=100):
        '''
        Delays until the device is finished moving plus .1 seconds. 
        (arg1) self 
        (arg2) axis: axis of operation (int)
        '''
        
        strAxis = str(axis)
        #self.writeCommand(strAxis + 'WS' + str(milliseconds))
        while True:
            self.writeCommand(strAxis + 'MD?')
            bit = int(self.ser.read(4).decode())
            if bit == 1:
                return
            else:
                time.sleep(.5)
                
    def configureAxis(self, axis, velocity, acceleration, moveHome=True):
        '''
        Initial configuration of device.
        (arg1) self
        (arg2) axis: axis of operation (int)
        (arg3) velocity: velocity to set device (double)
        (arg4) acceleration: acceleration/decceleration to set device (double)
        (arg5) moveHome: moves device to home position if true (boolean)
        '''
        
        #Turn axis on
        strAxis = str(axis)
        strVelocity = str(velocity)
        strAcceleration = str(acceleration)
        self.writeCommand(strAxis + 'MO')
        #Compute velocity
        self.writeCommand(strAxis + 'VU?')
        strMaxVelocity = self.ser.read(6).decode()  #5 sig figures
        try:
            maxVelocity = float(strMaxVelocity)
        except:
            print('Failure acquiring maximum velocity')
            return
        if velocity <= maxVelocity:
            self.writeCommand(strAxis + 'VA' + strVelocity)
        else:
            print('Attempting to use an invalid velocity.' +
                  'Setting velocity to max: ' + strMaxVelocity)
            self.writeCommand(strAxis + 'VA' + strMaxVelocity)
        #Compute acceleration/decceleration
        self.writeCommand(strAxis + 'AU?')
        strMaxAcceleration = self.ser.read(10).decode()[3:9] #5 sig figures
        maxAcceleration = float(strMaxAcceleration)
        if acceleration <= maxAcceleration:
            self.writeCommand(strAxis + 'AC' + strAcceleration)
            self.writeCommand(strAxis + 'AG' + strAcceleration)
        else:
            print('Attempting to use an invalid accleration.' +
                  'Setting acceleration to max: ' + strMaxAcceleration)
            self.writeCommand(strAxis + 'AC' + strMaxAcceleration)
            self.writeCommand(strAxis + 'AG' + strMaxAcceleration)
        #Move home
        if moveHome==True:
            self.writeCommand(strAxis + 'OR0')  #OR0,OR1,OR2...?
            self.waitMotionDone(axis)
    
    def __del__(self): #FIXME: possible source of major error
        '''
        Destructor to ensure the serial port is closed.
        (arg1) self
        '''
        
        self.ser.close()
        print("Serial Port Closed:", self.ser.port)