
from LDR import LDR
from DimmableLed import DimmableLed
from Potentiometer import Potentiometer
from Servomotor import Servomotor
from StepMotor import StepMotor
from Button import Button
from Buzzer import Buzzer
import time

        
potenziometro = Potentiometer(34,1000,3000)
fotoresistore = LDR(33,0,4095)
led = DimmableLed(14)
servo= Servomotor(32)
servo.set_angle(0)
step=StepMotor(15,16,17,18)
target_angle=0
curr_angle=0

target_verso=-1
curr_steps=0
max_steps=512
stato_step=False #false=orario, true=antiorario

#bottone
button=Button(4,1,250)
mode = False #false= auto , true=manual
already_switched=False
#handler
def change(irq):
    global mode,button
    if button.true_press()==True:
        mode= not mode

button.set_handler(change,10)


#buzzer
buzzer=Buzzer(26)
buzzer.play(["B5"], 200)

#contatore per la luminosità
cont_lum=0

while True:
    soglia= potenziometro.value()
    lum= fotoresistore.read()
    diff_soglia=soglia-lum
    print(f"Soglia: {soglia} \t \t e lum: {lum}\n La differenza è {diff_soglia} \t il target è {target_angle}\t il current è {curr_angle} \n il tar verso è {target_verso} \t il current step è {curr_steps}. Stato={stato_step}")
    print(f"Lo stato del bottone è {mode}")
    if mode==False: #auto
        if not already_switched:
            buzzer.play(["B6"], 300)
        already_switched=True
        if diff_soglia >800:
            led.set_lum_perc(100)
        elif diff_soglia >400:
            led.set_lum_perc(70)
        elif diff_soglia >100:
            led.set_lum_perc(30)
        else:
            led.off()
        
        #gestione del servo
        if lum<soglia:
            target_angle=0
        elif soglia<=lum<=soglia+500:
            target_angle=45
        elif lum>soglia+500:
            target_angle=90
        if target_angle>curr_angle:
            curr_angle+=5
            servo.set_angle(curr_angle)
        elif target_angle==curr_angle:
            pass
        elif target_angle<curr_angle:
            curr_angle-=5
            servo.set_angle(curr_angle)

        #gestione dello step
        if lum<soglia:
            if target_verso==1:
                target_verso=-1
                curr_steps=0
        if lum>=soglia:
            if target_verso==-1:
                target_verso=1
                curr_steps=0
        
        if curr_steps!=max_steps:
            curr_steps+=8
            step.step(target_verso, 8, 15, "HALF")
    else: #manuale
        led.set_duty(int((soglia-1000)/2000*1023))
        servo.set_angle(90)
        if already_switched:
            buzzer.play(["FS6",0,"FS6"], 100)
            step.step(-1, 256, 15, "HALF")
        already_switched=False        
    
    if lum<500:
        cont_lum+=1
    if cont_lum==4:
        cont_lum=0
        buzzer.play(["G5",0,"G5",0,"G5"], 150)
        
    
    time.sleep_ms(1000)




