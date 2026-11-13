from machine import Pin
from time import sleep,ticks_ms

ledblue= Pin(2, Pin.OUT)
ledgreen= Pin (16, Pin.OUT )
ledred= Pin (15 , Pin.OUT )

btn = Pin(27, Pin.IN, Pin.PULL_UP) 

ledred.off()
ledblue.off()
ledgreen.off()

blinking= True
ultimo_tempo=0

def switc(btn):
    global blinking, ultimo_tempo
    tempo_corrente = ticks_ms()
    
    if tempo_corrente - ultimo_tempo > 200:
        ultimo_tempo = tempo_corrente
        blinking = not blinking  
        
        if not blinking:
            ledblue.off()
            ledgreen.off()
            ledred.off()
    
    
btn.irq(trigger=Pin.IRQ_FALLING, handler=switc)

while True:
    if blinking:           
        ledblue.value(1)
        sleep(1)
        ledblue.value(0)
        if blinking:           
            ledgreen.value (1)
            sleep(1)
            ledgreen.value (0)
            if blinking:   
                ledred.value(1)
                sleep(1)
                ledred.value (0)