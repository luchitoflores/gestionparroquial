# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20141004_1855'),
    ]

    operations = [
        migrations.RenameField(
            model_name='funcionalidad',
            old_name='modulo',
            new_name='modulo_prueba',
        ),
    ]
