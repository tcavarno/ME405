import pyb

def led_setup():
    pinA0 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    tim2 = pyb.Timer (2, freq=20000)
    ch1 = tim2.channel (1, pyb.Timer.PWM_INVERTED, pin=pinA0)
    return ch1
    
def led_brightness(brightness, ch1):
    ch1.pulse_width_percent (brightness)
    
def main():
    ch1 = led_setup()
    while(1):
        for i in range(100):
            led_brightness(i, ch1)
            pyb.delay(50)
        led_brightness(0, ch1)   

    
if __name__ == "__main__":
    main()