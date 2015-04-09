# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20150320_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionalidad',
            name='grupos',
            field=models.ManyToManyField(related_name=b'grupos', to=b'auth.Group'),
        ),
    ]
