# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_funcionalidad_orden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='estado',
            field=models.ForeignKey(to='core.Item'),
        ),
        migrations.AlterField(
            model_name='item',
            name='padre',
            field=models.ForeignKey(related_name=b'item_padre', blank=True, to='core.Item', null=True),
        ),
    ]
