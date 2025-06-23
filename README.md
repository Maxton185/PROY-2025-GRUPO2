# PROY-2025-GRUPO2

Repositorio del grupo 2 para el proyecto del ramo *Proyecto Inicial* – 2025.

## 👥 Integrantes del grupo

| Nombre y Apellido | Usuario GitHub | Correo USM               | Rol          |
| ----------------- | -------------- | ------------------------ | ------------ |
| Luciano Acuña     | @elshanooooo   | lacunaf@usm.cl           | 202530032-k  |
| Ozman Morales     | @omoralesd     | omoralesd@usm.cl         | 202530041-9  |
| Martin Gajardo    | @maxton185     | mgajardom@usm.cl         | 202530033-8  |
| Sebastián gonzález | @S3B4ST14N-git| sgonzalezv@usm.cl        | 202530025-7  |

---

## 📝 Descripción breve del proyecto

 *Dispositivo portable capaz de detectar caídas y alertar mediante sonido he internet.*

---

## 🎯 Objetivos

- *Desarrollar un cinturón integrado con un giroscopio y un acelerómetro para detectar caídas en tiempo real, con el propósito de prevenir o mitigar lesiones en usuarios vulnerables (como adultos mayores o personas con movilidad reducida) mediante un sistema de alertas automáticas que active protocolos de asistencia inmediata:*

  - *Diseñar y construir el prototipo físico del cinturón con materiales ergonómicos, resistentes y adaptables a diferentes tallas para garantizar comodidad y portabilidad.*

  - *Implementar un sistema integrado de sensores (giroscopio y acelerómetro) capaz de medir en tiempo real la orientación, aceleración y cambios bruscos de movimiento.*

  - *Desarrollar un algoritmo de detección de caídas basado en datos de los sensores, diferenciando entre movimientos cotidianos (caminar, agacharse) y eventos de caída reales.*

  - *Crear un módulo de comunicación inalámbrica (Bluetooth, WiFi o GSM) para enviar alertas automáticas a dispositivos móviles, cuidadores o servicios de emergencia ante una caída detectada.*

  - *Incorporar un mecanismo de retroalimentación al usuario, en este caso un boton, para confirmar la detección y permitir cancelar falsas alarmas.*

  - *Validar el prototipo en entornos reales mediante pruebas con usuarios de grupos vulnerables (adultos mayores, personas con discapacidad) para ajustar sensibilidad y reducir falsos positivos.*

  - *Analizar datos recopilados por los sensores para mejorar patrones de detección y personalizar alertas según las necesidades del usuario.*

  - *Evaluar la relación costo-beneficio del dispositivo, asegurando que sea accesible para la población objetivo.*

---

## 🧩 Alcance del proyecto

 *Este proyecto posee una variedad de publicos objetivos:*
  - *Personas mayores (65+ años).*
  - *Personas con discapacidad fisica.*
  - *Cuidadores familiares (alerta de caida).*
  - *Personal de residencias geriátricas.*
  - *Deportistas extremos.*
  - *Trabajadores en alturas.*
    
---

## 🛠️ Tecnologías y herramientas utilizadas

- Lenguaje(s) de programación:
  - Microphyton
- Computador:
  - Raspberry Pi Pico 2 W 
- Componentes:
  - MPU6050.
  - buzzer.
  - pulsadores.
  - pantalla oled gme12864
---

## Intrucciones de uso

- Diagrama de conexion:
  - Raspberry a Mpu6050:
  - pin (Gpo) 0 : sda/mpu6050
  - pin (Gpo) 1 : scl/mpu6050
  - pin 40 : vcc/mpu6050
  - pin 37 : gnd/mpu6050
 
  - Raspberry a buzzer:
  - pin 5 : positive/buzzer
  - pin 8 : negarive/buzzer
 
  - Raspberry a botones:
  - pin 28 : pin 1/boton 1
  - pin 27 : pin 2/boton 1
  - pin 23 : pin 1/boton 2
  - pin 22 : pin 1/boton 2
  - pin 32 : pin 1/boton 3
  - pin 31 : pin 2/boton 3
 
  - Raspberry a oled:
  - pin 35 : pin vdd/oled
  - 
---
## 🗂️ Estructura del repositorio

```
/PROY-2025-GRUPOX
│
├── docs/               # Documentación general y reportes
├── src/                # Código fuente del proyecto
├── tests/              # Casos de prueba
├── assets/             # Imágenes, diagramas, etc.
└── README.md           # Este archivo
```

---

## 🧪 Metodología

*Metodologia de prototipado*

---

## 📅 Cronograma de trabajo


[Carta Gantt](https://docs.google.com/spreadsheets/d/100sGfFv-hZ-4b9II9qAl2fV0gZn1pVB36JyLCS3r4QU/edit?gid=0#gid=0)

---

## 📚 Bibliografía

[Pinout Rasperry pi pico w](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)

[Pinout Mpu6050](https://components101.com/sensors/mpu6050-module)

[WLAN](https://projects.raspberrypi.org/en/projects/get-started-pico-w)

[Thonny](https://thonny.org/)

[Telegram](https://core.telegram.org/bots/tutorial)

---

## 📌 Notas adicionales

> *Espacio para dejar cualquier comentario útil, como pendientes, acuerdos del grupo, consideraciones especiales, etc.*

## Video de youtube

[video](https://youtu.be/Az3OOnGK5uM)
