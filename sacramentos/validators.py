#-*- coding:utf-8 -*-
from django.core.exceptions import ValidationError

def validate_cedula(cedula):
	if not cedula.isdigit():
		raise ValidationError('El número de cédula no debe contener letras')
		return cedula
	if len(cedula)!=10:
		raise ValidationError('El número de cédula debe ser de 10 dígitos')
		return cedula
	valores = [ int(cedula[x]) * (2 - x % 2) for x in range(9) ]
	suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
	if int(cedula[9]) != 10 - int(str(suma)[-1:]):
		raise ValidationError('El número de cédula no es válido')
		return cedula


