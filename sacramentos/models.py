# -*- coding:utf-8 -*-
import re
import unicodedata

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import ForeignKey
from django.utils import six


# Para los logs
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType

from core.models import Item, Direccion
from sacramentos.managers import PersonaManager, LibroManager, PeriodoAsignacionManager


def user_new_unicode(self):
    return self.username if self.get_full_name() == '' else self.get_full_name()


def permissions_new_unicode(self):
    nombre_clase = six.text_type(self.content_type)
    nombre_permiso = six.text_type(self.name)
    if 'Can delete' in nombre_permiso:
        nombre_permiso = nombre_permiso.replace('Can delete', 'Puede eliminar')
    elif 'Can add' in nombre_permiso:
        nombre_permiso = nombre_permiso.replace('Can add', 'Puede crear')
    elif 'Can change' in nombre_permiso:
        nombre_permiso = nombre_permiso.replace('Can change', 'Puede modificar')

    return u'%s - %s' % ( nombre_clase.title(), nombre_permiso)


User.__unicode__ = user_new_unicode
Permission.__unicode__ = permissions_new_unicode


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    es_activo = models.BooleanField('Está activo?', default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        print args
        print kwargs
        LogEntry.objects.log_action(
            user_id=1,
            content_type_id=ContentType.objects.get_for_model(self).pk,
            object_id=self.id,
            object_repr=unicode(self),
            action_flag=CHANGE if self.id else ADDITION,
            change_message='Se update exitosamente prueba' if self.id else 'Se create exitosamente prueba')
        super(TimeStampedModel, self).save(*args, **kwargs)


class PerfilUsuario(TimeStampedModel):
    # p.f00_size
    # p.get_foo_size_display()
    SEXO_CHOICES = (
        ('', '-- Seleccione --'),
        ('m', 'Masculino'),
        ('f', 'Femenino')
    )
    # se lo puede llamar con related_name usuario o con el método get_profile
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='usuario', null=True, blank=True)
    nombres_completos = models.CharField(max_length=100)
    dni = models.CharField('Cédula/Pasaporte', max_length=20, null=True, blank=True,
                           help_text='Ingrese un numero de cedula ej:1101980561')
    nacionalidad = models.ForeignKey(Item, related_name='persona', help_text='Escoja la nacionalidad. Ej: Ecuador')
    padre = models.ForeignKey('self', related_name='+', null=True, blank=True,
                              help_text='Presione buscar, si no está en la lista, presione crear')
    madre = models.ForeignKey('self', related_name='+', null=True, blank=True,
                              help_text='Presione buscar, si no está en la lista, presione crear')
    fecha_nacimiento = models.DateField(null=True, blank=True,
                                        help_text='Ingrese la fecha de nacimiento Ej: dd/mm/yyyy')
    lugar_nacimiento = models.CharField(max_length=25, null=True, blank=True,
                                        help_text='Ingrese el lugar de Nacimiento. Ej: Amaluza')
    sexo = models.ForeignKey(Item, related_name='genero', help_text='Elija el sexo de la persona. Ej: Masculino')
    estado_civil = models.ForeignKey(Item, related_name='estado_civil', help_text='Elija el estado civil. Ej: Soltero/a')
    profesion = models.CharField(max_length=40, null=True, blank=True, help_text='Ingrese la profesión de la persona')
    celular = models.CharField(max_length=10, blank=True, null=True,
                               help_text='Ingrese su número celular. Ej: 0986522754')
    parroquias = models.ManyToManyField('Parroquia', null=True, blank=True, through='AsignacionParroquia')

    objects = PersonaManager()

    class Meta:
        verbose_name = u'Perfil'
        verbose_name_plural = u'Perfiles'
        get_latest_by = 'created'
        ordering = ['user__last_name', 'user__first_name']
        permissions = (
            ('add_secretaria', 'Puede crear secretarias'),
            ('change_secretaria', 'Puede actualizar secretarias'),
            ('delete_secretaria', 'Puede eliminar secretarias'),

            ('add_feligres', 'Puede crear feligreses'),
            ('change_feligres', 'Puede actualizar feligreses'),
            ('delete_feligres', 'Puede eliminar feligreses'),

            ('add_sacerdote', 'Puede crear sacerdotes'),
            ('change_sacerdote', 'Puede actualizar sacerdotes'),
            ('delete_sacerdote', 'Puede eliminar sacerdotes'),

            ('add_administrador', 'Puede crear administradores'),
            ('change_administrador', 'Puede actualizar administradores'),
            ('delete_administrador', 'Puede eliminar administradores'),
        )

    def __unicode__(self):
        if self.user.first_name is None and self.user.last_name is None:
            return self.user.username
        else:
            return '%s' % (self.user.get_full_name())

    def get_absolute_url_sacerdote(self):
        return u'/sacerdote/%i' % self.id

    def get_absolute_url_administrador(self):
        return u'/administrador/%i' % self.id

    def save(self, *args, **kwargs):
        nombres = ''.join(
            (c for c in unicodedata.normalize('NFD', unicode(self.user.first_name)) if unicodedata.category(c) != 'Mn'))
        apellidos = ''.join(
            (c for c in unicodedata.normalize('NFD', unicode(self.user.last_name)) if unicodedata.category(c) != 'Mn'))
        self.user.first_name = nombres.strip()
        self.user.last_name = apellidos.strip()
        self.nombres_completos = u'%s %s' % (self.user.first_name, self.user.last_name)
        if not self.id:
            self.user.is_active = False
        super(PerfilUsuario, self).save(*args, **kwargs)

    def crear_username(self, nombres, apellidos):
        nombres = ''.join(
            (c for c in unicodedata.normalize('NFD', unicode(nombres)) if unicodedata.category(c) != 'Mn'))
        apellidos = ''.join(
            (c for c in unicodedata.normalize('NFD', unicode(apellidos)) if unicodedata.category(c) != 'Mn'))
        nombres = nombres.lower().split()
        apellidos = apellidos.lower().split()
        username = u'%s%s' % (nombres[0][0], apellidos[0])
        user_name = PerfilUsuario.objects.username_disponible(username)

        if user_name:
            return username
        else:
            personas = PerfilUsuario.objects.filter(user__username__startswith=username).latest('user__date_joined')
            ultimo_username = personas.user.username
            digitos = ''
            for d in ultimo_username:
                if re.match('[0-9]+', d):
                    digitos += d

            if digitos == '':
                username += str(1)
            else:
                digitos = int(digitos) + 1
                username += str(digitos)
            return username

    def es_casado(self):
        if self.estado_civil == 'c':
            return True
        else:
            return False

    def es_mujer(self):
        if self.sexo == Item.objects.femenino():
            return True
        else:
            return False

    def es_hombre(self):
        if self.sexo == Item.objects.masculino():
            return True
        else:
            return False

    def es_bautizado(self):
        try:
            self.bautismo
            return True
        except ObjectDoesNotExist:
            return False

    def tiene_primera_comunion(self):
        try:
            self.primera_comunion
            return True
        except ObjectDoesNotExist:
            return False

    def es_confirmado(self):
        try:
            self.confirmacion
        except ObjectDoesNotExist:
            return False
        else:
            return True

    def tiene_matrimonios(self):
        if self.matrimonios_hombre.all() or self.matrimonios_mujer.all():
            return True
        else:
            return False


