# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20141005_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionalidad',
            name='url',
            field=models.CharField(max_length=50),
        ),
    ]
