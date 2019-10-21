# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 11:23:10 2019

@author: Luke Kurlandski
"""

import serial
import time

class Control:
    '''
    Generic class to allow easy use of machinery that uses serial ports
    '''
    
    def __init__(self, port, baudrate, timeout, stopbits, bytesize):
        '''
        Construct a serial object and configure the serial port.
        '''
        
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = timeout
        self.ser.stopbits = stopbits
        self.ser.bytesize = bytesize
        
    def writeCommand(self, command, closeAfter=False):
        '''
        Send any command to a serial port with/without carriage return.
        Arguments:
            (arg1) command (string) : the command to send to the motor
            (arg2) closeAfter (boolean) : if true, close port after command
        '''
        
        cmd = command
        if cmd.find('\r') == -1:
            cmd = cmd + '\r'
        if self.ser.is_open == False:
            self.ser.open()
        self.ser.write(cmd.encode())
        if closeAfter == True:
            self.ser.close()   
            
    def __del__(self): 
        '''
        Destructor to ensure the serial port is closed.
        '''
        
        self.ser.close()
        print("Serial Port Closed:", self.ser.port)
        
class Shutter(Control):
    '''
    Class to control shutter. Derives from Control class.
    '''
    
    def __init__(self, port, baudrate=9600, timeout=.1, stopbits=1, bytesize=8):
        '''
        Contructor calls parent.
        '''
        
        super().__init__(port, baudrate, timeout, stopbits, bytesize)
            
    def toggle_shutter(self, pause):
        '''
        Opens the shutter. Pauses for a certain amount of time. Closes the shutter.
        Arguments:
            (arg1) pause : number of seconds to pause (float)
        '''
        
        self.writeCommand('ens')
        time.sleep(pause)
        self.writeCommand('ens')
        time.sleep(.05) #prevents the shutter from being overloaded by signals

class Motor(Control):
    '''
    Class to control the motot. Derives from Control class.
    '''
    
    def __init__(self, port, baudrate=19200, timeout=.1, stopbits=1, bytesize=8):
        '''
        Contructor calls parent.
        '''
        
        super().__init__(port, baudrate, timeout, stopbits, bytesize)
        
    def moveAbsolute(self, axis, goToPos, delay=0):
        '''
        Move the stage to an absolute location. Wait until motion is complete.
        Arguments:
            (arg2) axis (int) : axis of operation 
            (arg3) goToPos (double) : position to navigate to 
            (arg4) delay (int) : additional time to wait in milliseconds 
        '''
        
        strAxis = str(axis)
        strGoToPos = str(goToPos)
        self.writeCommand(strAxis + 'PA' + strGoToPos)
        self.waitMotionDone(axis, delay)
    
    def waitMotionDone(self, axis, milliseconds=0):
        '''
        Delays until the device is finished moving plus .1 seconds. 
        Arguments: 
            (arg1) axis (int) : axis of operation
        '''
        
        strAxis = str(axis)
        while True:
            self.writeCommand(strAxis + 'MD?')
            try:
                byte = self.ser.read(4)
                bit = str(byte.decode())
            except:
                print('Cannot convert the motor\'s output: ', byte)
            if bit.find('1') != -1:
                return
            else:
                time.sleep(.5)
                
    def configureAxis(self, axis, velocity=1, acceleration=4, moveHome=True):
        '''
        Initial configuration of device.
        Arguments:
            (arg1) axis (int) : axis of operation
            (arg2) velocity (double) : velocity to set device
            (arg3) acceleration (double) : acceleration/decceleration to set device
            (arg4) moveHome (boolean) : moves device to home position if true
        '''
        
        #Turn axis on
        strAxis = str(axis)
        strVelocity = str(velocity)
        strAcceleration = str(acceleration)
        self.writeCommand(strAxis + 'MO')
        #Set velocity
        try:
            self.writeCommand(strAxis + 'VA' + strVelocity)
        except:
            print('Attempting to use an invalid velocity.')
        #Set acceleration/decceleration
        try:
            self.writeCommand(strAxis + 'AC' + strAcceleration)
            self.writeCommand(strAxis + 'AG' + strAcceleration)
        except:
            print('Attempting to use an invalid accleration.')
        #Move home
        if moveHome==True:
            self.writeCommand(strAxis + 'OR0')  #OR0,OR1,OR2...?
            self.waitMotionDone(axis)

def test():
    '''
    Method for internal testing
    '''