import utime
from machine import Pin
import time
from time import sleep_ms




class BUTTON:
    """
    Questa classe gestisce un bottone.
    Espone i metodi costruttore(n,mode,bounce_time), true_press() e set_handler(func).
    Dopo aver inizializzato un bottone, ricordati di settare l'handler. C'è un metodo apposito.
    """
    def __init__(self, n, mode, bounce_time):
        """
        Inizializza una nuova istanza.
        :parameter n           Il pin di ingresso.
        :parameter mode        Può asssumere due valori (+1 per la configurazione in pull up e -1 per la conf. in pull down)
        :parameter bounce_time Indica il tempo in ms sotto il quale una pressione del tasto è da ignorare
        """
        if(n<0 or n>39):
            self.__fatalError(1,n)
        elif(6<=n<=11):
            self.__fatalError(2,n)
        elif(34<=n<=39):
            print ("--- WARNING: i pin dal 34 al 39 non hanno le resistenze di pullup o pulldown. Mettile tu o cambia pin! ---")
        
        if (mode==+1):
            self.button=Pin(n, Pin.IN, Pin.PULL_UP)
        elif (mode==-1):
            self.button=Pin(n, Pin.IN, Pin.PULL_DOWN)
        else:
            self.__fatalError(3,mode)
        self.mode=mode
        if (bounce_time<0):
            self.__fatalError(4,bounce_time)
        self.last_press_time=-bounce_time
        self.bounce_time=bounce_time
            
        
    def __fatalError (self,err,arg):
        """PRIVATO. Arresta il sistema se succede qualcosa di inaspettato"""
        print("--- ERRORE ---")
        if (err==1):
            raise Exception(f"Il pin {arg} non è un pin valido!")
        elif (err==2):
            raise Exception(f"Il pin {arg} non è utilizzabile per i bottoni!")
        elif (err==3):
            raise Exception(f"L'argomento {arg} non è valido. Inserisci -1 o +1 per configurare il bottone in modalità pull up o pull down!")
        elif (err==4):
            raise Exception(f"Il tempo {arg} è negativo. Metti 0 o un numero positivo in ms!")
        elif (err==5):
            raise Exception(f"L'evento {arg} non è valido. Metti 1,10 o 11!")

        
    def true_press (self):
        """
        Da chiamare ogni volta che il bottone viene premuto.
        :return un booleano per confermare che la pressione di un tasto non sia conseguenza del bouncing.	
        """
        current_time=time.ticks_ms()
        delay = time.ticks_diff(current_time, self.last_press_time)
        self.last_press_time=current_time
        if (delay>self.bounce_time):
            return True
        else:
            return False
            
    def set_handler (self, func, event):
        """
        Associa una funzione handler alla pressione del bottone
        :parameter func           La funzione che opera da handler
        :parameter event           L'evento che chiama l'handler (10= press, 1=release, 11= press e release)
        """
        if(event not in (10,11,1)):
            self.__fatalError(5,event)
        
        if(event==11):
            self.button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = func)
        elif(self.mode==1):
            if(event==10):
                self.button.irq(trigger=Pin.IRQ_FALLING, handler = func)
            else:
                self.button.irq(trigger=Pin.IRQ_RISING, handler=func)
        else:
            if(event==10):
                self.button.irq(trigger=Pin.IRQ_RISING, handler=func)
            else:
                self.button.irq(trigger=Pin.IRQ_FALLING, handler = func)
              





class LED:
    """ 
    Questa classe gestisce un led.
    Espone i metodi costruttore(n), on(), off() e toggle().
    Dopo che hai inzializzato il led, ricordati di forzarlo a uno stato iniziale
    """
    def __init__(self, n):
        """
        Inizializza una nuova istanza.
        :parameter n    Il pin da associare al controllo del led.
        """
        if(n<0 or n>39):
            self.__fatalError(1,n)
        elif(6<=n<=11 or 34<=n<=39):
            self.__fatalError(2,n)
        self.led=Pin(n, Pin.OUT)
        
    def __fatalError (self,err,arg):
        """PRIVATO. Arresta il sistema se succede qualcosa di inaspettato"""
        print("--- ERRORE ---")
        if (err==1):
            raise Exception(f"Il pin {arg} non è un pin valido!")
        elif (err==2):
            raise Exception(f"Il pin {arg} non è utilizzabile per i led!")
        
        
    def on (self):
        """
        Accende il led.
        """
        self.led.value(1)
        
    def off (self):
        """
        Spegne il led
        """
        self.led.value(0)
        
    def toggle (self):
        """
        Commuta il led
        """
        self.led.value(not self.led.value())









# Definisco i pin per stepper motor
IN1=Pin(26, Pin.OUT)
IN2=Pin(25, Pin.OUT)
IN3=Pin(33, Pin.OUT)
IN4=Pin(32, Pin.OUT)

stepper_pins = [IN1, IN2, IN3, IN4]

# full-step con 2 bobine attive per ogni step
# due bobine accese per ogni step -> più coppia
# il valore (0=spento, 1=acceso) da dare a quel pin nel passo corrente.
step_sequence = [
    [1, 0, 0, 1],  
    [1, 1, 0, 0],  
    [0, 1, 1, 0],  
    [0, 0, 1, 1],  
]#4 step

# la half-step corrispondente (8 stati) è questa:
# Half-step (mezzo passo): alterna 1 bobina e 2 bobine
step_sequence_half = [
    [1,0,0,0],  # solo IN1
    [1,0,0,1],  # IN1+IN4
    [0,0,0,1],  # solo IN4
    [0,0,1,1],  # IN3+IN4
    [0,0,1,0],  # solo IN3
    [0,1,1,0],  # IN2+IN3
    [0,1,0,0],  # solo IN2
    [1,1,0,0],  # IN1+IN2
]
#8step
#direction = +1 (antiorario), -1 (orario)
#steps = numero di passi da eseguire
#delay = tempo tra un passo e l'altro
#step_index tiene traccia della posizione corrente
#nella sequenza di attivazione (fase) del motore.

def step(direction, steps, delay,lista):
    global step_index 
    for i in range(steps):
        # l'operatore % garantisce che step_index rimanga all'interno dell'intervallo valido,
        # assicurando che la sequenza dei passi venga ripetuta ciclicamente.
        # indica la riga quindi quale passo
        step_index = (step_index + direction) % len(lista)
        
        
        #pin_index determina la colonna (quindi la bobbina)
        for pin_index in range(len(stepper_pins)):
            #Esempio: se step_index = 2, la sequenza è [0, 1, 1, 0]
            # Se pin_index = 0 → pin_value = 0
            # Se pin_index = 1 → pin_value = 1
            # Se pin_index = 2 → pin_value = 1
            # Se pin_index = 3 → pin_value = 0
            pin_value = lista[step_index][pin_index]
            #Scrive il valore sul pin fisico, accendendo o spegnendo la bobina
            stepper_pins[pin_index].value(pin_value)
        
        #Aspetta il tempo delay prima di passare al prossimo passo.
        #Pausa più corta → motore più veloce. Pausa più lunga → motore più lento.
        utime.sleep(delay)
last_on=0
stato=False
def hand(irq):
    print(5)
    global stato,bottone    
    if(bottone.true_press()):
        stato=not stato


bottone=BUTTON(17,+1,250)
bottone.set_handler(hand,11)
led=LED(16)
led.off()
step_index = 0

while(True):
    print(10)
    if(stato):
        step(1, 1, 0.005,step_sequence)
        led.on()
    else:
        led.off()
    sleep_ms(10)
    
        
    

