# -*- coding: utf-8 -*-
"""
Initial experimental development of the MotorControl class.

Created on 9/10/19

@author: Luke Kurlandski
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

def writeCommand(ser, command, closeAfter=False):
    '''
    Send any command to a serial port.
    (arg1) ser: serial port (port object) 
    (arg2) command: the command to send to the motor (string)
    (arg3) closeAfter: close port after command, if true (boolean)
    '''
    
    if command.find('\r') == -1:
        command = command + '\r'
    if ser.is_open == False:
        ser.open()
    ser.write(command.encode())
    if closeAfter == True:
        ser.close()
    
def moveAbsolute(ser, axis, goToPos):
    '''
    Move the stage to an absolute location. Wait until motion is complete.
    (arg1) ser: serial port (port object)
    (arg2) axis: axis of operation (int)
    (arg3) goToPos: position to navigate to (double)
    '''
    
    strAxis = str(axis)
    strGoToPos = str(goToPos)
    writeCommand(ser, strAxis + 'PA' + strGoToPos)
    waitMotionDone(ser, axis)
    
def configureAxis(ser, axis, velocity, acceleration, moveHome=True):
    '''
    Initial configuration of device.
    (arg1) ser: serial port (port object)
    (arg2) axis: axis of operation (int)
    (arg3) velocity: velocity to set device (double)
    (arg4) acceleration: acceleration/decceleration to set device (double)
    (arg5) moveHome: moves device to home position if true (boolean)
    '''
    
    #Turn axis on
    strAxis = str(axis)
    strVelocity = str(velocity)
    strAcceleration = str(acceleration)
    writeCommand(ser, strAxis + 'MO')
    
    #Compute velocity
    writeCommand(ser, strAxis + 'VU?')
    strMaxVelocity = ser.read(6).decode()  #5 sig figures
    maxVelocity = float(strMaxVelocity)
    if velocity <= maxVelocity:
        writeCommand(ser, strAxis + 'VA' + strVelocity)
    else:
        print('Attempting to use an invalid velocity.' +
              'Setting velocity to max: ' + strMaxVelocity)
        writeCommand(ser, strAxis + 'VA' + strMaxVelocity)
        
    #Compute acceleration/decceleration
    writeCommand(ser, strAxis + 'AU?')
    strMaxAcceleration = ser.read(10).decode()[3:9] #5 sig figures
    maxAcceleration = float(strMaxAcceleration)
    if acceleration <= maxAcceleration:
        writeCommand(ser, strAxis + 'AC' + strAcceleration)
        writeCommand(ser, strAxis + 'AG' + strAcceleration)
    else:
        print('Attempting to use an invalid accleration.' +
              'Setting acceleration to max: ' + strMaxAcceleration)
        writeCommand(ser, strAxis + 'AC' + strMaxAcceleration)
        writeCommand(ser, strAxis + 'AG' + strMaxAcceleration)
        
    #Move home
    if moveHome==True:
        writeCommand(ser, strAxis + 'OR0')  #OR0,OR1,OR2...?
        waitMotionDone(ser, axis)
        
def waitMotionDone(ser, axis):
    '''
    Delays until the device is finished moving plus .1 seconds. 
    (arg1) ser: serial port (port object)
    (arg2) axis: axis of operation (int)
    '''
    
    strAxis = str(axis)
    writeCommand(ser, strAxis + 'WS100') #wait an additional .1 seconds

def main():
    #configureAxis(ser,1,4,4)
    writeCommand(ser, '1OR0')
    ser.open()
    print(ser.write('1MD\r'.encode()))
    ser.close()
    #print(writeCommand(ser, '1MD'))
    ser.open()
    ser.write('1PA1\r'.encode())
    ser.close()
    #writeCommand(ser, '1PA+10')
    #moveAbsolute(ser, 1, 10)

def test1():
    ser.open()
    ser.write('1PA-5\r'.encode())
    ser.close()
    ser.open()
    ser.write('1MD0\r'.encode())
    print(ser.read(1))
    ser.close()
    #ser.write('1PA1\r'.encode())
    #ser.close()
    
def test2():
    writeCommand(ser, '1PA-1')
    waitMotionDone(ser, 1)
    writeCommand(ser, '1PA1')
    
def test3():
    writeCommand(ser, '1PA1')
    writeCommand(ser, '1MD0')
    ser.open()
    print(ser.read(1))
    ser.close()
    
def test4():
    ser.open()
    ser.write('1PA1\r'.encode())
    ser.close()
    ser.open()
    ser.write('1MD0\r'.encode())
    x = ser.read(1)
    print(x)
    print(x == b'1')
    ser.close()
    
def test5():
    configureAxis(ser,1,1,1)
    ser.close()

def test6():
    configureAxis(ser, 1, 2, 2)
    moveAbsolute(ser,1,-1)
    #moveAbsolute(ser,1,1)
    ser.close()
    
def test7():
    writeCommand(ser, '1PA4')
    while True:
        writeCommand(ser, '1MD0')
        byteX = ser.read(1)
        print(byteX)
        if(byteX == b'1'):
            break
        time.sleep(.25)
    ser.close()
    
def test8():
    configureAxis(ser,1,1,1,False)
    writeCommand(ser, '1PA1')
    writeCommand(ser, '1WS')
    writeCommand(ser, '1PA-1')
    writeCommand(ser, '1WS')
    writeCommand(ser, '1PA1')
    writeCommand(ser, '1WS')
    writeCommand(ser, '1PA-1')
    
    ser.close()
    
def test9():
    moveAbsolute(ser, 1, 1)
    
def test10():
    configureAxis(ser,1,1,1)
    moveAbsolute(ser,1,1)
    moveAbsolute(ser,1,-1)
    moveAbsolute(ser,1,1)
    ser.close()
    
test10()

'''
ser.open()
print(ser.write('1AU\r'.encode()))
ser.close()
print(writeCommand(ser,'1AU?'))
print(writeCommand(ser, str(1) + 'VU?'))
'''
