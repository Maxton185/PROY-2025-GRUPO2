import machine
import time
import network
import socket
import ubinascii
import urequests
from mpu6050 import MPU6050
import ssd1306

# ===== Configuración general =====
PUERTO = 8080
SSID = "Italiano"
PASSWORD = "Parinha2025"

# Telegram
TG_BOT_TOKEN = "8025777647:AAEujn_mRNYcGjHYV47oz80Q_AuTkdfHYrE"
TG_CHAT_ID = "6689006729"

# ===== Pines y periféricos =====
i2c_sensor = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
sensor = MPU6050(i2c_sensor)

i2c_oled = machine.I2C(1, sda=machine.Pin(6), scl=machine.Pin(7))
oled = ssd1306.SSD1306_I2C(128, 64, i2c_oled)

buzzer = machine.Pin(3, machine.Pin.OUT)
btn_wifi = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
btn_modo = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
btn_panico = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)

# ===== Estados globales =====
wifi_conectado = False
current_user = None
caida_activa = False
buzzer_state = False
contador_caidas = 0
modo_actual = 0
ultimo_cambio_modo = 0

# ===== Modos de operación refinados =====
MODOS = [
    {"nombre": "Cotidiano", "acc_umbral": 0.80, "gyro_umbral": 50},
    {"nombre": "Deportivo", "acc_umbral": 0.60, "gyro_umbral": 100},
    {"nombre": "Descanso", "acc_umbral": 0.40, "gyro_umbral": 150}
]

usuarios = {
    "Maxton": "maxton185",
    "user1": "pass1",
}
historial_per_user = {u: [] for u in usuarios}

def mostrar_estado():
    oled.fill(0)
    modo = MODOS[modo_actual]
    oled.text(f"Modo: {modo['nombre']}", 0, 0)
    estado_wifi = "WiFi: ON" if wifi_conectado else "WiFi: OFF"
    oled.text(estado_wifi, 0, 16)
    estado_deteccion = "CAIDA ACTIVA!" if caida_activa else "Monitorizando"
    oled.text(estado_deteccion, 0, 32)
    oled.text(f"Caidas: {contador_caidas}", 0, 48)
    oled.show()

def alerta_telegram(msg):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": msg}
    try:
        r = urequests.post(url, json=payload)
        r.close()
    except Exception as e:
        print("Error Telegram:", e)

wlan = network.WLAN(network.STA_IF)

def iniciar_wifi():
    global wifi_conectado
    print("Esperando botón WiFi (GP27)...")
    oled.fill(0)
    oled.text("Presione BTN WiFi", 0, 24)
    oled.show()
    while btn_wifi.value():
        time.sleep(0.1)
    print("Conectando a Wi-Fi...")
    oled.fill(0)
    oled.text("Conectando WiFi", 0, 24)
    oled.show()
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    intentos = 0
    while not wlan.isconnected() and intentos < 20:
        time.sleep(0.5)
        intentos += 1
    if wlan.isconnected():
        print("Wi-Fi OK, IP:", wlan.ifconfig()[0])
        wifi_conectado = True
        iniciar_servidor()
        buzzer.value(1)
        time.sleep(0.3)
        buzzer.value(0)
    else:
        print("Error WiFi")
        oled.fill(0)
        oled.text("Error WiFi", 0, 24)
        oled.show()

servidor_socket = None

def iniciar_servidor():
    global servidor_socket
    try:
        addr = socket.getaddrinfo("0.0.0.0", PUERTO)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(1)
        s.bind(addr)
        s.listen(1)
        servidor_socket = s
        print(f"Servidor HTTP escucha en puerto {PUERTO}")
    except Exception as e:
        print("Error al iniciar servidor:", e)

