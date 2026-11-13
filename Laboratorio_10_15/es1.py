

from machine import Pin
from time import sleep,ticks_ms

ledblue= Pin(2, Pin.OUT)
ledgreen= Pin (16, Pin.OUT )
ledred= Pin (15 , Pin.OUT )

btn = Pin(27, Pin.IN, Pin.PULL_UP) 

ledred.off()
ledblue.off()
ledgreen.off()

blinking= False
ultimo_tempo=0
temp=2.0

def switc(btn):
    global blinking, ultimo_tempo
    tempo_corrente = ticks_ms()
    global temp
    
    place=tempo_corrente- ultimo_tempo
    
    if place > 200:
        if place > 500:
            temp=2.0
            ultimo_tempo = tempo_corrente
            blinking = not blinking
        else:
            temp=0.5
            ultimo_tempo = tempo_corrente
        
    
        
        if not blinking:
            ledblue.off()
            ledgreen.off()
            ledred.off()
    
    
btn.irq(trigger=Pin.IRQ_FALLING, handler=switc)

while True:
    if blinking:           
        ledblue.value(1)
        sleep(temp)
        ledblue.value(0)
        if blinking:           
            ledgreen.value (1)
            sleep(temp)
            ledgreen.value (0)
            if blinking:   
                ledred.value(1)
                sleep(temp)
                ledred.value (0)
    



