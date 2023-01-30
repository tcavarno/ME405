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
        self.en_pin = en_pin
        self.in1pin = in1pin
        self.in2pin = in2pin
        self.timer = timer

        self.en_pin.value(0)

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
        if(level > 0 and level <=100):
            self.in1ch.pulse_width_percent(level)
            self.in2ch.pulse_width_percent(0)
            self.en_pin(1)

        elif(level < 0 and level >= -100):
            self.in2ch.pulse_width_percent(abs(level))
            self.in1ch.pulse_width_percent(0)
            self.en_pin(1)
        else:
            self.en_pin(0)
        print (f"Setting duty cycle to {level}")

class EncoderReader:
    """! 
    This class implements a EncoderReader for an ME405 kit. 
    """

    def __init__ (self,en_A,en_B,timer):
        """! 
        Creates a EncoderReader by initializing GPIO
        pins and turning off the motor for safety. 
        @param 
        """
        print ("Creating a EncoderReader")
        self.en_A = en_A
        self.en_B = en_B
        self.timer = timer
        self.tim4_ch1 = timer.channel(1,mode = pyb.Timer.ENC_AB,pin = self.en_A)
        self.tim4_ch2 = timer.channel(2,mode = pyb.Timer.ENC_AB,pin = self.en_B)

        self.prev=0
        self.cur=0

        self.ticks=0
   
    def read(self):
        """!
        """
        self.cur = self.timer.counter()
        self.ticks += self.cur-self.prev if self.prev < self.cur else (2**16)- 1 - (self.prev - self.cur) 
        self.prev = self.cur

    def zero(self):
        """!
        """
        self.ticks=0


def motor_test():
    in1 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    en = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    timer = pyb.Timer(3,freq=20000)
    motorA = MotorDriver(en,in1,in2,timer)

    ch1 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
    ch2 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
    tim8 = pyb.Timer(8,period=0xffff,prescaler = 0)
    encoder = EncoderReader(ch1,ch2,tim8)
    

    try:
        while(1):
            for i in range(-100,110,10):
                motorA.set_duty_cycle(i)
                encoder.read()
                print (f"Ticks: {encoder.ticks}")
                pyb.delay(500)
            for i in range(100,-110,-10):
                motorA.set_duty_cycle(i)
                encoder.read()
                print (f"Ticks: {encoder.ticks}")
                pyb.delay(500)
    except KeyboardInterrupt:
        motorA.set_duty_cycle(0)
        return


def main():
    motor_test()



if __name__ == "__main__":
    main()