#############################################
#Desarrollado por: Jeremías Emmanuel Miranda#
#Modelo para calcular la curva de PPM       #
#############################################

import math

MQ2_CURVA = {"m": -0.47, "b": 1.38}
MQ3_CURVA = {"m": -0.36, "b": 1.65}
#MQ135_CURVA = {"m": -0.42, "b": 1.92}
MQ135_CURVA = {"m": -0.35, "b": 1.6}

def ratio_a_ppm(ratio, curva):

    # Evitar valores inválidos
    ratio = max(0.1, min(ratio, 50))

    try:
        ppm = 10 ** (
            (math.log10(ratio) - curva["b"])
            / curva["m"]
        )

        # Limitar ppm absurdos
        ppm = max(0, min(ppm, 10000))

        return ppm

    except Exception as e:
        print("PPM ERROR:", e)
        return 0