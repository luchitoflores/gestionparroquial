# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_funcionalidad_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionalidad',
            name='codigo',
            field=models.CharField(unique=True, max_length=20),
        ),
    ]
