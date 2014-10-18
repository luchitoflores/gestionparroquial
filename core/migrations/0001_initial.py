# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('codigo', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=200, null=True, blank=True)),
                ('estado', models.BooleanField(default=False)),
                ('editable', models.BooleanField(default=False)),
            ],
            options={
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
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Funcionalidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=200, null=True, blank=True)),
                ('estado', models.BooleanField(default=False)),
                ('icono', models.CharField(max_length=20)),
                ('funcion', models.ForeignKey(to='core.Funcion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50)),
                ('valor', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=200, null=True, blank=True)),
                ('estado', models.BooleanField(default=False)),
                ('principal', models.BooleanField(default=False)),
                ('catalogo', models.ForeignKey(to='core.Catalogo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parametro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50)),
                ('valor', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=200, null=True, blank=True)),
                ('estado', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
