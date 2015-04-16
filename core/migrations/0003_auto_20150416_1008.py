# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150416_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogo',
            name='estado',
            field=models.CharField(max_length=1, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')]),
        ),
    ]
