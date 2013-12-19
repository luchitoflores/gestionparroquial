# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User

from .models import Provincia, Canton,Parroquia, Direccion

	
admin.site.register(Provincia)
admin.site.register(Canton)
admin.site.register(Parroquia)
admin.site.register(Direccion)