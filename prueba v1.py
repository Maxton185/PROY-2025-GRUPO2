import machine
import urequests
import time
import network
import socket
from mpu6050 import MPU6050

# I2C y sensor
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
sensor = MPU6050(i2c)

# Conexión Wi-Fi
SSID = "Italiano"
PASSWORD = "Parinha2025"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

ip = wlan.ifconfig()[0]
print("Conectado con IP:", ip)

# Configuración de caída
ultima_caida = None
UMBRAL_ACEL = 2.5  # Gs
UMBRAL_GYRO = 250  # °/s

# Servidor web
def servidor_web():
    global ultima_caida

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Servidor web iniciado")

    while True:
        cl, addr = s.accept()
        print("Cliente web:", addr)
        cl.recv(1024)

        estado = "SIN caídas detectadas recientemente"
        if ultima_caida and time.time() - ultima_caida < 30:
            estado = "⚠️ ¡Caída detectada hace poco!"

        html = f"""\
HTTP/1.1 200 OK

<html>
    <head><title>Estado de Caídas</title></head>
    <body>
        <h1>Monitor de Caídas</h1>
        <p>{estado}</p>
    </body>
</html>
"""
        cl.send(html)
        cl.close()

# Detección de caída
def detectar_caida(acel, gyro):
    ax, ay, az = acel['x'], acel['y'], acel['z']
    gx, gy, gz = gyro['x'], gyro['y'], gyro['z']
    total_acel = (ax**2 + ay**2 + az**2)**0.5
    total_gyro = max(abs(gx), abs(gy), abs(gz))
    return total_acel > UMBRAL_ACEL or total_gyro > UMBRAL_GYRO

# Lanzar el servidor en segundo plano
import _thread
_thread.start_new_thread(servidor_web, ())

# Bucle principal
while True:
    acel = sensor.get_accel_data()
    gyro = sensor.get_gyro_data()

    if detectar_caida(acel, gyro):
        print("🚨 ¡Caída detectada!")
        ultima_caida = time.time()
        time.sleep(2)

    time.sleep(0.2)