from django.contrib import admin
from .models import Item, Catalogo, Parametro, Funcion, Funcionalidad, Modulo
from .forms import ItemForm, CatalogoForm, ParametroForm
from django.core.urlresolvers import reverse
from django.forms.widgets import RadioSelect
from django.db import models
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet


admin.AdminSite.site_header = 'Administrador de la Aplicacion'
admin.AdminSite.site_title = 'Sitio de Administracion'
# admin.site.disable_action('delete_selected')


class ItemInline(admin.StackedInline):
    model = Item
    form = ItemForm
    extra = 1
    radio_fields = {"estado": admin.HORIZONTAL}


# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    list_display = ('codigo','nombre','valor', 'estado', 'padre', 'principal')
    search_fields = ('nombre', 'codigo',)
    list_filter = ('catalogo', )
    change_list_filter_template = "admin/filter_listing.html"
    list_per_page = 20


@admin.register(Catalogo)
class CatalogoAdmin(admin.ModelAdmin):
    form = CatalogoForm
    list_display = ('codigo', 'nombre','descripcion', 'estado', 'padre', 'editable', 'items')
    inlines = [ItemInline, ]
    search_fields = ('nombre', 'codigo',)
    list_per_page = 20

    def items(self, obj):
        redirect_url = reverse('admin:core_item_changelist')
        extra = "?catalogo__id__exact=%d" % obj.id
        return "<a href='%s'>Ver Items</a>" % (redirect_url + extra)

    items.allow_tags = True

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide MyInline in the add view
            if isinstance(inline, ItemInline) and obj is None:
                print 'crear'
            else:
                print obj
            yield inline.get_formset(request, obj), inline

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "padre":
            kwargs["queryset"] = Item.objects.none()
            print 'estoy aqui'
        return super(CatalogoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Parametro)
class ParametroAdmin(admin.ModelAdmin):
    form = ParametroForm
    list_display = ('codigo','nombre', 'valor', 'estado', 'tipo_parametro')
    search_fields = ('nombre', 'codigo', 'valor')
    list_filter = ('tipo_parametro',)
    list_per_page = 20

@admin.register(Funcionalidad)
class FuncionalidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo','url', 'modulo','estado','orden')
    search_fields = ('nombre', 'modulo')
    list_filter = ('modulo',)
    list_per_page = 20

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre', 'descripcion', 'estado', 'orden')
    search_fields = ('nombre', 'codigo',)
    list_per_page = 20


