# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20150320_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionalidad',
            name='estado',
            field=models.ForeignKey(to='core.Item'),
        ),
    ]
