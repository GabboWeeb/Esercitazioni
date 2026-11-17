from LDR import LDR
from Servomotor import Servomotor
from Led import Led
from machine import Pin, I2C
from Cronometro import Cronometro
import ssd1306
import framebuf
import time
import math




#inizializza cronometro LDR
cronometro_LDR = Cronometro()
cronometro_LDR.start()
#inizializza ldr
ldr=LDR(14,0,180)
ldr_lum=ldr.value()
#inizializza schermo
WIDTH = 128
HEIGHT = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
#inizializza led
led=Led(25)
#inizializza servo
servo=Servomotor(23)


def rilevazione_ldr(ldr):
    global ldr_lum
    ldr_lum=ldr.value()
    print("La luminosità rilevata è ",ldr_lum,'\n')

lum_registrata=0
def aggiornamento_schermo(display):
    global lum_registrata, ldr_lum
    if round(ldr_lum)!=lum_registrata:
        lum_registrata= round(ldr_lum)
        display.fill_rect(0,0,128,64,0)
        display.text("{:2.2f}".format(ldr_lum), 40, 20,1)
        display.show()
    
    
def aggiorna_led(led):
    global ldr_lum
    if ldr_lum>60:
        led.on()
    else:
        led.off()
    
def aggiorna_servo(servo):
    global ldr_lum
    if ldr_lum>60:
        servo.set_angle(180)
    else:
        servo.set_angle(0)

while True:
    #gestione rilevazione dell'LDR
    if cronometro_LDR.scaduto(500):
        cronometro_LDR.avanza(500)
        rilevazione_ldr(ldr)
        aggiornamento_schermo(display)
        aggiorna_led(led)
        aggiorna_servo(servo)
    
    
    time.sleep_ms(10)


