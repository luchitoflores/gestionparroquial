# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20141004_1853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcionalidad',
            name='url',
        ),
        migrations.AddField(
            model_name='funcionalidad',
            name='nombre_url',
            field=models.CharField(default=b'mi url', max_length=50),
            preserve_default=True,
        ),
    ]
