from machine import Pin, ADC
import time

adc = ADC(Pin(34, mode=Pin.IN))
adc.atten(ADC.ATTN_11DB)  # Misura 0-3.3V


while True:
    # Read ADC and convert to voltage
    #This method returns the raw ADC value ranged according to the resolution of the block,
    #e.g., 0-4095 for 12-bit resolution.
    val = adc.read()
    val = val * (3.3 / 4095)
    print(round(val, 2), "V") # Keep only 2 digits

    # Wait a bit before taking another reading
    time.sleep_ms(100)