# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20141026_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Canton',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(help_text=b'Ingrese un Canton Ej: Esp\xc3\xadndola, Calvas', max_length=50, verbose_name=b'Nombre *')),
                ('abreviatura', models.CharField(help_text=b'Ingrese una abreviatura Ej:lo, Ca, A', unique=True, max_length=4, verbose_name=b'C\xc3\xb3digo *')),
            ],
            options={
                'ordering': ['nombre', 'provincia__nombre'],
                'verbose_name': 'Cant\xf3n',
                'verbose_name_plural': 'Cantones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domicilio', models.CharField(help_text=b'Ingrese las calles. Ej: 10 agosto 10-04, Bernardo Valdivieso', max_length=100, verbose_name=b'Calles *')),
                ('telefono', models.CharField(max_length=10, null=True, verbose_name=b'Tel\xc3\xa9fono', blank=True)),
                ('canton', models.ForeignKey(related_name='direccion_canton', to='core.Item')),
                ('parroquia', models.ForeignKey(related_name='direccion_parroquia', to='core.Item')),
                ('provincia', models.ForeignKey(related_name='direccion_provincia', to='core.Item')),
            ],
            options={
                'ordering': ['provincia__nombre', 'canton__nombre', 'parroquia__nombre'],
                'verbose_name': 'Direcci\xf3n',
                'verbose_name_plural': 'Direcciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parroquia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(help_text=b'Ingrese Parroquia Ej: Catamayo, Cariamanga', max_length=50, verbose_name=b'Nombre *')),
                ('abreviatura', models.CharField(help_text=b'Ingrese una abreviatura Ej:ca, C-a', unique=True, max_length=4, verbose_name=b'C\xc3\xb3digo *')),
                ('canton', models.ForeignKey(related_name=b'canton', verbose_name='Cant\xf3n *', to='ciudades.Canton')),
            ],
            options={
                'ordering': ['nombre', 'canton__nombre'],
                'verbose_name': 'Parroquia Civil',
                'verbose_name_plural': 'Prarroquias Civiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(help_text=b'Ingrese el nombre de una Provincia Ej: Loja. El Oro', max_length=50, verbose_name=b'Nombre *')),
                ('abreviatura', models.CharField(help_text=b'Ingrese una abreviatura para la Provincia Ej: LO', unique=True, max_length=4, verbose_name=b'C\xc3\xb3digo *')),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name': 'Provincia',
                'verbose_name_plural': 'Provincias',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='canton',
            name='provincia',
            field=models.ForeignKey(related_name=b'provincia', verbose_name='Provincia *', to='ciudades.Provincia'),
            preserve_default=True,
        ),
    ]
