# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150416_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='estado',
            field=models.CharField(max_length=1, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')]),
        ),
    ]
