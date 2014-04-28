# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PerfilUsuario'
        db.create_table(u'sacramentos_perfilusuario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='usuario', null=True, to=orm['auth.User'])),
            ('dni', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('nacionalidad', self.gf('django.db.models.fields.CharField')(default='', max_length=2)),
            ('padre', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='papa', null=True, to=orm['sacramentos.PerfilUsuario'])),
            ('madre', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='mama', null=True, to=orm['sacramentos.PerfilUsuario'])),
            ('fecha_nacimiento', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('lugar_nacimiento', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('sexo', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('estado_civil', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('profesion', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('celular', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'sacramentos', ['PerfilUsuario'])

        # Adding model 'Libro'
        db.create_table(u'sacramentos_libro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('numero_libro', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('tipo_libro', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('fecha_apertura', self.gf('django.db.models.fields.DateField')()),
            ('fecha_cierre', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('estado', self.gf('django.db.models.fields.CharField')(default=None, max_length=20)),
            ('parroquia', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parroquia', to=orm['sacramentos.Parroquia'])),
            ('primera_pagina', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, null=True, blank=True)),
            ('primera_acta', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, null=True, blank=True)),
        ))
        db.send_create_signal(u'sacramentos', ['Libro'])

        # Adding model 'Sacramento'
        db.create_table(u'sacramentos_sacramento', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('numero_acta', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pagina', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('fecha_sacramento', self.gf('django.db.models.fields.DateField')()),
            ('celebrante', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sacramento_sacerdote', to=orm['sacramentos.PerfilUsuario'])),
            ('lugar_sacramento', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('padrino', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('madrina', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('iglesia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sacramentos.Iglesia'])),
            ('libro', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sacramento_libro', to=orm['sacramentos.Libro'])),
            ('parroquia', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sacramento_parroquia', to=orm['sacramentos.Parroquia'])),
        ))
        db.send_create_signal(u'sacramentos', ['Sacramento'])

        # Adding model 'Bautismo'
        db.create_table(u'sacramentos_bautismo', (
            (u'sacramento_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sacramentos.Sacramento'], unique=True, primary_key=True)),
            ('bautizado', self.gf('django.db.models.fields.related.OneToOneField')(related_name='bautizado', unique=True, to=orm['sacramentos.PerfilUsuario'])),
            ('abuelo_paterno', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('abuela_paterna', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('abuelo_materno', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('abuela_materna', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('vecinos_paternos', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('vecinos_maternos', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
        ))
        db.send_create_signal(u'sacramentos', ['Bautismo'])

        # Adding model 'Eucaristia'
        db.create_table(u'sacramentos_eucaristia', (
            (u'sacramento_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sacramentos.Sacramento'], unique=True, primary_key=True)),
            ('feligres', self.gf('django.db.models.fields.related.OneToOneField')(related_name='feligres', unique=True, to=orm['sacramentos.PerfilUsuario'])),
        ))
        db.send_create_signal(u'sacramentos', ['Eucaristia'])

        # Adding model 'Confirmacion'
        db.create_table(u'sacramentos_confirmacion', (
            (u'sacramento_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sacramentos.Sacramento'], unique=True, primary_key=True)),
            ('confirmado', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='confirmado', unique=True, null=True, to=orm['sacramentos.PerfilUsuario'])),
        ))
        db.send_create_signal(u'sacramentos', ['Confirmacion'])

        # Adding model 'Matrimonio'
        db.create_table(u'sacramentos_matrimonio', (
            (u'sacramento_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sacramentos.Sacramento'], unique=True, primary_key=True)),
            ('novio', self.gf('django.db.models.fields.related.OneToOneField')(related_name='novio', unique=True, to=orm['sacramentos.PerfilUsuario'])),
            ('novia', self.gf('django.db.models.fields.related.OneToOneField')(related_name='novia', unique=True, to=orm['sacramentos.PerfilUsuario'])),
            ('testigo_novio', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('testigo_novia', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('vigente', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tipo_matrimonio', self.gf('django.db.models.fields.CharField')(default='Catolico', max_length=100)),
        ))
        db.send_create_signal(u'sacramentos', ['Matrimonio'])

        # Adding model 'NotaMarginal'
        db.create_table(u'sacramentos_notamarginal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
            ('descripcion', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('bautismo', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='bautismo', null=True, to=orm['sacramentos.Bautismo'])),
            ('matrimonio', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='matrimonio', null=True, to=orm['sacramentos.Matrimonio'])),
        ))
        db.send_create_signal(u'sacramentos', ['NotaMarginal'])

        # Adding model 'AsignacionParroquia'
        db.create_table(u'sacramentos_asignacionparroquia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('persona', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sacramentos.PerfilUsuario'])),
            ('parroquia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sacramentos.Parroquia'])),
        ))
        db.send_create_signal(u'sacramentos', ['AsignacionParroquia'])

        # Adding model 'PeriodoAsignacionParroquia'
        db.create_table(u'sacramentos_periodoasignacionparroquia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('inicio', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('estado', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('asignacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sacramentos.AsignacionParroquia'])),
        ))
        db.send_create_signal(u'sacramentos', ['PeriodoAsignacionParroquia'])

        # Adding model 'Intenciones'
        db.create_table(u'sacramentos_intenciones', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('intencion', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
            ('hora', self.gf('django.db.models.fields.TimeField')()),
            ('oferente', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('ofrenda', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('parroquia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sacramentos.Parroquia'])),
            ('individual', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('iglesia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sacramentos.Iglesia'])),
        ))
        db.send_create_signal(u'sacramentos', ['Intenciones'])

        # Adding model 'Parroquia'
        db.create_table(u'sacramentos_parroquia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('direccion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='direccion_parroquia', to=orm['ciudades.Direccion'])),
        ))
        db.send_create_signal(u'sacramentos', ['Parroquia'])

        # Adding model 'Iglesia'
        db.create_table(u'sacramentos_iglesia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parroquia', self.gf('django.db.models.fields.related.ForeignKey')(related_name='iglesias', to=orm['sacramentos.Parroquia'])),
            ('principal', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'sacramentos', ['Iglesia'])

        # Adding model 'ParametrizaDiocesis'
        db.create_table(u'sacramentos_parametrizadiocesis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('diocesis', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('obispo', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('direccion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='direccion_diocesis', to=orm['ciudades.Direccion'])),
        ))
        db.send_create_signal(u'sacramentos', ['ParametrizaDiocesis'])

        # Adding model 'ParametrizaParroquia'
        db.create_table(u'sacramentos_parametrizaparroquia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('numero_acta', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pagina', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('parroquia', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sacramentos.Parroquia'], unique=True)),
            ('libro', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sacramentos.Libro'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'sacramentos', ['ParametrizaParroquia'])


    def backwards(self, orm):
        # Deleting model 'PerfilUsuario'
        db.delete_table(u'sacramentos_perfilusuario')

        # Deleting model 'Libro'
        db.delete_table(u'sacramentos_libro')

        # Deleting model 'Sacramento'
        db.delete_table(u'sacramentos_sacramento')

        # Deleting model 'Bautismo'
        db.delete_table(u'sacramentos_bautismo')

        # Deleting model 'Eucaristia'
        db.delete_table(u'sacramentos_eucaristia')

        # Deleting model 'Confirmacion'
        db.delete_table(u'sacramentos_confirmacion')

        # Deleting model 'Matrimonio'
        db.delete_table(u'sacramentos_matrimonio')

        # Deleting model 'NotaMarginal'
        db.delete_table(u'sacramentos_notamarginal')

        # Deleting model 'AsignacionParroquia'
        db.delete_table(u'sacramentos_asignacionparroquia')

        # Deleting model 'PeriodoAsignacionParroquia'
        db.delete_table(u'sacramentos_periodoasignacionparroquia')

        # Deleting model 'Intenciones'
        db.delete_table(u'sacramentos_intenciones')

        # Deleting model 'Parroquia'
        db.delete_table(u'sacramentos_parroquia')

        # Deleting model 'Iglesia'
        db.delete_table(u'sacramentos_iglesia')

        # Deleting model 'ParametrizaDiocesis'
        db.delete_table(u'sacramentos_parametrizadiocesis')

        # Deleting model 'ParametrizaParroquia'
        db.delete_table(u'sacramentos_parametrizaparroquia')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'ciudades.canton': {
            'Meta': {'ordering': "('nombre',)", 'object_name': 'Canton'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'provincia'", 'to': u"orm['ciudades.Provincia']"})
        },
        u'ciudades.direccion': {
            'Meta': {'object_name': 'Direccion'},
            'canton': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ciudades.Canton']"}),
            'domicilio': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parroquia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parroquia_civil'", 'to': u"orm['ciudades.Parroquia']"}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ciudades.Provincia']"}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'ciudades.parroquia': {
            'Meta': {'ordering': "('nombre',)", 'object_name': 'Parroquia'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'canton': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'canton'", 'to': u"orm['ciudades.Canton']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'ciudades.provincia': {
            'Meta': {'ordering': "('nombre',)", 'object_name': 'Provincia'},
            'abreviatura': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sacramentos.asignacionparroquia': {
            'Meta': {'object_name': 'AsignacionParroquia'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'parroquia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sacramentos.Parroquia']"}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sacramentos.PerfilUsuario']"})
        },
        u'sacramentos.bautismo': {
            'Meta': {'object_name': 'Bautismo', '_ormbases': [u'sacramentos.Sacramento']},
            'abuela_materna': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'abuela_paterna': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'abuelo_materno': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'abuelo_paterno': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'bautizado': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'bautizado'", 'unique': 'True', 'to': u"orm['sacramentos.PerfilUsuario']"}),
            u'sacramento_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sacramentos.Sacramento']", 'unique': 'True', 'primary_key': 'True'}),
            'vecinos_maternos': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'vecinos_paternos': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'})
        },
        u'sacramentos.confirmacion': {
            'Meta': {'object_name': 'Confirmacion', '_ormbases': [u'sacramentos.Sacramento']},
            'confirmado': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'confirmado'", 'unique': 'True', 'null': 'True', 'to': u"orm['sacramentos.PerfilUsuario']"}),
            u'sacramento_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sacramentos.Sacramento']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'sacramentos.eucaristia': {
            'Meta': {'object_name': 'Eucaristia', '_ormbases': [u'sacramentos.Sacramento']},
            'feligres': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'feligres'", 'unique': 'True', 'to': u"orm['sacramentos.PerfilUsuario']"}),
            u'sacramento_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sacramentos.Sacramento']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'sacramentos.iglesia': {
            'Meta': {'ordering': "('nombre',)", 'object_name': 'Iglesia'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parroquia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'iglesias'", 'to': u"orm['sacramentos.Parroquia']"}),
            'principal': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'sacramentos.intenciones': {
            'Meta': {'ordering': "['fecha', 'hora']", 'object_name': 'Intenciones'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'hora': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iglesia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sacramentos.Iglesia']"}),
            'individual': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'intencion': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'oferente': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'ofrenda': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'parroquia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sacramentos.Parroquia']"})
        },
        u'sacramentos.libro': {
            'Meta': {'object_name': 'Libro'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'estado': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20'}),
            'fecha_apertura': ('django.db.models.fields.DateField', [], {}),
            'fecha_cierre': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'numero_libro': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parroquia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parroquia'", 'to': u"orm['sacramentos.Parroquia']"}),
            'primera_acta': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'primera_pagina': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'tipo_libro': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'})
        },
        u'sacramentos.matrimonio': {
            'Meta': {'object_name': 'Matrimonio', '_ormbases': [u'sacramentos.Sacramento']},
            'novia': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'novia'", 'unique': 'True', 'to': u"orm['sacramentos.PerfilUsuario']"}),
            'novio': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'novio'", 'unique': 'True', 'to': u"orm['sacramentos.PerfilUsuario']"}),
            u'sacramento_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sacramentos.Sacramento']", 'unique': 'True', 'primary_key': 'True'}),
            'testigo_novia': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'testigo_novio': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'tipo_matrimonio': ('django.db.models.fields.CharField', [], {'default': "'Catolico'", 'max_length': '100'}),
            'vigente': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'sacramentos.notamarginal': {
            'Meta': {'object_name': 'NotaMarginal'},
            'bautismo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bautismo'", 'null': 'True', 'to': u"orm['sacramentos.Bautismo']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matrimonio': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'matrimonio'", 'null': 'True', 'to': u"orm['sacramentos.Matrimonio']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'sacramentos.parametrizadiocesis': {
            'Meta': {'object_name': 'ParametrizaDiocesis'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'diocesis': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'direccion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'direccion_diocesis'", 'to': u"orm['ciudades.Direccion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'obispo': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'sacramentos.parametrizaparroquia': {
            'Meta': {'object_name': 'ParametrizaParroquia'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'libro': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sacramentos.Libro']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'numero_acta': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pagina': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parroquia': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sacramentos.Parroquia']", 'unique': 'True'})
        },
        u'sacramentos.parroquia': {
            'Meta': {'object_name': 'Parroquia'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'direccion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'direccion_parroquia'", 'to': u"orm['ciudades.Direccion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'sacramentos.perfilusuario': {
            'Meta': {'object_name': 'PerfilUsuario'},
            'celular': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dni': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'estado_civil': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'fecha_nacimiento': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugar_nacimiento': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'madre': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mama'", 'null': 'True', 'to': u"orm['sacramentos.PerfilUsuario']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'nacionalidad': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2'}),
            'padre': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'papa'", 'null': 'True', 'to': u"orm['sacramentos.PerfilUsuario']"}),
            'parroquias': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['sacramentos.Parroquia']", 'null': 'True', 'through': u"orm['sacramentos.AsignacionParroquia']", 'blank': 'True'}),
            'profesion': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'sexo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'usuario'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'sacramentos.periodoasignacionparroquia': {
            'Meta': {'object_name': 'PeriodoAsignacionParroquia'},
            'asignacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sacramentos.AsignacionParroquia']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'estado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'sacramentos.sacramento': {
            'Meta': {'object_name': 'Sacramento'},
            'celebrante': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sacramento_sacerdote'", 'to': u"orm['sacramentos.PerfilUsuario']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_sacramento': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iglesia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sacramentos.Iglesia']"}),
            'libro': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sacramento_libro'", 'to': u"orm['sacramentos.Libro']"}),
            'lugar_sacramento': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'madrina': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'numero_acta': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'padrino': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pagina': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parroquia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sacramento_parroquia'", 'to': u"orm['sacramentos.Parroquia']"})
        }
    }

    complete_apps = ['sacramentos']