#############################################
#Desarrollado por: Jeremías Emmanuel Miranda#
#Calibración de los sensores                #
#############################################

from config import FACTORES, RL, VCC
import time

def calcular_rs(vout):
    if vout is None or vout == 0:
        return 0

    return RL * (VCC - vout) / vout


def warmup(oled, segundos=30):

    for i in range(segundos, 0, -1):

        oled.fill(0)
        oled.text("MQ WARMUP", 0, 10)
        oled.text("{} segundos".format(i), 0, 30)
        oled.show()

        time.sleep(1)


def calibrar(oled, ads, promedio_lectura):

    # =========================
    # WARMUP
    # =========================
    warmup(oled, 180)

    Ro = {}

    sensores = [
        ("MQ2", 0),
        ("MQ3", 1),
        ("MQ135", 2)
    ]

    for nombre, canal in sensores:

        oled.fill(0)
        oled.text("Calibrando:", 0, 0)
        oled.text(nombre, 0, 15)
        oled.show()

        rs_total = 0
        muestras = 30

        for _ in range(muestras):

            v = promedio_lectura(ads, canal)

            if v is None:
                continue

            rs = calcular_rs(v)

            rs_total += rs

            time.sleep_ms(200)

        rs_prom = rs_total / muestras

        ro = rs_prom / FACTORES[nombre]

        Ro[nombre] = ro

        print(nombre, "Ro =", ro)

    oled.fill(0)
    oled.text("Calibracion OK", 0, 20)
    oled.show()

    time.sleep(2)

    return Ro