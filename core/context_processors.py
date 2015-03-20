from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy

from .models import Funcionalidad, Modulo


def menu(request):
    menuvar = dict()
    if request.user.is_authenticated():
        menu = dict()
        listMenus= list()
        modulos = Modulo.objects.modulos_por_usuario(request.user)
        for m in modulos:
            funcionalidades = Funcionalidad.objects.funcionalidades_por_modulo(m,request.user)
            list_submenus = list()
            if funcionalidades:
                for f in funcionalidades:
                    submenu = {'nombre': f.nombre, 'url': reverse_lazy(f.url), 'icon': f.icono}#'url': reverse_lazy(f.url)}
                    list_submenus.append(submenu)

                menu["nombre"] = m.nombre
                menu["submenu"] = list_submenus
                menu["id"] = m.id
                listMenus.append(menu)
                menu = {}
        menuvar["menu"] = listMenus
    return {"menuvar":menuvar}