from machine import Pin
import dht
import time
from LDR import LDR
from DimmableLed import DimmableLed
from Potentiometer import Potentiometer
from Servomotor import Servomotor
from StepMotor import StepMotor
from Button import Button
from Buzzer import Buzzer
from Led import Led
import math
from machine import Pin, I2C
from Cronometro import Cronometro
import ssd1306
import framebuf

#inizializza potenziometro
potenziometro=Potentiometer(35,22,32)

#inizializza servo
servo=Servomotor(18)
servo.set_angle(0)
#inizializza step
step=StepMotor(16,17,19,23)

#inizializza led verde e rosso
verde=Led(25)
rosso=Led(26)

#inizializza buzzer
buzzer=Buzzer(27)

#inizializza pulsanti
butt1=Button(32,1,250)
butt2=Button(33,1,250)

auto1=True
def func1(irq):
    global butt1,auto1
    if butt1.true_press():
        auto1= not auto1 
        
    

def func2(irq):
    global butt2,auto1,target_step
    if butt2.true_press():
        if auto1:
            buzzer.set_duty(0)
        else:
            if target_step==0:
                target_step=120
            elif target_step==120:
                target_step=240
            elif target_step==240:
                target_step=0

butt1.set_handler( func1, 10)
butt2.set_handler( func2, 10)
#inizializza schermo
WIDTH = 128
HEIGHT = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
display.text("Smarterra", 0, 0,1)
display.rect(0, 10, 128, 1, 1)
#inizializza cronometro per le misurazioni
cronometro_misure = Cronometro()
cronometro_misure.start()
# Inizializzazione del sensore DHT22
sensor = dht.DHT22(Pin(4))
# Richiede una nuova misurazione
sensor.measure()
# Legge la temperatura in gradi Celsius
temperatura = sensor.temperature()
# Legge l'umidità relativa in percentuale
umidita = sensor.humidity()
    
    
#inizializza ldr
ldr=LDR(14,0,100)
ldr_lum=ldr.value()

def effettua_misurazioni(sensor,ldr):
    global ldr_lum,temperatura,umidita
    ldr_lum=ldr.value()
    sensor.measure()
    temperatura = sensor.temperature()
    umidita = sensor.humidity()
    #print("La luminosità rilevata è ",ldr_lum,'\n')
    #print("La temperatura rilevata è ",temperatura,'\n')
    #print("La umidita rilevata è ",umidita,'\n')

def aggiorna_schermo(display):
    global ldr_lum,temperatura,umidita,causa, angolo_ventilazione, target_step
    global auto1
    lum_registrata= round(ldr_lum)
    display.fill_rect(0,12,128,64,0)
    display.text("TEMP:{:2.2f}C".format(temperatura), 0, 12,1)
    display.text("UMID:{:2.0f}%".format(umidita), 0, 20,1)
    display.text("LUCE:{:2.0f}%".format(ldr_lum), 0, 28,1)
    if angolo_ventilazione==0:
        vent="APERTA"
    else:
        vent="CHIUSA"
    display.text(f"VENT:{vent}", 0, 36,1)
    if target_step==0:
        tent="APERTA"
    else:
        tent="CHIUSA"
    display.text(f"TENDA:{tent}", 0, 44,1)


    #display.fill_rect(70,0,50,9,0)
    if causa==0:
        c="SISTEMA OK"
    elif causa==1:
        c="ALLARME UMID"
    elif causa==2:
        c="ALLARME TEMP"
    elif causa==3:
        c="ALLARME TEMP + UMID"
    display.text(f"{c}", 0, 52,1)
    
    if auto1:
        mode="AUTO"
    else:
        mode="MANUAL"
    if causa!=0:
        mode="ALARM"
    display.fill_rect(0,80,60,8,0)
    display.text(f"{mode}", 80, 0,1)
    display.show()
    
    
angolo_ventilazione=0 #false==sotto la soglia,true=sopra la soglia
def ventilazione_automatica(potenziometro,servo):
    global temperatura,angolo_ventilazione
    soglia=potenziometro.value()
    #print("Il potenziometro legge: ",soglia,"C°")
    if temperatura>soglia:
        servo.set_angle(90)
        angolo_ventilazione=90
    elif temperatura<soglia-2:
        servo.set_angle(0)
        angolo_ventilazione=0
        
def ventilazione_manuale(potenziometro,servo):
    global angolo_ventilazione
    angolo_ventilazione=potenziometro.value_between(0,90)
    servo.set_angle(angolo_ventilazione)
        
target_step=0
angolo_step=0
def schermatura_intelligente(step):
    global ldr_lum,target_step,angolo_step
    if ldr_lum<=30:
        target_step=0
        if angolo_step==0:
            pass
        else:
            step.step(1, 10, 10, "HALF")
            angolo_step-=1
    elif 31<=ldr_lum<=70:
        target_step=120
        if angolo_step==120:
            pass
        elif angolo_step>120:
            step.step(1, 10, 10, "HALF")
            angolo_step-=1
        elif angolo_step<120:
            step.step(-1, 10, 10, "HALF")
            angolo_step+=1
    elif ldr_lum>70:
        target_step=240
        if angolo_step==240:
            pass
        else:
            step.step(-1, 10, 10, "HALF")
            angolo_step+=1

def schermatura_manuale(step):
    global ldr_lum,target_step,angolo_step
    if target_step==0:
        if angolo_step==0:
            pass
        else:
            step.step(1, 10, 10, "HALF")
            angolo_step-=1
    elif target_step==120:
        if angolo_step==120:
            pass
        elif angolo_step>120:
            step.step(1, 10, 10, "HALF")
            angolo_step-=1
        elif angolo_step<120:
            step.step(-1, 10, 10, "HALF")
            angolo_step+=1
    elif target_step==240:
        if angolo_step==240:
            pass
        else:
            step.step(-1, 10, 10, "HALF")
            angolo_step+=1
    

causa=0 #0 nulla, 1 umidità, 2 temp, 3 entrambe
def sistema_allarme(rosso,verde,buzzer):
    global temperatura,umidita,causa
    if causa==0:
        if temperatura>35 and umidita<35:
            causa=3
            rosso.load (((1,500),(0,500)),0)
            buzzer.load(("E6",0),500,512,0)
            verde.off()
        elif temperatura>35:
            causa=2
            rosso.load (((1,500),(0,500)),0)
            buzzer.load(("E6",0),500,512,0)
            verde.off()
        elif umidita<35:
            causa=1
            rosso.load (((1,500),(0,500)),0)
            buzzer.load(("E6",0),500,512,0)
            verde.off()
        else:
            causa=0
            
    else:
        if temperatura>35 and umidita<35:
            causa=3
        elif temperatura>35:
            causa=2
        elif umidita<35:
            causa=1
        else:
            causa=0
            rosso.stop()
            buzzer.stop()
            verde.on()

        
        
    
    rosso.async_execute()
    buzzer.async_execute()
        
    
    
    
    

while True:
    if cronometro_misure.scaduto(1100):
        cronometro_misure.avanza(1100)
        effettua_misurazioni(sensor,ldr)
        aggiorna_schermo(display)
        if auto1:
            ventilazione_automatica(potenziometro,servo)
        else:
            ventilazione_manuale(potenziometro,servo)
            
        
    if auto1:
        schermatura_intelligente(step)
    else:
        schermatura_manuale(step)
    sistema_allarme(rosso,verde,buzzer)
    time.sleep_ms(10)
     