# class Feligres(TimeStampedModel):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='feligres', null=True, blank=True)
#     padre = models.CharField(max_length=100, blank=True, null=True)
#     madre = models.CharField(max_length=100, blank=True, null=True)
#     nombres_completos = models.CharField(max_length=100)
#     dni = models.CharField('Cédula/Pasaporte', max_length=20, null=True, blank=True,
#                            help_text='Ingrese un numero de cedula ej:1101980561')
#     nacionalidad = models.ForeignKey(Item, help_text='Escoja la nacionalidad. Ej: Ecuador', related_name='nacionalidad_feligres')
#     fecha_nacimiento = models.DateField(null=True, blank=True,
#                                         help_text='Ingrese la fecha de nacimiento Ej: dd/mm/yyyy')
#     lugar_nacimiento = models.CharField(max_length=25, null=True, blank=True,
#                                         help_text='Ingrese el lugar de Nacimiento. Ej: Amaluza')
#     sexo = models.ForeignKey(Item, help_text='Elija el sexo de la persona. Ej: Masculino', related_name='sexo_feligres')
#     estado_civil = models.ForeignKey(Item, help_text='Elija el estado civil. Ej: Soltero/a', related_name='estado_civil_feligres')


class Parroquia(TimeStampedModel):
    nombre = models.CharField('Nombre de Parroquia *', max_length=50,
                              help_text='Ingrese el nombre de la parroquia Ej: El Cisne')
    direccion = models.ForeignKey(Direccion, related_name='direccion_parroquia')

    class Meta:
        verbose_name = u'Parroquia'
        verbose_name_plural = u'Parroquias'
        get_latest_by = 'created'
        ordering = ['nombre']

    def __unicode__(self):
        return u'%s' % (self.nombre)

    def get_absolute_url(self):
        return '/parroquia/%s' % (self.id)


