# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20141019_2318'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=None,
        ),
    ]
