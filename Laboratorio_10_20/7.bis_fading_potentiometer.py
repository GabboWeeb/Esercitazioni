from machine import Pin, PWM, ADC
from time import sleep_ms

led = PWM(Pin(5), freq=5000)

vmaxi = 4095 
vmaxo = 1023 

sensor = ADC(Pin(35))

sensor.atten(ADC.ATTN_11DB)

while True:
    valore = sensor.read() 
    segnale = int (valore * vmaxo / vmaxi) 
    print(f"Lettura ADC: {valore}, PWM: {segnale}")  
    
    led.duty(segnale) 
    sleep_ms(50) 