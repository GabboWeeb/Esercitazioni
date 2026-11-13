from LDR import LDR
from DimmableLed import DimmableLed
from Potentiometer import Potentiometer
from Servomotor import Servomotor
from StepMotor import StepMotor
from Button import Button
from Buzzer import Buzzer
from Led import Led
import time
import math

        
potenziometro = Potentiometer(34,0,4095)#blu
fotoresistore = LDR(33,0,4095)#arancione
led = Led(14)
servo= Servomotor(32)
servo.set_angle(0)
step=StepMotor(15,16,17,18)
target_angle=0
curr_angle=0
button=Button(4,1,250)#bianco


#handler
lista_cifre=[0,0,0,0]
next_cifra=0
current_time=0
def change(irq):
    global current_time
    current_time=time.ticks_ms()
    global button,lista_cifre,next_cifra,cifra
    #print("AAAAAA")
    if button.true_press()==True:
        lista_cifre[next_cifra]=cifra
        next_cifra=next_cifra+1
        if next_cifra==4:
            next_cifra=0
            verifica_codice(lista_cifre)

button.set_handler(change,10)


#buzzer
buzzer=Buzzer(26)

#letture dei sensori
pot_read=0
fot_read=0



#acquisizione della cifra
def leggi_sensori():
    global pot_read,fot_read
    global potenziometro,fotoresistore
    pot_read= potenziometro.read()
    fot_read= fotoresistore.read()
    print(f"Il potenziometro legge {pot_read} \t il fotoresistore legge {fot_read}")

global cifra

def acquisisci_cifra():
    global pot_read,cifra
    risultato = math.floor(( pot_read * 10) / 4096)
    cifra= min(9, risultato)
    segnala_cifra(cifra)

def controllo_cifra():
    global pot_read,potenziometro
    lettura_corrente=potenziometro.read()
    
    if pot_read-30<=lettura_corrente<=pot_read+30:    
        return False
    else:
        return True
    

def segnala_cifra(cifra):
    """
    Mostra la cifra selezionata tramite lampeggi LED:
    - 0: Un lampeggio lungo di 800 ms
    - 1: Un lampeggio breve (100 ms)
    - 2..9: Due a nove lampeggi brevi (100 ms l'uno, con 150 ms di pausa)
    """
    global potenziometro
    # Spegne il LED all'inizio per sicurezza
    led.off()
    time.sleep_ms(300) # Piccola pausa prima di iniziare la sequenza
    
    if cifra == 0:
        # Cifra 0: Un lampeggio lungo di 800 ms
        led.on()
        time.sleep_ms(800)
        led.off()
        
    elif 1 <= cifra <= 9:
        # Cifre da 1 a 9: Sequenza di lampeggi brevi
        for i in range(cifra):
            if controllo_cifra():
                break
            # Accensione lampeggio breve (100 ms)
            led.on()
            time.sleep_ms(100)
            
            # Spegnimento
            led.off()
            
            # Pausa tra lampeggi consecutivi (150 ms), 
            # ma evitiamo la pausa dopo l'ultimo lampeggio della sequenza
            if i < cifra - 1:
                time.sleep_ms(150)
    

def verifica_codice(lista_cifre):
    global buzzer,counter
    if(lista_cifre==[3,7,1,9]):
        print("Corretto")
        buzzer.play(["FS6",0,"FS6"], 150, 32)
        led.on()
        time.sleep(2)
        led.off()
        sblocco_sistema()
        counter=0
        
    else:
        print("Non corretto")
        buzzer.play(["G4"], 500, 32)
        for cont in range(3):
            led.on()
            time.sleep_ms(100)
            led.off()
            time.sleep_ms(100)
        
        blocco_temporaneo()
        
     
mode = True #True è abilitato, False è bloccato
counter=0
def blocco_temporaneo():
    global counter,mode,button,led
    counter+=1
    if counter==3:
        block_start=time.ticks_ms()
        delay=0
        gestione_led=0
        gestione_buzzer=0
        buzzer.set_freq(800)
        button.set_handler(None,10)
        blocco_motore()
        while delay<30_000:
            delay=time.ticks_diff(time.ticks_ms(),block_start)
            gestione_led=delay%500
            gestione_buzzer=delay%5_000
            if gestione_led<250:
                led.on()
            else:
                led.off()
  
            if gestione_buzzer<1_000:
                buzzer.set_duty(32)
            else:
                buzzer.set_duty(0)     
        button.set_handler(change,10)
    else:
        return

def blocco_motore():
    pass
        
def sblocco_sistema():
    pass
    
def gestisci_autenticazione(): pass 
def gestisci_servo(): pass
def gestisci_stepper(): pass
def rileva_intrusione(): pass 
def gestisci_allarmi(): pass
def gestisci_buzzer(): pass
def gestisci_pulsante(): pass
def aggiorna_stato(): pass

while True:
    print(lista_cifre)
    leggi_sensori()
    acquisisci_cifra()
    
    delay = time.ticks_diff(time.ticks_ms(),current_time)
    if (delay>99_000):
        lista_cifre=[0,0,0,0]
    
    time.sleep_ms(1000)