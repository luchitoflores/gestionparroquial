# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20141004_1856'),
    ]

    operations = [
        migrations.RenameField(
            model_name='funcionalidad',
            old_name='modulo_prueba',
            new_name='modulo',
        ),
        migrations.RenameField(
            model_name='funcionalidad',
            old_name='nombre_url',
            new_name='url',
        ),
    ]
