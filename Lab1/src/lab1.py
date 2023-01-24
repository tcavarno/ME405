import pyb

class MotorDriver:
    """! 
    This class implements a motor driver for an ME405 kit. 
    """

    def __init__ (self, en_pin, in1pin, in2pin, timer):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin (Set the enable pin for the motor)
        @param in1pin (Set the in1 pin for the motor)
        @param in2pin (Set the in2 pin for the motor)
        @param timer  ()
        """


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
        print ("Setting duty cycle to {level}")

class EncoderReader:
    """! 
    This class implements a EncoderReader for an ME405 kit. 
    """

    def __init__ (self):
        """! 
        Creates a EncoderReader by initializing GPIO
        pins and turning off the motor for safety. 
        @param 
        """
        print ("Creating a motor driver")

   
    def read():
       """!
       """
       pass
    
    def zero():
        """!
        """
        pass

def encoder_test():
    #init
    tim4 = pyb.Timer(4,period = 0xffff,prescaler = 0)
    tim4_ch1 = tim4.channel(1,mode = pyb.Timer.ENC_AB)
    #timer stuff


def main():
    encoder_test()

if __name__ == "__main__":
    main()