from machine import Pin, PWM,ADC
import math
import time
from time import sleep_ms

# Uso della costante matematica pi greco
PI = math.pi
#led
ledblue= Pin(2, Pin.OUT)
ledgreen= Pin (16, Pin.OUT )
ledred= Pin (15 , Pin.OUT )

ledred.off()
ledblue.off()
ledgreen.off()


# Configurazione del pin del buzzer
pinB = Pin(23, Pin.OUT)
passiveBuzzer = PWM(pinB, freq=2000) #suono molto acuto
passiveBuzzer.duty(512)  # Inizialmente il buzzer è spento

sensor = ADC(Pin(35))
vmaxi = 4095 
vmaxo = 2000 


while True:
    valore = sensor.read() 
    segnale = int (valore * vmaxo / vmaxi) 
    print(f"Lettura ADC: {valore}, PWM: {segnale}")  
    
    if(segnale!=0):
        passiveBuzzer.duty(512)
        passiveBuzzer.freq(segnale)
    else:
        passiveBuzzer.duty(0)
    
    if(segnale>0):
        ledgreen.value(1)
    else:
        ledgreen.value(0)

    if(segnale>666):
        ledred.value(1)
    else:
        ledred.value(0)
    
    if(segnale>1500):
        ledblue.value(1)
    else:
        ledblue.value(0)
    
    
    sleep_ms(10)


    