class Iglesia(TimeStampedModel):
    nombre = models.CharField(max_length=100)
    parroquia = models.ForeignKey(Parroquia, related_name='iglesias')
    principal = models.BooleanField('Es la Iglesia Matriz?', default=False)

    class Meta:
        verbose_name = u'Iglesia'
        verbose_name_plural = u'Iglesias'
        get_latest_by = 'created'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('iglesia_update', kwargs={'pk': str(self.id)})


class Libro(TimeStampedModel):
    TIPO_LIBRO_CHOICES = (
        ('', '-- Seleccione --'),
        ('bautismo', 'Bautismo'),
        ('eucaristia', 'Primera Comunión'),
        ('confirmacion', 'Confirmación'),
        ('matrimonio', 'Matrimonio'),
    )

    nombre = models.CharField(u'Nombre *', max_length='50', help_text='Nombre del Libro', null=True, blank=True)
    numero_libro = models.PositiveIntegerField()
    tipo_libro = models.CharField(u'Tipo de Libro *', max_length=200, choices=TIPO_LIBRO_CHOICES,
                                  help_text='Seleccione un tipo de libro Ej: Bautismo',
                                  default=TIPO_LIBRO_CHOICES[0][0])
    fecha_apertura = models.DateField(u'Fecha apertura *', help_text='Ingrese una fecha Ej:22/07/2010')
    fecha_cierre = models.DateField(null=True, blank=True, help_text='Ingrese una fecha Ej:22/07/2010')
    principal = models.BooleanField(u'Es principal', default=False)
    parroquia = models.ForeignKey('Parroquia', related_name='libros', help_text='Seleccione una parroquia')
    primera_pagina = models.PositiveIntegerField(u'Primera página *')
    primera_acta = models.PositiveIntegerField(u'Primera acta *')

    objects = LibroManager()

    class Meta:
        verbose_name = u'Libro'
        verbose_name_plural = u'Libros'
        get_latest_by = 'created'
        ordering = ['principal', 'nombre', 'numero_libro', 'tipo_libro', '-fecha_apertura']

    def __unicode__(self):
        return '%s.- %s %s' % (self.numero_libro, self.get_tipo_libro_display(), self.fecha_apertura.year)

    def ultima_pagina(self):
        return self.sacramento_libro.latest('created')
        # return self.paginas.last()

    def ultima_pagina_par(self):
        return self.paginas.last() % 2 == 0

    def esta_vacio(self):
        if self.sacramento_libro.all():
            return False
        else:
            return True


