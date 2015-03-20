# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20150320_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionalidad',
            name='codigo',
            field=models.CharField(max_length=20, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
