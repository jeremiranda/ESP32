#############################################
#Desarrollado por: Jeremías Emmanuel Miranda#
#Configuraciones de los sensores y ADS1115  #
#############################################

from machine import I2C
import time

class ADS1115:
    def __init__(self, i2c, addr=0x48):
        self.i2c = i2c
        self.addr = addr

    def read_voltage(self, channel):
        config = 0xC383 | (channel << 12)
        self.i2c.writeto_mem(self.addr, 0x01, config.to_bytes(2, 'big'))
        time.sleep_ms(10)
        data = self.i2c.readfrom_mem(self.addr, 0x00, 2)
        raw = int.from_bytes(data, 'big')
        if raw > 32767:
            raw -= 65536
        return raw * 4.096 / 32767


def promedio_lectura(ads, canal):
    suma = 0
    for _ in range(10):
        suma += ads.read_voltage(canal)
        time.sleep_ms(50)
    return suma / 10


def calcular_rs(vout, RL, VCC):
    if vout <= 0:
        return 0
    return RL * (VCC - vout) / vout