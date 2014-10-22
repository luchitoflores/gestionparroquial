# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sacramentos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intencion',
            name='tipo_intencion',
        ),
        migrations.AddField(
            model_name='intencion',
            name='individual',
            field=models.BooleanField(default=None, help_text=b'Elija el tipo de intencion', verbose_name=b'Es unica?'),
            preserve_default=True,
        ),
    ]
