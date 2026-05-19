#############################################
#Desarrollado por: Jeremías Emmanuel Miranda#
#Configuraciones de la pantalla             #
#############################################

import ssd1306

def init_display(i2c):
    return ssd1306.SSD1306_I2C(128, 64, i2c)


def mostrar_error(oled, estados):
    oled.fill(0)
    oled.text("ERROR SENSOR", 0, 0)
    oled.text("MQ2:" + estados[0], 0, 10)
    oled.text("MQ3:" + estados[1], 0, 20)
    oled.text("MQ135:" + estados[2], 0, 30)
    oled.show()

def dibujar_wifi(oled, x, y, estado):
    # limpiar zona
    for i in range(20):
        for j in range(10):
            oled.pixel(x+i, y+j, 0)

    niveles = {
        "OK": 4,
        "ERR": 1,
        "OFF": 0
    }

    nivel = niveles.get(estado, 0)

    for i in range(nivel):
        altura = (i + 1) * 2
        for h in range(altura):
            oled.pixel(x + i*4, y + 8 - h, 1)
            oled.pixel(x + i*4 + 1, y + 8 - h, 1)

def mostrar_datos(oled, mq2, mq3, mq135, estado, wifi_estado,
                  ppm2, ppm3, ppm135, ip, temp, hum):

    oled.fill(0)

    oled.text("MQ2:{:.1f}".format(mq2), 0, 0)
    oled.text("{:>4}ppm".format(int(ppm2)), 72, 0)

    oled.text("MQ3:{:.1f}".format(mq3), 0, 10)
    oled.text("{:>4}ppm".format(int(ppm3)), 72, 10)

    oled.text("M135:{:.1f}".format(mq135), 0, 20)
    oled.text("{:>4}ppm".format(int(ppm135)), 72, 20)

    oled.text("ST:{}".format(estado), 0, 32)

    oled.text(ip, 0, 42)

    oled.text("{}C".format(temp), 0, 54)
    oled.text("{}%".format(hum), 44, 54)

    dibujar_wifi(oled, 96, 54, wifi_estado)

    oled.show()