# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('codigo', models.CharField(unique=True, max_length=50)),
                ('descripcion', models.TextField(max_length=200, null=True, blank=True)),
                ('estado', models.CharField(max_length=1, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')])),
                ('editable', models.BooleanField(default=False)),
                ('padre', models.ForeignKey(blank=True, to='core.Catalogo', null=True)),
            ],
            options={
                'verbose_name_plural': 'Catalogos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domicilio', models.CharField(help_text=b'Ingrese las calles. Ej: 10 agosto 10-04, Bernardo Valdivieso', max_length=100, verbose_name=b'Calles *')),
                ('telefono', models.CharField(max_length=10, null=True, verbose_name=b'Tel\xc3\xa9fono', blank=True)),
            ],
            options={
                'ordering': ['provincia__nombre', 'canton__nombre', 'parroquia__nombre'],
                'verbose_name': 'Direcci\xf3n',
                'verbose_name_plural': 'Direcciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Funcionalidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=50, validators=[core.validators.validate_url_name])),
                ('codigo', models.CharField(unique=True, max_length=20)),
                ('estado', models.CharField(max_length=1, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')])),
                ('descripcion', models.TextField(max_length=200, null=True, blank=True)),
                ('orden', models.PositiveIntegerField(null=True, blank=True)),
                ('icono', models.CharField(max_length=20, null=True, blank=True)),
                ('grupos', models.ManyToManyField(to='auth.Group')),
            ],
            options={
                'verbose_name_plural': 'Funcionalidades',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50)),
                ('valor', models.CharField(max_length=50, null=True, blank=True)),
                ('descripcion', models.TextField(max_length=200, null=True, blank=True)),
                ('estado', models.CharField(max_length=1, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')])),
                ('principal', models.BooleanField(default=False)),
                ('catalogo', models.ForeignKey(to='core.Catalogo')),
                ('padre', models.ForeignKey(related_name=b'item_padre', blank=True, to='core.Item', null=True)),
            ],
            options={
                'verbose_name_plural': 'Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LogDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log', models.ForeignKey(to='admin.LogEntry')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(unique=True, max_length=20)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=200, null=True, blank=True)),
                ('estado', models.CharField(max_length=1, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')])),
                ('orden', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Modulos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parametro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(unique=True, max_length=20)),
                ('nombre', models.CharField(max_length=50)),
                ('valor', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=200, null=True, blank=True)),
                ('estado', models.CharField(max_length=1, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')])),
                ('tipo_parametro', models.ForeignKey(related_name=b'tipo_parametro', blank=True, to='core.Item', null=True)),
            ],
            options={
                'verbose_name_plural': 'Parametros',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('catalogo', 'codigo')]),
        ),
        migrations.AddField(
            model_name='funcionalidad',
            name='modulo',
            field=models.ForeignKey(to='core.Modulo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='direccion',
            name='canton',
            field=models.ForeignKey(related_name='direccion_canton', to='core.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='direccion',
            name='parroquia',
            field=models.ForeignKey(related_name='direccion_parroquia', to='core.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='direccion',
            name='provincia',
            field=models.ForeignKey(related_name='direccion_provincia', to='core.Item'),
            preserve_default=True,
        ),
    ]
