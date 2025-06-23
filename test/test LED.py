import machine
import time

led = machine.Pin(15, machine.Pin.OUT)  # Usa GP15 como salida
led.on()  # Enciende el LED

# Si quieres mantenerlo encendido por 5 segundos:
time.sleep(5)
led.off()  # Apaga el LED después