class Sacramento(TimeStampedModel):
    TIPO_SACRAMENTO_CHOICES = (
        ('Bautismo', 'Bautismo'),
        ('Eucaristia', 'Eucaristia'),
        ('Confirmacion', 'Confirmacion'),
        ('Matrimonio', 'Matrimonio')
    )

    numero_acta = models.PositiveIntegerField(help_text='Ingrese el numero de acta ej:3,78')
    pagina = models.PositiveIntegerField(help_text='Numero de pagina ej:1,3')
    fecha_sacramento = models.DateField(help_text='Elija una fecha ej:dd/mm/aaaa')
    celebrante = models.ForeignKey(PerfilUsuario, verbose_name='Celebrante *', related_name='%(class)s_sacerdote',
                                   help_text='Escoja el celebrante. Ej: Segundo Pardo Rojas')
    lugar_sacramento = models.CharField(u'Lugar del Sacramento *', max_length=30,
                                        help_text='Ingrese el lugar del sacramento Ej: Loja,San Pedro')
    padrino = models.CharField(max_length=50, null=True, blank=True,
                               help_text='Ingrese el nombre de padrino ej: Jose Rivera')
    madrina = models.CharField(max_length=50, null=True, blank=True,
                               help_text='Ingrese el nombre de madrina ej: Luisa Mera')
    iglesia = models.ForeignKey('Iglesia', verbose_name=u'Iglesia *',
                                help_text='Ingrese el nombre de la iglesia Ej: La Catedral')
    libro = models.ForeignKey(Libro, verbose_name='Libro *', related_name='%(class)s_libro',
                              help_text='Seleccione un libro')
    parroquia = models.ForeignKey('Parroquia', related_name='%(class)s_parroquia')
    #padrinos = models.ManyToOneRel('Padrino', related_name='padrinos')

    def ultimo_libro(self, libro):
        return self.__class__.objects.filter(libro=libro).latest('created')

    # Aqui debería manjerase la página como clase
    # con atributos como numero y total de actas que contiene. 
    # def pagina_esta_llena(self, libro):
    # libro.actas_por_pagina
    # pass

    def asignar_numero_acta(self, libro):
        sacramento = self.__class__.objects.filter(libro=libro).latest('created')
        self.numero_acta = sacramento.numero_acta + 1
        if self.numero_acta % 2 == 0:
            self.pagina = sacramento.pagina
        else:
            self.pagina = sacramento.pagina + 1


class Bautismo(Sacramento):
    bautizado = models.OneToOneField(PerfilUsuario, related_name='bautismo',
                                     help_text='Seleccione un feligres')
    abuelo_paterno = models.CharField(max_length=70, null=True, blank=True,
                                      help_text='Nombre de abuelo paterno ej: Jose Rivera')
    abuela_paterna = models.CharField(max_length=70, null=True, blank=True,
                                      help_text='Nombre de abuela paterna ej: Mary Gonzalez')
    abuelo_materno = models.CharField(max_length=70, null=True, blank=True,
                                      help_text='Nombre de abuelo materno ej: Jose Gonzalez')
    abuela_materna = models.CharField(max_length=70, null=True, blank=True,
                                      help_text='Nombre de abuela materna ej: Gloria Correa')
    vecinos_paternos = models.CharField(u'Residencia Abuelos Paternos', max_length=70, null=True, blank=True,
                                        help_text='Residencia de abuelos paternos ej: Catacocha')
    vecinos_maternos = models.CharField(u'Residencia Abuelos Maternos', max_length=70, null=True, blank=True,
                                        help_text='Residencia de abuelos maternos ej: Malacatos')

    class Meta:
        verbose_name = u'Bautismo'
        verbose_name_plural = u'Bautismos'
        get_latest_by = 'created'
        ordering = ['bautizado__user__last_name', 'bautizado__user__first_name', 'fecha_sacramento', 'lugar_sacramento']

    def __unicode__(self):
        return '%s %s' % (self.bautizado.user.first_name, self.bautizado.user.last_name)


class Eucaristia(Sacramento):
    feligres = models.OneToOneField(PerfilUsuario, related_name='primera_comunion',
                                    help_text='Seleccione un feligres')

    class Meta:
        verbose_name = u'Primera Comunión'
        verbose_name_plural = u'Primera Comunión'
        get_latest_by = 'created'
        ordering = ['feligres__user__last_name', 'feligres__user__first_name', 'fecha_sacramento', 'lugar_sacramento']

    def __unicode__(self):
        return '%s %s' % (self.feligres.user.first_name, self.feligres.user.last_name)


class Confirmacion(Sacramento):
    confirmado = models.OneToOneField(PerfilUsuario, related_name='confirmacion', help_text='Seleccione un feligres')

    def __unicode__(self):
        return '%s %s' % (self.confirmado.user.first_name, self.confirmado.user.last_name)


