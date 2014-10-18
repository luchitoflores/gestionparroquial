# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('core', '0007_auto_20141004_1858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcionalidad',
            name='grupo',
        ),
        migrations.AddField(
            model_name='funcionalidad',
            name='grupos',
            field=models.ManyToManyField(to='auth.Group'),
            preserve_default=True,
        ),
    ]
