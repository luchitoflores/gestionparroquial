# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sacramentos', '0005_auto_20141025_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='tipo_libro',
            field=models.ForeignKey(related_name=b'tipo_libro', to='core.Item', help_text=b'Seleccione un tipo de libro Ej: Bautismo'),
        ),
    ]
