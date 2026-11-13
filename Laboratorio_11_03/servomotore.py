from machine import Pin,PWM
import time




sg90 = PWM(Pin(23, mode=Pin.OUT))
sg90.freq(50) # Periodo di 20 ms (50 Hz)

ext_button = Pin(32, Pin.IN, Pin.PULL_UP)

stato=False #false=0°
duty=26 #base
#solution with debounce
# Memorizza il tempo dell'ultima attivazione del pulsante.
last_on = 0

#modifica il valore del blinking
def led_toggle(irq):
    print('a')
    global last_on
    global stato, duty
    
    # Debounce: misura il tempo dall'ultima attivazione.
    time_ms = time.ticks_ms() # Ottiene il tempo attuale in millisecondi.
    delay = time.ticks_diff(time_ms, last_on) # Calcola la differenza tra il tempo corrente e l'ultima attivazione.
    if (delay < 200): # Se la differenza è inferiore a 200ms (tempo di debounce), ignora l'input.
        return
    
    last_on = time_ms # Aggiorna `last_on` con il tempo corrente.
    
    stato=not stato
    if(stato==True):
        duty=128
    else:
        duty=26
        

    
ext_button.irq(trigger = Pin.IRQ_FALLING, handler = led_toggle)
ext_button.irq(trigger = Pin.IRQ_RISING, handler = led_toggle)


# calcoliamo il range su cui opera il servo motore 
# minima posizione (0 gradi) -> duty = durata impulso alto/periodo 0.5ms/20ms = 0.025 = 2.5% duty cycle
# massima posizione (180 gradi) -> duty = durata impulso alto/periodo 2.4ms/20ms = 0.12 = 12% duty cycle

# Risoluzione a 10 bit per duty cycle 0 e 2^10-1 (0-1023).
# 0.025*1023=25.575
# 0.12*1023=122.76

while True:
    sg90.duty(duty)#0° -0.5ms
    