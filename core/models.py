from django.db import models
from django.contrib.auth.models import Group
from django.contrib.admin.models import LogEntry
from core.managers import ModuloManager, FuncionalidadManager, ItemManager
from .validators import validate_url, validate_url_name

# Create your models here.
from django.db import models

# Create your models here.


def get_limit_choices_to():
    #return {'catalogo': Catalogo.objects.get(codigo="EST").id} Esto estaba funcionando
    return {'catalogo': Catalogo.objects.filter(codigo="EST")}


class Catalogo(models.Model):

    ESTADOS_GENERALES = (
        ('A', 'Activo'),
        ('I', 'Inactivo')
    )

    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADOS_GENERALES)
    padre = models.ForeignKey('self', blank=True, null=True)
    editable = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Catalogos'

    def __unicode__(self):
        return self.nombre


class Item(models.Model):
    ESTADOS_GENERALES = (
        ('A', 'Activo'),
        ('I', 'Inactivo')
    )
    catalogo = models.ForeignKey(Catalogo)
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    valor = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.TextField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADOS_GENERALES)
    padre = models.ForeignKey('self',related_name='item_padre', blank=True, null=True)
    principal = models.BooleanField(default=False)
    objects = ItemManager()

    class Meta:
        unique_together = ('catalogo', 'codigo',)
        verbose_name_plural = 'Items'

    def __unicode__(self):
        return self.nombre


class Funcionalidad(models.Model):
    ESTADOS_GENERALES = (
        ('A', 'Activo'),
        ('I', 'Inactivo')
    )
    nombre = models.CharField(max_length=50)
    url = models.CharField(max_length=50, validators=[validate_url_name])  # tiene que ser el mismo nombre de la url
    codigo = models.CharField(max_length=20, unique=True)
    modulo = models.ForeignKey('Modulo')
    grupos = models.ManyToManyField(Group)
    #estado = models.BooleanField(default=False)
    estado = models.CharField(max_length=1, choices=ESTADOS_GENERALES)
    descripcion = models.TextField(max_length=200, null=True, blank=True)
    orden = models.PositiveIntegerField(null=True, blank=True)
    icono = models.CharField(max_length=20, null=True, blank=True)
    objects = FuncionalidadManager()

    class Meta:
        verbose_name_plural = u'Funcionalidades'

    def save(self, *args, **kwargs):
        if self.orden:
            if Funcionalidad.objects.filter(orden=self.orden, modulo=self.modulo):
                funcionalidad = Funcionalidad.objects.get(orden=self.orden,modulo=self.modulo)
                funcionalidad.orden = self.orden+1
                funcionalidad.save()
                print 'algo'
                self.save(*args, **kwargs)
        super(Funcionalidad, self).save(*args, **kwargs)

    def actualizar_orden(self):
        if Funcionalidad.objects.filter(orden=self.orden):
            Funcionalidad.objects.get(orden=1).update(orden=self.orden+1)

    def __unicode__(self):
        return u'%s.- %s' % (self.modulo.id, self.nombre)


class Parametro(models.Model):
    ESTADOS_GENERALES = (
        ('A', 'Activo'),
        ('I', 'Inactivo')
    )
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADOS_GENERALES)
    tipo_parametro = models.ForeignKey(Item, related_name='tipo_parametro', blank=True, null=True)

    class Meta:
        verbose_name_plural = u'Parametros'

    def __unicode__(self):
        return self.nombre


class Modulo(models.Model):
    ESTADOS_GENERALES = (
        ('A', 'Activo'),
        ('I', 'Inactivo')
    )
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADOS_GENERALES)
    orden = models.PositiveIntegerField(null=True, blank=True);
    objects = ModuloManager()

    class Meta:
        verbose_name_plural = u'Modulos'

    def save(self, *args, **kwargs):
        if self.orden:
            if Modulo.objects.filter(orden=self.orden):
                modulo = Modulo.objects.get(orden=self.orden)
                modulo.orden = self.orden+1
                modulo.save()
                print 'algo'
                self.save(*args, **kwargs)
        super(Modulo, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.nombre

class LogDetail(models.Model):
    log = models.ForeignKey(LogEntry)
