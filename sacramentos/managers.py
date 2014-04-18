from django.db import models
# from sacramentos.models import *

class LibroManager(models.Manager):
	#def get_query_set(self):
	#	return super(LibroManager, self).get_query_set().filter(parroquia='1')
	
	#def libros_por_parroquia(self):
	#  	return self.models.objects.filter(parroquia=self)

	def libro(self):
		return self.model.objects.filter(tipo_libro='Bautismo',estado='Abierto',
			parroquia=self.parroquia)

	#def get_by_natural_key(self,numero_libro,tipo_libro):
	 #	return self.get(numero_libro=numero_libro, tipo_libro=tipo_libro)



class ParroquiaManager(models.Manager):
	pass

class PersonaManager(models.Manager):

	def padre(self):
		return self.model.objects.filter(sexo='m').exclude(user__groups__name='Sacerdote')

	def madre(self):
		return self.model.objects.filter(sexo='f')

	def feligres(self):
		return self.model.objects.all().exclude(user__groups__name='Sacerdote')
	
	def administrador(self):
		return self.model.objects.filter(user__groups__name='Administrador')

	def male(self):
		return self.model.objects.filter(sexo='m')

	def female(self):
		return self.model.objects.filter(sexo='f')

	def todos(self):
		return self.model.objects.all()

	def sacerdote(self):
		return self.model.objects.filter(user__groups__name='Sacerdote', profesion='Sacerdote')

	def parroco(self, parroquia):
		return self.model.objects.filter(user__groups__name='Sacerdote', profesion='Sacerdote', 
			asignacionparroquia__parroquia = parroquia)

	# def feligres(self):
	# 	return self.model.objects.filter(user__groups__name='Feligres', profesion='-Sacerdote')

	def username_disponible(self, username):
		try:
			persona = self.model.objects.get(user__username=username)
			return persona.user.username
		except:
			return True

class BautismoManager(models.Manager):
	# def libro_activo(self):
	# 	return self.model.objects.filter(libro__tipo_libro='Bautismo')
	pass

class NotaMarginalManager(models.Manager):
	
	pass


class AsignacionParroquiaManager(models.Manager):
	pass
