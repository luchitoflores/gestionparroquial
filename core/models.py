from django.db import models
from django.contrib.auth.models import Group
from core.managers import ModuloManager, FuncionalidadManager, ItemManager

# Create your models here.
from django.db import models

# Create your models here.

def get_limit_choices_to():
    return {'catalogo': Catalogo.objects.get(codigo="EST").id}

class Catalogo(models.Model):
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=200, null=True, blank=True)
    estado = models.ForeignKey('Item', related_name='estado_item', limit_choices_to=get_limit_choices_to)
    padre = models.ForeignKey('self', blank=True, null=True)
    editable = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Catalogos'

    def __unicode__(self):
        return self.nombre

class Item(models.Model):
    catalogo = models.ForeignKey(Catalogo)
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=200, null=True, blank=True)
    estado = models.ForeignKey('self')
    padre = models.ForeignKey('self',related_name='item_padre', blank=True, null=True)
    principal = models.BooleanField(default=False)
    objects = ItemManager()

    class Meta:
        unique_together = ('catalogo', 'codigo',)
        verbose_name_plural = 'Items'



    def __unicode__(self):
        return self.nombre

class Funcion(models.Model):
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=200, null=True, blank=True)
    estado = models.BooleanField(default=False)
    eliminada = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = u'Funciones'

    def __unicode__(self):
        return self.nombre

class Funcionalidad(models.Model):
    nombre = models.CharField(max_length=50)
    url = models.CharField(max_length=50)  # tiene que ser el mismo nombre de la url
    modulo = models.ForeignKey('Modulo')
    grupos = models.ManyToManyField(Group)
    estado = models.BooleanField(default=False)
    descripcion = models.TextField(max_length=200, null=True, blank=True)
    orden = models.PositiveIntegerField(null=True, blank=True)
    icono = models.CharField(max_length=20, null=True, blank=True)
    objects = FuncionalidadManager()

    class Meta:
        verbose_name_plural = u'Funcionalidades'

    def __unicode__(self):
        return u'%s.- %s' % (self.modulo.id, self.nombre)


class Parametro(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=200, null=True, blank=True)
    estado = models.ForeignKey(Item, limit_choices_to=get_limit_choices_to)
    tipo_parametro =  models.ForeignKey(Item, related_name='tipo_parametro')


    class Meta:
        verbose_name_plural = u'Parametros'

    def __unicode__(self):
        return self.nombre


class Modulo(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=200, null=True, blank=True)
    estado = models.ForeignKey(Item, limit_choices_to=get_limit_choices_to)
    orden = models.PositiveIntegerField(null=True, blank=True);
    objects = ModuloManager()

    class Meta:
        verbose_name_plural = u'Modulos'

    def __unicode__(self):
        return self.nombre
