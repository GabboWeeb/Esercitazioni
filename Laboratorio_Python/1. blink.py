#blinking di un led

from machine import Pin
# machine.Pin: Modulo specifico per controllare i GPIO di microcontrollori come ESP32
from time import sleep
#time.sleep(): Usato per le pause nel codice (in secondi)

led= Pin(23, Pin.OUT)
#Imposta il pin GPIO23 come uscita digitale.

while True:
    led.value(not led.value())
    #led.value() restituisce 1 (HIGH) se il LED è acceso, 0 (LOW) se è spento.
    #not led.value() inverte lo stato:
    #Se il LED è acceso (1), lo spegne (0).
    #Se il LED è spento (0), lo accende (1).
    sleep(3)
    #Aspetta 3 secondi prima di cambiare di nuovo lo stato.