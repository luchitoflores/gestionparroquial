# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20150320_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulo',
            name='codigo',
            field=models.CharField(unique=True, max_length=20),
        ),
    ]
