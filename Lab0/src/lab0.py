"""!
@file lab0.py
This file contains code which uses PWM output
with varying duty cycle to change the brightness of 
an LED. The LED slowly reaches its max brightness 
over a 5 second time period and then resets and
continues this cycle indefinitely.

TODO: Create a function name led_setup which initializes
      the proper timer and channel and pin to generate a PWM.
TODO: Create a function name led_brightness which is passed a 
      brightness percent and sets that brightness
TODO: Create a function name main which calls the led_brightness
      function with the proper brightness

@author Miloh Padgett, Tristan Cavarno, Jon Abraham
@date 12-Jan-2023 Original File
"""

import pyb #micropython board functions library

def led_setup():
    """!
    Setup channel for PWM output
    This function initializes the pine PA0
    with its correspoding channel and timer
    for PWM output. 
    @param None
    @returns The channel initalized for PWM
    """
    #Set pin PA0 as an output pin
    pinA0 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    #set timer2
    tim2 = pyb.Timer (2, freq=20000)
    #set channel 1 with timer 2 as PWM on pin PA0
    ch1 = tim2.channel (1, pyb.Timer.PWM_INVERTED, pin=pinA0)
    return ch1
    
def led_brightness(brightness, ch1):
    """!
    Set the brightness of the LED
    This function sets the pulse width percent
    of the given channel to a given percent which
    is the desired brightness of the LED
    @param brightness, the desired brightness percent of the LED
    @param ch1, the initiazled channel for PWM output
    @returns None
    """
    ch1.pulse_width_percent (brightness)
    
def main():
    """!
    Call set up channel and then set LED brightness
    This function first initializes the board by calling
    the led_setup function, then it iterares from 0 to 100
    in an indefinite loop setting the LED brightness percent
    to the iterated value. It delays by 50ms between setting 
    values so that the LED brightness reaches its max over
    a 5 second time period. It resets the LED value after
    reaching the max and then repeats.
    @param None
    @returns None
    """
    #set up board for PWM output to LED
    ch1 = led_setup()
    #indefinite loop
    while(1):
        #iterate from 0 to 100
        for i in range(100):
            #call led_brightness with percent i,
            # and the initialized channel
            led_brightness(i, ch1)
            #delay for 50ms 
            pyb.delay(50)
        #reset brightness to 0
        led_brightness(0, ch1)   

# The following code only runs if this file is run as the main script;
# it does not run if this file is imported as a module
if __name__ == "__main__":

    #Call the main function
    main()