# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20141026_0926'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('catalogo', 'codigo')]),
        ),
    ]
