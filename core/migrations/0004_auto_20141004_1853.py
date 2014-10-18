# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('core', '0003_auto_20141004_1844'),
    ]

    operations = [
        migrations.RenameField(
            model_name='funcionalidad',
            old_name='codigo',
            new_name='url',
        ),
        migrations.RemoveField(
            model_name='funcionalidad',
            name='funcion',
        ),
        migrations.AddField(
            model_name='funcionalidad',
            name='grupo',
            field=models.ForeignKey(default='1', to='auth.Group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='funcionalidad',
            name='modulo',
            field=models.ForeignKey(default=1, to='core.Modulo'),
            preserve_default=False,
        ),
    ]
