# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20150320_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionalidad',
            name='estado',
            field=models.BooleanField(),
        ),
    ]
