# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 12:27:10 2019

@author: Luke Kurlandski
"""

import serial
import time #package used to reduce communications with serial port

class Shutter:
    '''
    ser: serial port (serial object)
    '''
    
    ser = serial.Serial()
    
    def __init__(self, port, baudrate=9600, timeout=.1, stopbits=1, bytesize=8):
        '''
        Construct an object and configure the serial port.
        #flow control = 1?
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
        
        cmd = command
        if cmd.find('\r') == -1:
            cmd = cmd + '\r'
        if self.ser.is_open == False:
            self.ser.open()
        self.ser.write(cmd.encode())
        if closeAfter == True:
            self.ser.close()
            
    def toggle_shutter(self, pause):
        '''
        Opens the shutter. Pauses for a certain amount of time. Closes
            the shutter.
        (arg1) pause : number of seconds to pause (float)
        '''
        self.writeCommand('ens')
        time.sleep(pause)
        self.writeCommand('ens')
        time.sleep(.05) #prevents the shutter from being overloaded by signals
        
    def __del__(self): #FIXME: possible source of major error
        '''
        Destructor to ensure the serial port is closed.
        (arg1) self
        '''
        
        self.ser.close()
        print("Serial Port Closed:", self.ser.port)
        
def test():
    s = Shutter('COM10')
    s.toggle_shutter(2)
    s.toggle_shutter(1)
    s.ser.close()

test()