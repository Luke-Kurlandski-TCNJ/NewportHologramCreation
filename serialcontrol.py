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
            
        
    def write_command(self, command, closeAfter=False):
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
        
        self.write_command('ens')
        time.sleep(pause)
        self.write_command('ens')
        time.sleep(.05) #prevents the shutter from being overloaded by signals
    
    def set_operating_mode(self, mode = 'single'):
        """
        Alter the operating mode of the shutter.
        
        Arguments:
            (arg1) mode (string) : one of several allowed operating modes of the shutter
        """
        
        m = mode.lowercase()
        if m == 'manual':
            n='1'
        elif m == 'auto':
            n='2'
        elif m == 'single':
            n='3'
        elif m == 'repeat':
            n='4'
        elif m == 'external gate':
            n='5'
        else:
            raise Exception('Setting shutter to an invalid mode: ' + str(mode))
        self.write_command('mode='+n)

class Motor(Control):
    """
    Class to control the motor. Derives from Control class.
    """
        
    def move_absolute(self, axis, goToPos, delay=0):
        """
        Move the stage to an absolute location. Wait until motion is complete.
        Arguments:
            (arg2) axis (int) : axis of operation 
            (arg3) goToPos (double) : position to navigate to 
            (arg4) delay (int) : additional time to wait in milliseconds 
        """
        
        strAxis = str(axis)
        strGoToPos = str(goToPos)
        self.write_command(strAxis + 'PA' + strGoToPos)
        self.wait_motion_done(axis, delay)
    
    def wait_motion_done(self, axis, milliseconds=0):
        """
        Delays until the device is finished moving plus .1 seconds. 
        
        Arguments: 
            (arg1) axis (int) : axis of operation
        """
        
        strAxis = str(axis)
        while True:
            self.write_command(strAxis + 'MD?')
            try:
                byte = self.ser.read(4)
                bit = str(byte.decode())
            except:
                print('Cannot convert the motor\'s output: ', byte)
            if bit.find('1') != -1:
                return
            else:
                time.sleep(.5)
                
    def configure_axis(self, axis, velocity=1, acceleration=4, moveHome=True):
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
        self.write_command(strAxis + 'MO')
        #Set velocity
        try:
            self.write_command(strAxis + 'VA' + strVelocity)
        except:
            print('Attempting to use an invalid velocity.')
        #Set acceleration/decceleration
        try:
            self.write_command(strAxis + 'AC' + strAcceleration)
            self.write_command(strAxis + 'AG' + strAcceleration)
        except:
            print('Attempting to use an invalid accleration.')
        #Move home
        if moveHome==True:
            self.write_command(strAxis + 'OR0')  #OR0,OR1,OR2...?
            self.wait_motion_done(axis)

class Laser(Control):
    """
    Class to control the laser, derived from Control class.
    """
    
    def __init__(self, port, baudrate, timeout, stopbits, bytesize):
        """
        Construct a laser object.
        """
        
        super().__init__(port, baudrate, timeout, stopbits, bytesize)
        self.max_power = -1
        self.power_pause = 0
    
    def get_head_ID(self):
        """
        Get the head ID from connected laser.
        """
        
        self.write_command('?HID')
        head_ID = self.ser.read(30)
        byte_head_ID = head_ID[6:15]
        if float(byte_head_ID) != 42185.000: #HID number
            raise Exception('WARNING: \n\tAttempting to use laser configurations that ' +
                'does not have a compatable Head ID!\n\tStop immidiately or you will destroy the laser')
        
    def turn_on_off(self, on_off):
        """
        Turn the laser on or off.
        
        Arguments:
            (arg1) on_off (boolean) : True indicates turn on; False indicates turn off
        """
        
        if on_off:
            self.write_command('L=1')
        if not on_off:
            self.write_command('L=0')
            
    def change_power(self, new_power):
        """
        Change the power output of the laser, not exceeding max power.
        
        Arguments:
            (arg1) new_power (float) : new power level of the laser in milliwatts
        """
        
        if new_power == 0:
            #Turn the laser off if nessecary
            self.write_command('L=0')        
        elif new_power > self.max_power:
            #Set power to max power if new power is too large
            self.write_command('P='+str(self.max_power))
        else:
            #Otherwise set to new power
            self.write_command('P='+str(new_power))
        time.sleep(self.power_pause)

    def configure_settings(self, settings):
        """
        Configure all settings on the laser.
        
        Arguments:
            (arg1) settings (list) : various settings to confiure the laser to
        """
        
        self.max_power = settings[0]
        self.power_pause = settings[1]
        
def test1():
    """
    Method for internal testing
    """
    
    try:
        print('Test')
        laser = Laser('COM3', 19200, .1, 1, 8)
        print('Setting max power')
        laser.set_max_power(new_max=10)
        print('Waiting for boot up')
        laser.boot_up()
        print('Turning laser on')
        laser.turn_on_off(True)
        time.sleep(5)
        print('Changing laser power')
        laser.change_power(9)
        time.sleep(5)
        print('Turning laser off')
        laser.turn_on_off(False)
        
    except Exception as e:
        print(e)
        laser.ser.close() 
        
def test2():
    try:
        shutter = Shutter.from_arguments(('COM6', 9600, .1, 1, 8))
        shutter.write_command('?mode')
        print(shutter.ser.read(10))
        print('Toggling the shutter')
        shutter.toggle_shutter(5.0)
        shutter.toggle_shutter(1.0)
        shutter.toggle_shutter(1.0)
        shutter.toggle_shutter(1.0)
        shutter.ser.close()
    except Exception as e:
        shutter.ser.close()
        print(e)
    
def test3():
    try:
        laser = Laser('COM3', 19200, .1, 1, 8)
        laser.set_max_power(20)
        print('Booting up')
        laser.boot_up()
        print('Turn on')
        laser.turn_on_off(True)
        laser.change_power(10)
        print('Run until keyboard interrupt')
        while True:
            laser.find_faults()
            time.sleep(1)
    except Exception or KeyboardInterrupt as e:
        print(e)
        laser.ser.close()

def test4():
        try:
            laser = Laser('COM3', 19200, .1, 1, 8)
            laser.set_max_power(40)
            #laser.turn_on_off(True)
            #laser.write_command('P=20')
            laser.change_power(20)
            '''
            laser.ser.open()
            laser.ser.write('P=15\r'.encode())
            laser.ser.close()
            '''
            time.sleep(5)
        except Exception or KeyboardInterrupt as e:
            print(e)
            laser.ser.close()
        laser.ser.close()


    