class Matrimonio(Sacramento):
    TIPO_MATRIMONIO_CHOICES = (
        ("", "-- Seleccione --"),
        ('Catolico', 'Catolico'),
        ('Mixto', 'Mixto'),
    )

    novio = models.ForeignKey(PerfilUsuario, related_name='matrimonios_hombre',
                              help_text='Seleccione un novio')
    novia = models.ForeignKey(PerfilUsuario, related_name='matrimonios_mujer',
                              help_text='Seleccione una novia')
    testigo_novio = models.CharField(u'Testigo novio *', max_length=70,
                                     help_text='Nombre de testigo ej: Pablo Robles')
    testigo_novia = models.CharField(u'Testigo novia *', max_length=70,
                                     help_text='Nombre de testiga ej:Fernanda Pincay')
    vigente = models.BooleanField(default=None)
    tipo_matrimonio = models.CharField(u'Tipo Matrimonio *', max_length=100, choices=TIPO_MATRIMONIO_CHOICES,
                                       default=TIPO_MATRIMONIO_CHOICES[1][1],
                                       help_text='Elija tipo de matrimonio Ej: Catolico o Mixto')

    class Meta:
        verbose_name = u'Matrimonio'
        verbose_name_plural = u'Matrimonios'
        get_latest_by = 'created'
        ordering = ['-vigente', 'novio__user__last_name', 'novio__user__first_name', 'novia__user__last_name',
                    'novia__user__first_name', 'fecha_sacramento', 'lugar_sacramento']

    def __unicode__(self):
        return u'%s - %s' % (self.novio.user.last_name, self.novia.user.last_name )


class NotaMarginal(TimeStampedModel):
    fecha = models.DateField(help_text='Ingrese una fecha Ej: 16/09/2013')
    descripcion = models.TextField('Descripción *', max_length=200,
                                   help_text='Ingrese una descripcion ej: Di copia para matrimonio')
    bautismo = models.ForeignKey('Bautismo', related_name='bautismo', null=True, blank=True)
    matrimonio = models.ForeignKey('Matrimonio', related_name='matrimonio', null=True, blank=True)

    class Meta:
        verbose_name = u'Nota Marginal'
        verbose_name_plural = u'Notas Marginales'
        get_latest_by = 'created'
        ordering = ['-fecha']


    def __unicode__(self):
        return self.descripcion


class Intencion(TimeStampedModel):
    intencion = models.TextField(max_length=500,
                                 help_text='Ingrese la intención. Ej: Aniversario de fallecimiento')
    fecha = models.DateField(help_text=
                             'Ingrese la fecha de la intención Ej: dd/mm/yyyy')
    hora = models.TimeField(help_text='Ingrese la hora de celebración de la intención Ej: 17:00')
    oferente = models.CharField(max_length=70,
                                help_text='Ingrese quien ofrece la intención. Ej: La Flia Flores')
    ofrenda = models.DecimalField(decimal_places=2, max_digits=7,
                                  help_text='Ingrese el valor de la ofrenda por la intención. Ej: 5')
    parroquia = models.ForeignKey('Parroquia')
    #tipo_intencion = models.ForeignKey(Item, related_name='tipo_intencion', help_text='Elija el tipo de intencion')
    individual = models.BooleanField('Es unica?', help_text='Elija el tipo de intencion', default=None)
    iglesia = models.ForeignKey('Iglesia', help_text='Escoja la iglesia en donde se celebrará la intención')

    class Meta:
        verbose_name = u'Intencion de Misa'
        verbose_name_plural = u'Intenciones de Misa'
        get_latest_by = 'created'
        ordering = ['iglesia__principal', '-fecha', '-hora', 'iglesia__nombre', 'oferente']

    def __unicode__(self):
        return self.oferente

    def get_absolute_url(self):
        return u'/intencion/%i' % self.id


