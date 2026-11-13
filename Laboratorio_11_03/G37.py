

from machine import ADC, Pin,PWM
import time


class LDR:
    """This class read a value from a light dependent resistor (LDR)"""

    def __init__(self, pin, min_value=0, max_value=100):
        """
        Initializes a new instance.
        :parameter pin A pin that's connected to an LDR.
        :parameter min_value A min value that can be returned by value() method.
        :parameter max_value A max value that can be returned by value() method.
        """
        if min_value >= max_value:
            raise Exception('Min value is greater or equal to max value')

        # initialize ADC (analog to digital conversion)
        # create an object ADC
        self.adc = ADC(Pin(pin))
        self.min_value = min_value
        self.max_value = max_value

    def read(self):
        """
        Read a raw value from the LDR.
        :return a value from 0 to 4095.
        """
        return self.adc.read()

    def value(self):
        """
        Read a value from the LDR in the specified range.
        :return a value from the specified [min, max] range.
        """
        return (self.max_value - self.min_value) * self.read() / 4095


# initialize an LDR
ldr = LDR(34)
# === AGGIUNTA: Inizializzazione del buzzer sul Pin 22 ===
buzzer = PWM(Pin(22, Pin.OUT), freq=2000)


sg90 = PWM(Pin(23, mode=Pin.OUT))
sg90.freq(50) # Periodo di 20 ms (50 Hz)
led= Pin(25, Pin.OUT)

while True:
    # read a value from the LDR
    value1 = ldr.read()
    print('analog value= {}'.format(value1))
    value = ldr.value()
    print('value = {}'.format(value))
    if value < 20:
        led.value(1)
        buzzer.duty(512)     
        sg90.duty(26)
    elif value<50:
        buzzer.duty(0)     
        sg90.duty(76)
        led.value(0)
    else:
        buzzer.duty(0)    
        sg90.duty(100)
        led.value(0)


    # a little delay
    time.sleep(1)

