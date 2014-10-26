__author__ = 'lucho'

from django.forms import ModelForm
from .models import Catalogo, Item, Parametro

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['estado'].queryset = Item.objects.items_por_catalogo_cod('EST')
        if self.instance.id:
            if self.instance.catalogo.padre:
                self.fields['padre'].queryset = Item.objects.filter(catalogo=self.instance.catalogo.padre)
            else:
                self.fields['padre'].queryset = Item.objects.none()
        else:
            self.fields['padre'].queryset = Item.objects.none()


class CatalogoForm(ModelForm):
    class Meta:
        model = Catalogo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CatalogoForm, self).__init__(*args, **kwargs)
        self.fields['estado'].queryset = Item.objects.items_por_catalogo_cod('EST')
        if self.instance.id:
            if self.instance.padre:
                self.fields['padre'].queryset = Catalogo.objects.filter(id=self.instance.padre.id)
            else:
                self.fields['padre'].queryset = Catalogo.objects.all()
        else:
            self.fields['padre'].queryset = Catalogo.objects.all()

class ParametroForm(ModelForm):
    class Meta:
        model = Parametro
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ParametroForm, self).__init__(*args, **kwargs)
        self.fields['estado'].queryset = Item.objects.items_por_catalogo_cod('EST')