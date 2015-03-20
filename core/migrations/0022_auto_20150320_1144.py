# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
        ('core', '0021_auto_20150213_1305'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='parametro',
            name='codigo',
            field=models.CharField(unique=True, max_length=20),
        ),
    ]
