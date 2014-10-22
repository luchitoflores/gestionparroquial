# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20141014_2217'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='catalogo',
            options={'verbose_name_plural': 'Catalogos'},
        ),
        migrations.AlterModelOptions(
            name='funcion',
            options={'verbose_name_plural': 'Funciones'},
        ),
        migrations.AlterModelOptions(
            name='funcionalidad',
            options={'verbose_name_plural': 'Funcionalidades'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name_plural': 'Items'},
        ),
        migrations.AlterModelOptions(
            name='modulo',
            options={'verbose_name_plural': 'Modulos'},
        ),
        migrations.AlterModelOptions(
            name='parametro',
            options={'verbose_name_plural': 'Parametros'},
        ),
    ]
