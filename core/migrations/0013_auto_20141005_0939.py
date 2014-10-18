# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20141005_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogo',
            name='estado',
            field=models.ForeignKey(related_name=b'estado_item', to='core.Item'),
        ),
    ]
