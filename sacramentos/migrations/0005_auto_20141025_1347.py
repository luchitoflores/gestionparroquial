# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sacramentos', '0004_auto_20141025_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilusuario',
            name='estado_civil',
            field=models.ForeignKey(related_name=b'estado_civil', to='core.Item', help_text=b'Elija el estado civil. Ej: Soltero/a'),
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='sexo',
            field=models.ForeignKey(related_name=b'genero', to='core.Item', help_text=b'Elija el sexo de la persona. Ej: Masculino'),
        ),
    ]
