#############################################
#Desarrollado por: Jeremías Emmanuel Miranda#
#Control de Humedad y Temperatura           #
#############################################

from machine import Pin
import dht
import time

sensor_dht = dht.DHT11(Pin(4))

last_temp = 25
last_hum = 50

def leer_clima():

    global last_temp, last_hum

    for _ in range(3):

        try:
            sensor_dht.measure()

            temp = sensor_dht.temperature()
            hum = sensor_dht.humidity()

            # Validaciones
            if temp < 0 or temp > 60:
                continue

            if hum < 0 or hum > 100:
                continue

            # Suavizado simple
            temp = (last_temp * 0.7) + (temp * 0.3)
            hum = (last_hum * 0.7) + (hum * 0.3)

            last_temp = temp
            last_hum = hum

            return round(temp, 1), round(hum, 1)

        except Exception as e:
            print("DHT ERROR:", e)

        time.sleep_ms(200)

    return last_temp, last_hum