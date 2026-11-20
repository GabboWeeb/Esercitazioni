#blinking del led con due pulsanti

from machine import Pin
from time import sleep

led= Pin(23, Pin.OUT)
btnON =  Pin(14, Pin.IN, Pin.PULL_DOWN) 
btnOFF = Pin(27, Pin.IN, Pin.PULL_UP) 
led.off()
blinking= False #non lampeggia
def switchON(bt1):
    global blinking
    blinking=True
def switchOFF(bt2):
    global blinking
    blinking=False
    led.off()
    
btnON.irq(trigger=Pin.IRQ_RISING, handler=switchON)
btnOFF.irq(trigger=Pin.IRQ_FALLING, handler=switchOFF)
while True:
    if blinking:
        led.value(not led.value())
        sleep(1)
