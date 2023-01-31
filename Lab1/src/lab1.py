"""!
@file lab1.py
This file contains code which uses PWM output
with varying duty cycle to control a DC motor.
It also uses timer channels for encoder measurements.

TODO: Create a function called motor_test which spins a motor in both
      directions and prints out the encoder count.
TODO: Create a function name main which calls the motor_test
      function.

@author Miloh Padgett, Tristan Cavarno, Jon Abraham
@date 30-Jan-2023 Original File
"""

import pyb #micropython board functions library
from EncoderReader import *
from MotorDriver import *

def motor_test():
    """! 
    Tests the motor driver class by setting an oscillating range of duty cycles.
    The range includes running the motor at the maximum values (+/- 100%) and minimum
    value (0%). The encoder count is read each step and its value is printed.
    """
    
    #Set the GPIO pins and timer channel for the motor to pass into the motor class
    in1 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    en = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    timer = pyb.Timer(3,freq=20000)
    
    #Create motor driver object
    motorA = MotorDriver(en,in1,in2,timer)

    #Set the GPIO pins and timer channel to pass into the encoder class
    ch1 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
    ch2 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
    tim8 = pyb.Timer(8,period=0xffff,prescaler = 0)
    
    #Create encoder driver object
    encoder = EncoderReader(ch1,ch2,tim8)
    
    #Set oscillating range of duty cycles and print encoder count
    try:
        while(1):    
            for i in range(0,105,5):
                motorA.set_duty_cycle(i)
                encoder.read()
                print(f"Ticks: {encoder.ticks}")
                pyb.delay(100)
            for i in range(100,-105,-5):
                motorA.set_duty_cycle(i)
                encoder.read()
                print (f"Ticks: {encoder.ticks}")
                pyb.delay(100)
            for i in range(-100,5,5):
                motorA.set_duty_cycle(i)
                encoder.read()
                print (f"Ticks: {encoder.ticks}")
                pyb.delay(100)
    
    #Halt motor when user inputs keyboard interrupt
    except KeyboardInterrupt:
        motorA.set_duty_cycle(0)
        return


def main():
    """!
    calls the motor_test function.
    """
    motor_test()


# The following code only runs if this file is run as the main script;
# it does not run if this file is imported as a module
if __name__ == "__main__":
    #Call the main function
    main()