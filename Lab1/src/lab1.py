"""!
@file lab1.py
This file contains code which uses PWM output
with varying duty cycle to control a DC motor.
It also uses timer channels for encoder measurements.

TODO: Create a class called MotorDriver which allows a user
      to initialize enabable, in1, in2, and timer pins to control
      a motor with. As well as set the duty cycle of the initialized
      motor to controll speed. 
TODO: Create a class called EncoderReader which allows a user 
      to inialize board pins for use with a motor_encoder, as well 
      as read the encoder counter and handle underflow and overflow.
TODO: Create a function called motor_test which spins a motor in both
      directions and prints out the encoder count.
TODO: Create a function name main which calls the motor_test
      function.

@author Miloh Padgett, Tristan Cavarno, Jon Abraham
@date 12-Jan-2023 Original File
"""


import pyb #micropython board functions library

class MotorDriver:
    """! 
    This class implements a motor driver for an ME405 kit. 
    """

    def __init__ (self, en_pin: pyb.Pin, in1pin: pyb.Pin, in2pin: pyb.Pin, timer: pyb.Timer):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin (Set the enable pin for the motor)
        @param in1pin (Set the in1 pin for the motor)
        @param in2pin (Set the in2 pin for the motor)
        @param timer  (Sets the timer for the motor)
        """
        #Asign this drivers pins and timer
        self.en_pin = en_pin
        self.in1pin = in1pin
        self.in2pin = in2pin
        self.timer = timer

        #Disable the motor to begin
        self.en_pin.value(0)

        #Asign the timer channels
        self.in1ch = self.timer.channel(1,pyb.Timer.PWM,pin = self.in1pin)
        self.in2ch = self.timer.channel(2,pyb.Timer.PWM,pin = self.in2pin)
        

        print ("Creating a motor driver")

    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
        #Set motor output for valid positive 'level's
        if(level > 0 and level <=100):
            self.in1ch.pulse_width_percent(level)
            self.in2ch.pulse_width_percent(0)
            self.en_pin(1)
        #Set motor output for valid negative 'level's
        elif(level < 0 and level >= -100):
            self.in2ch.pulse_width_percent(abs(level))
            self.in1ch.pulse_width_percent(0)
            self.en_pin(1)
        #Disable the motor on all other values
        else:
            self.en_pin(0)

        print(f"Setting duty cycle to {level}")

class EncoderReader:
    """! 
    This class implements a EncoderReader for an ME405 kit. 
    """

    def __init__ (self,enc_A,enc_B,timer):
        """! 
        Creates a EncoderReader by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_A     Pin for encoder channel A
        @param en_A     Pin for encoder channel B
        @param timer    timer used for counting 
        """

        print ("Creating a EncoderReader")

        #Set interal pins and timer
        self.en_A = enc_A
        self.en_B = enc_B
        self.timer = timer

        #Setup channels.
        self.tim4_ch1 = timer.channel(1,mode = pyb.Timer.ENC_AB,pin = self.en_A)
        self.tim4_ch2 = timer.channel(2,mode = pyb.Timer.ENC_AB,pin = self.en_B)

        #Init other EncoderReader members
        self.prev=0
        self.cur=0
        self.ticks=0
        self.timer.counter(0)
   
    def read(self):
        """!
        Reads the counter and calculates the number of ticks.
        Also accounts for underflow and overflow
        """
        #get current encoder count
        self.cur = self.timer.counter()
        #calculate delta
        delta = self.cur-self.prev
        #calculate over/underflow limit
        max_change = (2**16 + 1) / 2
        print(f"Cur: {self.cur} Delta: {delta} Max: {max_change}")
        #Underflow case
        if(delta > max_change):
            delta -= (2**16 +1)
        #Overflow case
        elif(delta < -1*max_change):
            delta += (2**16 +1)

        #add delta to number of ticks
        self.ticks+=delta
        #store current in previous    
        self.prev = self.cur

    def zero(self):
        """!
        Set's ticks to zero
        """
        self.ticks=0


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