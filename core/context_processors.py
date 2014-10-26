from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy

from .models import Funcionalidad, Modulo


def menu(request):
    menuvar = dict()
    if request.user.is_authenticated():
        menu = dict()
        #listSubmenus= list()
        listMenus= list()
        listSubmenuAux = list()
        modulos = Modulo.objects.ModulosPorUsuario(request.user)
        for m in modulos:
            funcionalidades = Funcionalidad.objects.funcionalidades_por_modulo(m,request.user )
            listSubmenus = list()
            if funcionalidades:
                for f in funcionalidades:
                    submenu = {'nombre': f.nombre, 'url': reverse_lazy(f.url)}#'url': reverse_lazy(f.url)}
                    listSubmenus.append(submenu)

                menu["nombre"] = m.nombre
                menu["submenu"] = listSubmenus
                menu["id"] = m.id
                listMenus.append(menu)
                menu = {}
        menuvar["menu"] = listMenus
            #menu = {'menu': [
            #    {'nombre': 'Iglesia', 'url': reverse_lazy('iglesia_list')},
            #    {'nombre': 'Ciudades', 'submenu': [
            #        {'nombre': 'Provincias', 'url': reverse_lazy('provincia_list')},
            #        {'nombre': 'Cantones', 'url': reverse_lazy('canton_list')},
            #        {'nombre': 'Parroquias', 'url': reverse_lazy('parroquia_list')},
            #    ]},
            #    {'nombre': 'Intenciones', 'url': reverse_lazy('intencion_list')},
            #]}
    return {"menuvar":menuvar}