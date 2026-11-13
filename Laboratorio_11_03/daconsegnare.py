

from machine import ADC, Pin,PWM
import time

class PuWM:
  """
  Questa classe modella un led o qualsiasi componente controllato con la PWM (pulse width modulation).
  Espone i metodi costruttore(n,f), set_duty(d), set_freq(f)
  """

  def __init__(self, n, f=5000):
    """
    Inizializza una nuova istanza.
    :parameter n Il pin che va connesso al componente da controllare.
    :parameter f Il valore della frequenza
    """
    if(n<0 or n>39):
      self.__fatalError(1,n)
    elif(34<= n<= 39 or 6<=n<=11):
      self.__fatalError(2,n)
    self.pwm=PWM(Pin(n))
    self.set_duty(0)
    self.set_freq(f)

  def __fatalError (self,err,arg):
    """PRIVATO. Arresta il sistema se succede qualcosa di inaspettato"""
    print("--- ERRORE ---")
    if (err==1):
      raise Exception(f"Il pin {arg} non è un pin valido!")
    elif (err==2):
      raise Exception(f"Il pin {arg} non è utilizzabile per un PWM!")
    elif (err==3):
      raise Exception(f"Non puoi settare il duty a {arg}!")
    elif (err==4):
      raise Exception(f"Non puoi settare la frequenza a {arg}!")
          
  def set_duty(self,d):
    """
    Setta una nuova duty.
    :parameter d La nuova percentuale di tempo alto (espressa da 0 a 1023)
    """
    if(d<0 or d>1023):
      self.__fatalError (3,d)
    self.pwm.duty(d)
    
  def set_freq(self,f):
    """
    Setta una nuova frequenza.
    :parameter f La nuova frequenza (come valore da 0 a 5000)
    """
    if(f>5000 or f<1): #meglio non gestire f=0 modificando il duty, principio del least surprise
      self.__fatalError(4,f)
    self.pwm.freq(f)
  
  
class LDR:
    """This class read a value from a light dependent resistor (LDR)"""

    def __init__(self, pin, min_value=0, max_value=100):
        """
        Initializes a new instance.
        :parameter pin A pin that's connected to an LDR.
        :parameter min_value A min value that can be returned by value() method.
        :parameter max_value A max value that can be returned by value() method.
        """
        if min_value >= max_value:
            raise Exception('Min value is greater or equal to max value')

        # initialize ADC (analog to digital conversion)
        # create an object ADC
        self.adc = ADC(Pin(pin))
        self.min_value = min_value
        self.max_value = max_value

    def read(self):
        """
        Read a raw value from the LDR.
        :return a value from 0 to 4095.
        """
        return self.adc.read()

    def value(self):
        """
        Read a value from the LDR in the specified range.
        :return a value from the specified [min, max] range.
        """
        return (self.max_value - self.min_value) * self.read() / 4095


# initialize an LDR
ldr = LDR(34)
# === AGGIUNTA: Inizializzazione del buzzer sul Pin 22 ===
buzzer = PWM(Pin(22, Pin.OUT), freq=2000)


sg90 = PWM(Pin(23, mode=Pin.OUT))
sg90.freq(50) # Periodo di 20 ms (50 Hz)
ledblue= PuWM(25)
ledred= PuWM(26)
ledgreen= PuWM(27)



while True:
    # read a value from the LDR
    value1 = ldr.read()
    print('analog value= {}'.format(value1))
    value = ldr.value()
    print('value = {}'.format(value))

    
    if value < 20:
        buzzer.duty(0)    
        sg90.duty(26)
        ledblue.set_duty(1+10*int(value))
        ledgreen.set_duty(1+10*int(value))
        ledred.set_duty(1+10*int(value))
    elif value<50:
        buzzer.duty(0)    
        sg90.duty(76)
        ledblue.set_duty(1+10*int(value))
        ledgreen.set_duty(1+10*int(value))
        ledred.set_duty(1+10*int(value))
    else:
        buzzer.duty(512)    
        sg90.duty(100)
        ledblue.set_duty(0)
        ledgreen.set_duty(0)
        ledred.set_duty(1023)
        #ledblue.value(0)


    # a little delay
    time.sleep(1)

