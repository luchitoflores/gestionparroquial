# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sacramentos', '0006_auto_20141026_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='tipo_libro',
            field=models.CharField(default=b'', help_text=b'Seleccione un tipo de libro Ej: Bautismo', max_length=200, verbose_name='Tipo de Libro *', choices=[(b'', b'-- Seleccione --'), (b'bautismo', b'Bautismo'), (b'eucaristia', b'Primera Comuni\xc3\xb3n'), (b'confirmacion', b'Confirmaci\xc3\xb3n'), (b'matrimonio', b'Matrimonio')]),
        ),
    ]
