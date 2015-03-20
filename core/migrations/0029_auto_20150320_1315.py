# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20150320_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='valor',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
