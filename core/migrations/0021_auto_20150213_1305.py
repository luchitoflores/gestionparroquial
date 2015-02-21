# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20150205_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametro',
            name='tipo_parametro',
            field=models.ForeignKey(related_name=b'tipo_parametro', blank=True, to='core.Item', null=True),
        ),
    ]
