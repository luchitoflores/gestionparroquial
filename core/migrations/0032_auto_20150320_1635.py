# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20150320_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionalidad',
            name='grupos',
            field=models.ManyToManyField(to=b'auth.Group'),
        ),
    ]