def manejar_cliente():
    global current_user
    if not servidor_socket:
        return
    try:
        cl, addr = servidor_socket.accept()
    except:
        return
    try:
        req = cl.recv(1024).decode("utf-8", "ignore")
        user = None
        if "Authorization: Basic " in req:
            cred = req.split("Authorization: Basic ")[1].split("\r\n")[0]
            u, p = ubinascii.a2b_base64(cred).decode().split(":")
            if u in usuarios and usuarios[u] == p:
                user = u
        if not user:
            cl.send("HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm=\"Acceso\"\r\n\r\n")
            cl.close()
            return
        current_user = user
        if "GET /estado" in req:
            estado = "¡¡CAÍDA!!" if caida_activa else "SIN CAÍDAS"
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + estado)
        elif "GET /historial" in req:
            lines = historial_per_user.get(current_user, [])[-10:]
            body = "<br>".join(lines)
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + body)
        elif "GET /borrar" in req:
            historial_per_user[current_user] = []
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHistorial borrado")
        else:
            page = """HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head><title>Monitor Caidas - """ + current_user + """</title>
<script>
function update() {
  fetch('/estado').then(r=>r.text()).then(t=>document.getElementById('e').innerText=t);
  fetch('/historial').then(r=>r.text()).then(h=>document.getElementById('h').innerHTML=h);
}
setInterval(update,1000);
</script>
</head>
<body>
  <h1>Caidas (""" + current_user + """</h1>
  <p id="e">Cargando...</p>
  <h2>Historial</h2>
  <div id="h">Cargando...</div>
  <button onclick="fetch('/borrar').then(update)">Borrar historial</button>
</body>
</html>"""
            cl.send(page)
    except Exception as e:
        print("Error cliente:", e)
    finally:
        cl.close()

def detectar_caida():
    global caida_activa, contador_caidas
    modo = MODOS[modo_actual]
    try:
        accel = sensor.get_accel_data()
        gyro = sensor.get_gyro_data()
        total_acc = (accel['x']**2 + accel['y']**2 + accel['z']**2)**0.5
        total_gyro = max(abs(gyro['x']), abs(gyro['y']), abs(gyro['z']))
        if not caida_activa and (total_acc < modo['acc_umbral'] and total_gyro > modo['gyro_umbral']):
            caida_activa = True
            contador_caidas += 1
            ts = time.localtime()
            s_ts = f"{ts[3]:02d}:{ts[4]:02d}:{ts[5]:02d}"
            texto = f"Caída ({modo['nombre']}) a las {s_ts}"
            user = current_user or "Anon"
            if user not in historial_per_user:
                historial_per_user[user] = []
            historial_per_user[user].append(texto)
            alerta_telegram(f"[{user}] {texto}")
            print("Caída detectada:", texto)
    except Exception as e:
        print("Error detección:", e)

def cambiar_modo():
    global modo_actual, ultimo_cambio_modo
    ahora = time.ticks_ms()
    if time.ticks_diff(ahora, ultimo_cambio_modo) > 500:
        modo_actual = (modo_actual + 1) % len(MODOS)
        ultimo_cambio_modo = ahora
        print(f"Modo cambiado a: {MODOS[modo_actual]['nombre']}")
        buzzer.value(1)
        time.sleep(0.1)
        buzzer.value(0)
        mostrar_estado()

print("Iniciando sistema...")
mostrar_estado()
ultimo_actualizacion = time.ticks_ms()
ultimo_lectura = time.ticks_ms()
iniciar_wifi()

while True:
    if not btn_modo.value():
        cambiar_modo()
        time.sleep(0.3)
    if time.ticks_diff(time.ticks_ms(), ultimo_lectura) > 100:
        detectar_caida()
        ultimo_lectura = time.ticks_ms()
    if caida_activa:
        buzzer_state = not buzzer_state
        buzzer.value(buzzer_state)
        if not btn_panico.value():
            caida_activa = False
            buzzer.value(0)
            print("Alarma parada")
            time.sleep(0.3)
        time.sleep(0.5)
    else:
        buzzer.value(0)
    if not btn_wifi.value() and not btn_modo.value() and not btn_panico.value():
        ts = time.localtime()
        s_ts = f"{ts[3]:02d}:{ts[4]:02d}:{ts[5]:02d}"
        texto = f"PANICO a las {s_ts}"
        user = current_user or "Anon"
        if user not in historial_per_user:
            historial_per_user[user] = []
        historial_per_user[user].append(texto)
        alerta_telegram(f"[{user}] {texto}")
        print("Botón de pánico activado")
        for _ in range(6):
            buzzer.value(1)
            time.sleep(0.7)
            buzzer.value(0)
            time.sleep(0.7)
        time.sleep(1)
    if time.ticks_diff(time.ticks_ms(), ultimo_actualizacion) > 500:
        mostrar_estado()
        ultimo_actualizacion = time.ticks_ms()
    manejar_cliente()
    time.sleep(0.05)