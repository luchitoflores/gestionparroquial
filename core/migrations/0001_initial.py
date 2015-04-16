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
            name='Funcion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=200, null=True, blank=True)),
                ('estado', models.BooleanField(default=False)),
                ('eliminada', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Funciones',
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
                ('descripcion', models.TextField(max_length=200, null=True, blank=True)),
                ('orden', models.PositiveIntegerField(null=True, blank=True)),
                ('icono', models.CharField(max_length=20, null=True, blank=True)),
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
                ('principal', models.BooleanField(default=False)),
                ('catalogo', models.ForeignKey(to='core.Catalogo')),
                ('estado', models.ForeignKey(to='core.Item')),
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
                ('orden', models.PositiveIntegerField(null=True, blank=True)),
                ('estado', models.ForeignKey(to='core.Item')),
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
                ('estado', models.ForeignKey(to='core.Item')),
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
            name='estado',
            field=models.ForeignKey(to='core.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='funcionalidad',
            name='grupos',
            field=models.ManyToManyField(to='auth.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='funcionalidad',
            name='modulo',
            field=models.ForeignKey(to='core.Modulo'),
            preserve_default=True,
        ),
    ]
