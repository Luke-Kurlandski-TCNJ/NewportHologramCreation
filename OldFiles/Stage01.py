# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:02:06 2019

@author: xyz
"""

import serial #Library of the Serial-Port
import serial.tools.list_ports #Library for listing the COM ports
'''
comlist = serial.tools.list_ports.comports()
print(comlist)
'''
port = 'COM7'
baudrate = 19200
timeout = 0.1
stopbits = 1
bytesize = 8

ser = serial.Serial(port, baudrate, timeout=timeout, stopbits=stopbits, bytesize=bytesize)
ser.close()

def writeCommand(ser, command):
    '''
    Send any command to a serial port
    Use arg1 (port object) port to send arg2 (string) command to the device 
    '''
    
    if command.find('\r') == -1:
        command = command + '\r'
    ser.open()
    ser.write(command.encode())
    ser.close()
    
def moveAbsolute(ser, axis, goToPos):
    '''
    
    '''
    writeCommand(ser, str(axis) + 'PA' + '+10')
    writeCommand(ser, str(axis) + 'WF')
    
def configureAxis(ser, axis, velocity, acceleration, moveHome=True):
    '''
    Initial configuration of device.
    Use the port (arg1:port object) to set the axis's (arg2:int)
    velocity (arg3:int) and acceleration/decceleration (arg4:int).
    Moves the axis to Home position if moveHome (arg5:boolean) is true.
    '''
    
    #Turn axis on
    writeCommand(ser, str(axis) + 'MO')
    #Compute velocity
    ser.open()
    maxVelocity = ser.write((str(axis) + 'VU?').encode()) #value is 4
    ser.close()
    if velocity <= maxVelocity:
        writeCommand(ser, str(axis) + 'VA' + str(velocity))
    else:
        print('Attempting to use an invalid velocity')
        quit()
    #Compute acceleration/decceleration
    ser.open()
    maxAcceleration = ser.write((str(axis) + 'AU?').encode())  #value is 4
    ser.close()
    if acceleration <= maxAcceleration:
        writeCommand(ser, str(axis) + 'AC' + str(acceleration))
        writeCommand(ser, str(axis) + 'AG' + str(acceleration))
    else:
        print('Attempting to use an invalid accleration')
        quit()
    #Move home
    if moveHome==True:
        writeCommand(ser, str(axis) + 'OR0')  #OR0 is "find +0 position count"
    
def main():
    #configureAxis(ser,1,4,4)
    ser.open()
    ser.write('1PA1\r'.encode())
    ser.close()
    #writeCommand(ser, '1PA+10')
    #moveAbsolute(ser, 1, 10)

main()
'''
ser.open()
print(ser.write('1AU\r'.encode()))
ser.close()
print(writeCommand(ser,'1AU?'))
print(writeCommand(ser, str(1) + 'VU?'))
'''
