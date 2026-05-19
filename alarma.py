#############################################
#Desarrollado por: Jeremías Emmanuel Miranda#
#Activa el buzzer de alarma                 #
#############################################

from machine import Pin, PWM
import time

# GPIO del buzzer
buzzer = PWM(Pin(18))
buzzer.duty_u16(0)

# =========================================================
# TEST INICIO
# =========================================================
def startup_sound():
    beep(1, 0.10)
    time.sleep(0.1)
    beep(1, 0.05)

# =========================================================
# APAGAR
# =========================================================
def alarma_off():
    buzzer.duty_u16(0)

# =========================================================
# BEEP SIMPLE
# =========================================================
def beep(times=1, delay=0.15, freq=2000):
    for _ in range(times):
        buzzer.freq(freq)
        buzzer.duty_u16(30000)
        time.sleep(delay)
        buzzer.duty_u16(0)
        time.sleep(delay)


# =========================================================
# ALARMA ESCALONADA
# =========================================================
def alarma_estado(estado):

    # =====================
    # NORMAL
    # =====================
    if estado == "NORMAL":
        alarma_off()

    # =====================
    # ALERTA SIMPLE
    # =====================
    elif "ALERTA" in estado:

        # 2 beeps medios
        beep(2, 0.15)

    # =====================
    # MULTIGAS
    # =====================
    elif estado == "MULTIGAS":

        # 5 beeps rápidos
        beep(5, 0.08)

    # =====================
    # FALLBACK
    # =====================
    else:
        beep(1, 0.3)