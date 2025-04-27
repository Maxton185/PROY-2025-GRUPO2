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
UMBRAL_ACEL = 5.2  # Gs
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
    <h1>Monitor de Cadías</h1>
    <p id="estado">Cargando...</p>
</body>
</html>
"""

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
        request = cl.recv(1024)
        request_str = str(request)

        if "GET /estado" in request_str:
            estado = "SIN caídas recientes"
            if ultima_caida and time.time() - ultima_caida < 10:
                estado = "⚠️ ¡Caida detectada!"
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

# Lanzar el servidor en segundo plano
_thread.start_new_thread(servidor_web, ())

# Bucle principal
while True:
    acel = sensor.get_accel_data()
    gyro = sensor.get_gyro_data()

    if detectar_caida(acel, gyro):
        print("🚨 ¡Caída detectada!")
        ultima_caida = time.time()

        # ACTIVAR BUZZER
        buzzer.on()
        time.sleep(1)
        buzzer.off()
        
        time.sleep(2)

    time.sleep(0.2)
