from machine import Pin
import time

# Usamos el pin 25 que está conectado al LED integrado en la Raspberry Pi Pico W
led = Pin("LED", Pin.OUT)

while True:
    led.toggle()       # Cambia el estado del LED (on/off)
    time.sleep(1)