class AsignacionParroquia(TimeStampedModel):
    persona = models.ForeignKey('PerfilUsuario', verbose_name=u'Sacerdote *')
    parroquia = models.ForeignKey('Parroquia')

    class Meta:
        verbose_name = u'Asignacion de Parroquia'
        verbose_name_plural = u'Asignaciones de Parroquias'
        get_latest_by = 'created'
        ordering = ['persona__user__last_name', 'parroquia__nombre']
        permissions = (
            ('add_asignarsecretaria', 'Puede asignar secretarias'),
            ('change_asignarsecretaria', 'Puede actualizar asignacion secretarias'),
            ('delete_asignarsecretaria', 'Puede eliminar asignacion secretarias'),
            ('add_asignarsacerdote', 'Puede asignar sacerdotes'),
            ('change_asignarsacerdote', 'Puede actualizar asignacion sacerdotes'),
            ('delete_asignarsacerdote', 'Puede eliminar asignacion sacerdotes'),
        )

    def __unicode__(self):
        return u'Párroco: %s - Parroquia: %s' % (self.persona.user.get_full_name(), self.parroquia.nombre)

    def get_absolute_url(self):
        return '/asignar/parroquia/parroco/%i' % self.id


class PeriodoAsignacionParroquia(TimeStampedModel):
    inicio = models.DateField(help_text='Ingrese la fecha de inicial de asignación Ej: dd/mm/aaaa')
    fin = models.DateField(null=True, blank=True, help_text='Ingrese la fecha final de asignación  Ej: dd/mm/aaaa')
    estado = models.BooleanField('Es administrador?',
                                 help_text='Marque la casilla activo para indicar que el usuario puede acceder al sistema',
                                 default=None)
    asignacion = models.ForeignKey('AsignacionParroquia', related_name='periodos')
    objects = PeriodoAsignacionManager()

    class Meta:
        verbose_name = u'Periodo'
        verbose_name_plural = u'Periodos'
        get_latest_by = 'created'
        ordering = ['estado', '-inicio']

    def __unicode__(self):
        return u'%s - %s : %s' % (self.asignacion.persona, self.asignacion.parroquia, self.estado)


class ParametrizaDiocesis(TimeStampedModel):
    diocesis = models.CharField('Nombre Diócesis *', max_length=50,
                                help_text='Nombre de la Diócesis Ej:Diócesis de Loja')
    obispo = models.CharField('Obispo *', max_length=50,
                              help_text='Ingrese el nombre del Obispo Ej: Julio Parrilla')
    direccion = models.ForeignKey(Direccion, related_name='direccion_diocesis')

    class Meta:
        verbose_name = u'Parámetro de la Diócesis'
        verbose_name_plural = u'Parámetros de la Diócesis'
        get_latest_by = 'created'

    def __unicode__(self):
        return 'Parametros-Diocesis: %s' % (self.diocesis)


class ParametrizaParroquia(TimeStampedModel):
    numero_acta = models.PositiveIntegerField(help_text='Ingrese el numero de acta Ej: 1 - 17')
    pagina = models.PositiveIntegerField(help_text='Ingrese el numero de la página Ej: 1 - 17')
    parroquia = models.OneToOneField('Parroquia')
    libro = models.OneToOneField(Libro, null=True, blank=True)

    class Meta:
        verbose_name = u'Parámetro de la Parroquia'
        verbose_name_plural = u'Parámetros de la Parroquia'
        get_latest_by = 'created'

    def __unicode__(self):
        return 'Parametros-Parroquia: %s' % (self.parroquia.nombre)


class Configuracion(TimeStampedModel):
    diocesis = models.BooleanField(default=False)
    iglesia = models.BooleanField(default=False)
    libro_bautismo = models.BooleanField(default=False)
    libro_eucaristia = models.BooleanField(default=False)
    libro_confirmacion = models.BooleanField(default=False)
    libro_matrimonio = models.BooleanField(default=False)


class Padrino(models.Model):
    nombre = models.CharField('nombre', max_length=50)


class Agenda(models.Model):
    evento = models.TextField(max_length= 400, help_text="Ingrese la descripción del evento.")
    fecha = models.DateField(help_text='Ingrese la fecha del evento.')
    hora = models.TimeField(help_text='Ingrese la hora del evento.')
    parroquia = models.ForeignKey(Parroquia)
