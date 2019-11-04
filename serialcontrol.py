# -*- coding: utf-8 -*-
"""
Control devices that use a serial port connection.

Created on 10/21/19
Modified on 11/1/19

@author: Luke Kurlandski

These classes are designed to allow simple control of serial devices.
"""

import serial
import time

class Control:
    """
    Generic class to allow easy use of machinery that uses serial ports
    """
    
    def __init__(self, port, baudrate, timeout, stopbits, bytesize):
        """
        Construct a serial object and configure the serial port.
        """
        
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = timeout
        self.ser.stopbits = stopbits
        self.ser.bytesize = bytesize
        
    @classmethod
    def from_arguments(cls, args):
        """
        Construct serial objects from different data types (constructor overload). 
        
            Arguments:
                (arg1) args (tuple or list) : arguments to handle
                
            Returns:
                (ret1) : class object
        """
        
        if isinstance(args, tuple) or isinstance(args, list):
            return cls(args[0], args[1], args[2], args[3], args[4])
            
        
    def writeCommand(self, command, closeAfter=False):
        """
        Send any command to a serial port with/without carriage return.
        
        Arguments:
            (arg1) command (string) : the command to send to the motor
            (arg2) closeAfter (boolean) : if true, close port after command
        """
        
        cmd = command
        if cmd.find('\r') == -1:
            cmd = cmd + '\r'
        if self.ser.is_open == False:
            self.ser.open()
        self.ser.write(cmd.encode())
        if closeAfter == True:
            self.ser.close()   
            
    def __del__(self): 
        """
        Destructor to ensure the serial port is closed.
        """
        
        self.ser.close()
        print("Serial Port Closed:", self.ser.port)
        
class Shutter(Control):
    """
    Class to control shutter. Derives from Control class.
    """
            
    def toggle_shutter(self, pause):
        """
        Opens the shutter. Pauses for a certain amount of time. Closes the shutter.
        
        Arguments:
            (arg1) pause : number of seconds to open for (float)
        """
        
        self.writeCommand('ens')
        time.sleep(pause)
        self.writeCommand('ens')
        time.sleep(.05) #prevents the shutter from being overloaded by signals

class Motor(Control):
    """
    Class to control the motor. Derives from Control class.
    """
        
    def moveAbsolute(self, axis, goToPos, delay=0):
        """
        Move the stage to an absolute location. Wait until motion is complete.
        Arguments:
            (arg2) axis (int) : axis of operation 
            (arg3) goToPos (double) : position to navigate to 
            (arg4) delay (int) : additional time to wait in milliseconds 
        """
        
        strAxis = str(axis)
        strGoToPos = str(goToPos)
        self.writeCommand(strAxis + 'PA' + strGoToPos)
        self.waitMotionDone(axis, delay)
    
    def waitMotionDone(self, axis, milliseconds=0):
        """
        Delays until the device is finished moving plus .1 seconds. 
        
        Arguments: 
            (arg1) axis (int) : axis of operation
        """
        
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
        """
        Initial configuration of motor device.
        
        Arguments:
            (arg1) axis (int) : axis of operation
            (arg2) velocity (double) : velocity to set device
            (arg3) acceleration (double) : acceleration/decceleration to set device
            (arg4) moveHome (boolean) : moves device to home position if true
        """
        
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

class Laser(Control):
    """
    Class to control the laser, derived from Control class.
    """
    
    def __init__(self, port, baudrate, timeout, stopbits, bytesize):
        """
        Construct a laser object.
        """
        
        super().__init__(port, baudrate, timeout, stopbits, bytesize)
        self.set_max_power()
    
    def set_max_power(self, new_max=-1):
        """
        Modify the maximum power of the laser.
        
        Arguments:
            (arg1) new_max (float) : the maximum power this laser is allowed to reach
        """
        
        self.max_power = new_max
        print('WARNING: \n\tYou have set the maximum power to ' + str(new_max) + ' miliwatts.')
    
    def get_head_ID(self):
        """
        Get the head ID from connected laser.
        """
        
        self.writeCommand('?HID')
        head_ID = self.ser.read(30)
        byte_head_ID = head_ID[6:15]
        if float(byte_head_ID) != 42185.000: #HID number
            raise Exception('WARNING: \n\tAttempting to use laser configurations that ' +
                'does not have a compatable Head ID!\n\tStop immidiately or you will destroy the laser')
            
    def read_power(self):
        """
        Start up the laser by monitoring its power level.
        """
        
        self.ser.write('?P\r'.encode())
        str_power = str(self.ser.read(30))
        float_power = float(str_power[8:12])
        #If the laser is on, make inactive
        if float_power >= 0.4:
            self.writeCommand('L=0')
        #If the laser is not on (or booting up), ensure it is inactive
        else:
            for i in range(0, 450):
                self.writeCommand('L=0')
                time.sleep(.1)
                
    def turn_on_off(self, on_off):
        """
        Turn the laser on or off.
        
        Arguments:
            (arg1) on_off (boolean) : True indicates turn on; False indicates turn off
        """
        
        if on_off:
            self.writeCommand('L=1')
        if not on_off:
            self.writeCommand('L=0')
            
    def change_power(self, new_power):
        """
        Change the power output of the laser, not exceeding max power.
        
        Arguments:
            (arg1) new_power (float) : new power level of the laser in milliwatts
        """
        
        if new_power < self.max_power:
            self.writeCommand('P='+str(new_power))
        else:
            self.writeCommand('P='+str(self.max_power))
            print('WARNING:')
            print('\tInstruction: \'Set max power to ' + str(new_power) + '\'')
            print('\tMax Power: ' + str(self.max_power))
            print('\tOutcome: power set to max power')
            
    def configure_settings(self, settings):
        """
        Configure all settings on the laser.
        
        Arguments:
            (arg1) settings (list) : various settings to confiure the laser to
        """
        
        self.set_max_power(settings[0])
        
def test():
    """
    Method for internal testing
    """
    
    print('Test')