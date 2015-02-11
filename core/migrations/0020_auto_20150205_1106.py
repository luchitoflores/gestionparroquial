# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20141026_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogo',
            name='codigo',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
