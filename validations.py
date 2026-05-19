#############################################
#Desarrollado por: Jeremías Emmanuel Miranda#
#Validaciones de los sensores               #
#############################################

def validar_sensor(vout, historial):

    if vout is None:
        return "SIN ADC"

    if vout < 0.05:
        return "DESCONECTADO"

    if vout > 4.9:
        return "ERROR"

    if len(historial) >= 5:
        variacion = max(historial) - min(historial)

        if variacion < 0.02:
            return "ESTABLE"

        if variacion > 0.5:
            return "RUIDO"

    return "OK"