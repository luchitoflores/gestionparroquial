# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20141005_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulo',
            name='estado',
            field=models.ForeignKey(to='core.Item'),
        ),
    ]
