# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20141005_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametro',
            name='tipo_parametro',
            field=models.ForeignKey(related_name=b'tipo_parametro', default=1, to='core.Item'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='parametro',
            name='estado',
            field=models.ForeignKey(to='core.Item'),
        ),
    ]
