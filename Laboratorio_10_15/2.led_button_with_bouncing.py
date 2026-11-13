from machine import Pin

led = Pin(4, Pin.OUT)


ext_button = Pin(17, Pin.IN, Pin.PULL_UP)


led_state = False

#WARNING!!! Bouncing button!!!
#causa potenzialmente più attivazioni non volute del LED

#La funzione led_toggle() è chiamata ogni volta
#che il pulsante viene premuto (causando un interrupt). 
def led_toggle(irq):
    global led_state
    led_state = not led_state # Inverte lo stato del LED
    led.value(led_state) # Imposta il LED in base al nuovo stato
    

ext_button.irq(trigger = Pin.IRQ_FALLING, handler = led_toggle)

