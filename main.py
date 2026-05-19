#############################################
#Desarrollado por: Jeremías Emmanuel Miranda#
#Archivo principal                          #
#############################################

from machine import Pin, I2C
import time
import network
import _thread

from config import *
from sensors import ADS1115, promedio_lectura, calcular_rs
from validations import validar_sensor
from display import init_display, mostrar_error, mostrar_datos
from webserver import iniciar_servidor
from calibration import calibrar
from gas_model import ratio_a_ppm, MQ2_CURVA, MQ3_CURVA, MQ135_CURVA
from climate import leer_clima
from alarma import beep, alarma_estado, alarma_off, startup_sound

# =========================
# I2C + OLED
# =========================
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = init_display(i2c)

# =========================
# TEST SONORO
# =========================
startup_sound()
beep(2, 0.05)

# =========================
# WIFI (NO BLOQUEANTE)
# =========================
wlan = network.WLAN(network.STA_IF)

wlan.active(False)
time.sleep(1)

wlan.active(True)
wlan.connect(SSID, PASSWORD)

wifi_ok = False
ip = "NO WIFI"

for i in range(10):  # no bloquea
    if wlan.isconnected():
        wifi_ok = True
        ip = wlan.ifconfig()[0]
        break
    time.sleep(1)

print("WiFi:", wifi_ok)
print("IP:", ip)

# =========================
# DETECTAR ADS
# =========================
devices = i2c.scan()
print("I2C devices:", devices)

ads = ADS1115(i2c, devices[-1]) if len(devices) > 1 else None

if ads:
    Ro = calibrar(oled, ads, promedio_lectura)
else:
    Ro = None

# =========================
# ESTADO GLOBAL
# =========================
data_global = {
    "mq2": 0,
    "mq3": 0,
    "mq135": 0,
    "temp": 0,
    "hum": 0,
    "estado": "INIT"
}

def get_data():
    return data_global

# =========================
# SERVIDOR SOLO SI HAY WIFI
# =========================
if wifi_ok:
    _thread.start_new_thread(iniciar_servidor, (get_data,))
    beep(2, 0.05)
else:
    print("Servidor desactivado (sin WiFi)")
    beep(4, 0.2)

# =========================
# HISTORIALES
# =========================
# Validación (voltajes)
hist_v_mq2, hist_v_mq3, hist_v_mq135 = [], [], []

# Suavizado (ratios)
hist_r_mq2, hist_r_mq3, hist_r_mq135 = [], [], []
def suavizar(valor, historial):
    historial.append(valor)
    if len(historial) > 20:
        historial.pop(0)
    return sum(historial) / len(historial)

# =========================
# WiFi
# =========================

def estado_wifi(wlan):
    if not wlan.active():
        return "OFF"
    if wlan.isconnected():
        return "OK"
    return "ERR"

# =========================
# LOOP PRINCIPAL
# =========================
while True:
    # =====================
    # SIN ADS
    # =====================
    if not ads:
        oled.fill(0)
        oled.text("SIN ADS1115", 0, 10)
        oled.text(ip, 0, 30)
        oled.show()
        time.sleep(2)
        continue

    # =====================
    # LECTURAS
    # =====================
    v1 = promedio_lectura(ads, 0)
    v2 = promedio_lectura(ads, 1)
    v3 = promedio_lectura(ads, 2)

    # =====================
    # HISTORIAL
    # =====================
    hist_v_mq2.append(v1)
    hist_v_mq3.append(v2)
    hist_v_mq135.append(v3)

    if len(hist_v_mq2) > 10:
        hist_v_mq2.pop(0)
        hist_v_mq3.pop(0)
        hist_v_mq135.pop(0)

    # =====================
    # VALIDACIÓN
    # =====================
    e1 = validar_sensor(v1, hist_v_mq2)
    e2 = validar_sensor(v2, hist_v_mq3)
    e3 = validar_sensor(v3, hist_v_mq135)

    if e1 in ["DESCONECTADO", "ERROR", "SIN ADC"] or e2 in ["DESCONECTADO", "ERROR", "SIN ADC"] or e3 in ["DESCONECTADO", "ERROR", "SIN ADC"]:
        oled.fill(0)
        oled.text("ERROR SENSOR", 0, 0)
        oled.text("MQ2:{}".format(e1), 0, 10)
        oled.text("MQ3:{}".format(e2), 0, 20)
        oled.text("MQ135:{}".format(e3), 0, 30)
        oled.show()
        time.sleep(2)
        continue

    # =====================
    # RS
    # =====================
    r1 = calcular_rs(v1, RL, VCC)
    r2 = calcular_rs(v2, RL, VCC)
    r3 = calcular_rs(v3, RL, VCC)

    if not Ro:
        oled.fill(0)
        oled.text("ERROR Ro", 0, 20)
        oled.show()
        time.sleep(2)
        continue

    ratio1 = r1 / max(Ro["MQ2"], 0.1)
    ratio2 = r2 / max(Ro["MQ3"], 0.1)
    ratio3 = r3 / max(Ro["MQ135"], 0.1)
    
    # =====================
    # SUAVIZADO
    # =====================
    mq2_s = suavizar(ratio1, hist_r_mq2)
    mq3_s = suavizar(ratio2, hist_r_mq3)
    mq135_s = suavizar(ratio3, hist_r_mq135)

    ppm2 = ratio_a_ppm(ratio1, MQ2_CURVA)
    ppm3 = ratio_a_ppm(ratio2, MQ3_CURVA)
    ppm135 = ratio_a_ppm(ratio3, MQ135_CURVA)

    # =====================
    # ESTADO
    # =====================
    alertas = []

    if mq2_s < 3:
        alertas.append("MQ2")

    if mq3_s < 10:
        alertas.append("MQ3")

    if mq135_s < 2:
        alertas.append("MQ135")

    if len(alertas) == 0:
        estado = "NORMAL"

    elif len(alertas) == 1:
        estado = "ALR " + alertas[0]

    else:
        estado = "MULTIGAS"
        
    # =========================
    # ALARMA SONORA
    # =========================
    alarma_estado(estado)

    # =====================
    # LEER DHT11
    # =====================
    temp, hum = leer_clima()
    if temp is None:
        temp = 25

    if hum is None:
        hum = 50


    data_global.update({
        "mq2": mq2_s,
        "ppm2": int(ppm2),
        "mq3": mq3_s,
        "ppm3": int(ppm3),
        "mq135": mq135_s,
        "ppm135": int(ppm135),
        "temp": temp,
        "hum": hum,
        "estado": estado
    })

    # =====================
    # OLED SIEMPRE FUNCIONA
    # =====================
    wifi_estado = estado_wifi(wlan)
    mostrar_datos(
        oled,
        mq2_s, mq3_s, mq135_s,
        estado,
        wifi_estado,
        ppm2, ppm3, ppm135, ip,
        temp, hum
    )
    
    print("----------------")
    print("MQ2 ratio:", mq2_s)
    print("MQ3 ratio:", mq3_s)
    print("MQ135 ratio:", mq135_s)

    print("PPM2:", ppm2)
    print("PPM3:", ppm3)
    print("PPM135:", ppm135)

    print("TEMP:", temp)
    print("HUM:", hum)

    print("Estado:", estado)
    
    time.sleep(2)