# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sacramentos', '0003_padrino'),
    ]

    operations = [
        migrations.AlterField(
            model_name='padrino',
            name='nombre',
            field=models.CharField(max_length=50, verbose_name=b'nombre'),
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='nacionalidad',
            field=models.ForeignKey(related_name=b'persona', to='core.Item', help_text=b'Escoja la nacionalidad. Ej: Ecuador'),
        ),
    ]
