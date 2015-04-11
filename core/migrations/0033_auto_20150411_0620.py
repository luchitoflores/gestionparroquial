# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20150320_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionalidad',
            name='url',
            field=models.CharField(max_length=50, validators=[core.validators.validate_url]),
        ),
    ]
