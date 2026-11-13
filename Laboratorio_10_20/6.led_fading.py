
from machine import Pin, PWM
import time

pwm_led = PWM(Pin(5, mode=Pin.OUT)) # Attach PWM object on the LED pin

#Da 1 kHz a 5 kHz → Ottimo per un controllo stabile della luminosità senza sfarfallio.
#In Python, puoi inserire i trattini bassi _ per rendere i numeri più facili da leggere.
#Ad esempio, per scrivere 1 MHz invece di 1000000, possiamo scrivere 1_000_000.
pwm_led.freq(5_000)


#We use the function .duty_()
#to select the duty cycle with a value between 0 and 1023 (resolution is 10 bit). 
#The voltage is set directly on the output of the previously selected pin.

while True:
    #To vary the voltage faster, we change the duty from 5 to 5 with range(0, 1023, 5)
    for duty in range(0,1024, 5): 
        pwm_led.duty(duty)
        time.sleep_ms(5)
    #To decrement a value, we put a step of -5 range(1023, -1, -5) 
    for duty in range(1023,-1, -5):
        pwm_led.duty(duty)
        time.sleep_ms(5)