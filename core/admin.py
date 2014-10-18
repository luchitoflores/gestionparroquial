from django.contrib import admin
from .models import Item, Catalogo, Parametro, Funcion, Funcionalidad, Modulo
from .forms import ItemForm, CatalogoForm, ParametroForm
from django.core.urlresolvers import reverse
from django.forms.widgets import RadioSelect
from django.db import models


admin.AdminSite.site_header = 'Administrador de la Aplicacion'
admin.AdminSite.site_title = 'Sitio de Administracion'

class ItemInline(admin.StackedInline):
    model = Item
    form = ItemForm
    extra = 0
    radio_fields = {"estado": admin.HORIZONTAL}


# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    list_display = ('codigo','nombre','valor', 'estado', 'padre', 'principal')
    search_fields = ('nombre', 'codigo',)
    list_filter = ('catalogo', )
    change_list_filter_template = "admin/filter_listing.html"


@admin.register(Catalogo)
class CatalogoAdmin(admin.ModelAdmin):
    form = CatalogoForm
    list_display = ('codigo', 'nombre','descripcion', 'estado', 'padre', 'editable', 'items')
    inlines = [ItemInline, ]
    search_fields = ('nombre', 'codigo',)

    def items(self, obj):
        redirect_url = reverse('admin:core_item_changelist')
        extra = "?catalogo__id__exact=%d" % obj.id
        return "<a href='%s'>Items por Catalogo</a>" % (redirect_url + extra)

    items.allow_tags = True

@admin.register(Parametro)
class ParametroAdmin(admin.ModelAdmin):
    form = ParametroForm
    list_display = ('codigo','nombre', 'valor', 'estado', 'tipo_parametro')
    search_fields = ('nombre', 'codigo', 'valor')
    list_filter = ('tipo_parametro',)

@admin.register(Funcionalidad)
class FuncionalidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'url', 'modulo','estado','orden')
    search_fields = ('nombre', 'modulo')
    list_filter = ('modulo',)

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre','descripcion', 'estado',)
    search_fields = ('nombre', 'codigo',)


#admin.site.register(Funcion)
