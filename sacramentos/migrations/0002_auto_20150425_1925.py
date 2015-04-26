# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sacramentos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignacionparroquia',
            name='es_activo',
            field=models.BooleanField(default=False, verbose_name=b'Est\xc3\xa1 activo?'),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='es_activo',
            field=models.BooleanField(default=False, verbose_name=b'Est\xc3\xa1 activo?'),
        ),
        migrations.AlterField(
            model_name='iglesia',
            name='es_activo',
            field=models.BooleanField(default=False, verbose_name=b'Est\xc3\xa1 activo?'),
        ),
        migrations.AlterField(
            model_name='intencion',
            name='es_activo',
            field=models.BooleanField(default=False, verbose_name=b'Est\xc3\xa1 activo?'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='es_activo',
            field=models.BooleanField(default=False, verbose_name=b'Est\xc3\xa1 activo?'),
        ),
        migrations.AlterField(
            model_name='notamarginal',
            name='es_activo',
            field=models.BooleanField(default=False, verbose_name=b'Est\xc3\xa1 activo?'),
        ),
        migrations.AlterField(
            model_name='parametrizadiocesis',
            name='es_activo',
            field=models.BooleanField(default=False, verbose_name=b'Est\xc3\xa1 activo?'),
        ),
        migrations.AlterField(
            model_name='parametrizaparroquia',
            name='es_activo',
            field=models.BooleanField(default=False, verbose_name=b'Est\xc3\xa1 activo?'),
        ),
        migrations.AlterField(
            model_name='parroquia',
            name='es_activo',
            field=models.BooleanField(default=False, verbose_name=b'Est\xc3\xa1 activo?'),
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='es_activo',
            field=models.BooleanField(default=False, verbose_name=b'Est\xc3\xa1 activo?'),
        ),
        migrations.AlterField(
            model_name='periodoasignacionparroquia',
            name='es_activo',
            field=models.BooleanField(default=False, verbose_name=b'Est\xc3\xa1 activo?'),
        ),
        migrations.AlterField(
            model_name='sacramento',
            name='es_activo',
            field=models.BooleanField(default=False, verbose_name=b'Est\xc3\xa1 activo?'),
        ),
    ]
