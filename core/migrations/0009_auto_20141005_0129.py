# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20141004_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionalidad',
            name='icono',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='modulo',
            name='orden',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
