import machine
import time
import network
import socket
from mpu6050 import MPU6050
import _thread

# I2C y sensor
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))  
sensor = MPU6050(i2c)

# Buzzer
buzzer = machine.Pin(3, machine.Pin.OUT)
buzzer.off()

# Pulsadores
boton_wifi = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)  
boton_2 = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)     
boton_3 = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)    

# Variables Wi-Fi
SSID = "Italiano"
PASSWORD = "Parinha2025"
wlan = network.WLAN(network.STA_IF)

# Configuración de caída
ultima_caida = None
UMBRAL_ACEL = 3.5  # Gs
UMBRAL_GYRO = 200  # °/s

# HTML principal
def html_principal():
    return """\
HTTP/1.1 200 OK

<html>
<head>
    <title>Monitor de Caidas</title>
    <script>
    function actualizarEstado() {
        fetch('/estado')
            .then(response => response.text())
            .then(data => {
                document.getElementById('estado').innerText = data;
            });
    }
    setInterval(actualizarEstado, 1000);
    </script>
</head>
<body>
    <h1>Monitor de Caídas</h1>
    <p id="estado">Cargando...</p>
</body>
</html>
"""

# Servidor web
def servidor_web():
    global ultima_caida

    while True:
        try:
            addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
            s = socket.socket()
            s.bind(addr)
            s.listen(1)
            print("Servidor web iniciado en puerto 8080")
            break
        except OSError as e:
            if e.errno == 98:  # EADDRINUSE
                print("⚠️ Puerto ocupado, intentando liberar...")
                time.sleep(1)
            else:
                raise e

    while True:
        cl, addr = s.accept()
        print("Cliente web:", addr)
        request = cl.recv(1024)
        request_str = str(request)

        if "GET /estado" in request_str:
            estado = "SIN caídas recientes"
            if ultima_caida and time.time() - ultima_caida < 30:
                estado = "⚠️ ¡Caída detectada!"
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + estado
            cl.send(response)
        else:
            cl.send(html_principal())

        cl.close()

# Detección de caída
def detectar_caida(acel, gyro):
    ax, ay, az = acel['x'], acel['y'], acel['z']
    gx, gy, gz = gyro['x'], gyro['y'], gyro['z']
    total_acel = (ax**2 + ay**2 + az**2)**0.5
    total_gyro = max(abs(gx), abs(gy), abs(gz))
    return total_acel > UMBRAL_ACEL or total_gyro > UMBRAL_GYRO

# 🛑 Esperar botón para conectar Wi-Fi
print("Esperando que presiones el botón para conectar WiFi...")
while boton_wifi.value() == 1:
    time.sleep(0.1)

print("¡Botón presionado! Conectando a WiFi...")
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Conectando...")
    time.sleep(1)

ip = wlan.ifconfig()[0]
print("¡Conectado a WiFi! IP:", ip)

# Iniciar servidor web
_thread.start_new_thread(servidor_web, ())

# Bucle principal
while True:
    # Leer botones
    b1 = boton_wifi.value() == 0
    b2 = boton_2.value() == 0
    b3 = boton_3.value() == 0
    botones_presionados = b1 + b2 + b3

    if botones_presionados == 1:
        if b2:
            print("Botón 2 presionado: Sonar buzzer 0.2s")
            buzzer.on()
            time.sleep(0.2)
            buzzer.off()
        elif b3:
            print("Botón 3 presionado: (sin acción individual aún)")
            # Aquí puedes poner otra acción si quieres para el botón 3 individualmente
    elif botones_presionados == 3:
        print("🚨 Los 3 botones presionados: Sonar 3 veces 0.5s")
        for _ in range(3):
            buzzer.on()
            time.sleep(0.5)
            buzzer.off()
            time.sleep(0.5)
    # Si se presionan 2 botones: no hacer nada

    # Detección de caídas
    acel = sensor.get_accel_data()
    gyro = sensor.get_gyro_data()

    if detectar_caida(acel, gyro):
        print("🚨 ¡Caída detectada!")
        ultima_caida = time.time()

        buzzer.on()
        time.sleep(0.5)
        buzzer.off()

        time.sleep(2)

    time.sleep(0.1)
