# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20141004_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(max_length=200, null=True, blank=True)),
                ('estado', models.BooleanField(default=False)),
                ('orden', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='codigo',
            field=models.CharField(max_length=20),
        ),
    ]
