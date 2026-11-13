from machine import Pin
import time


led = Pin(4, Pin.OUT)

ext_button = Pin(17, Pin.IN, Pin.PULL_UP)

led.off()
blinking = False

#solution with debounce
# Memorizza il tempo dell'ultima attivazione del pulsante.
last_on = 0

#modifica il valore del blinking
def led_toggle(irq):
    global blinking
    global last_on
    
    # Debounce: misura il tempo dall'ultima attivazione.
    time_ms = time.ticks_ms() # Ottiene il tempo attuale in millisecondi.
    delay = time.ticks_diff(time_ms, last_on) # Calcola la differenza tra il tempo corrente e l'ultima attivazione.
    if (delay < 200): # Se la differenza è inferiore a 200ms (tempo di debounce), ignora l'input.
        return
    
    last_on = time_ms # Aggiorna `last_on` con il tempo corrente.
    blinking = not blinking # Inverte lo stato del lampeggio (accende/spegne).
    
ext_button.irq(trigger = Pin.IRQ_FALLING, handler = led_toggle)

while True:
    while blinking:
        led.on()
        time.sleep_ms(500)  # LED acceso per 500ms.
        led.off()
        time.sleep_ms(500)  # LED spento per 500ms.
    
