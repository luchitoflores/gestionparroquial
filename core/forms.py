__author__ = 'lucho'

from django.forms import ModelForm
from .models import Catalogo, Item, Parametro

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['estado'].queryset = Item.objects.ItemsPorCatalogoCodigo('EST')

class CatalogoForm(ModelForm):
    class Meta:
        model = Catalogo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CatalogoForm, self).__init__(*args, **kwargs)
        self.fields['estado'].queryset = Item.objects.ItemsPorCatalogoCodigo('EST')

class ParametroForm(ModelForm):
    class Meta:
        model = Parametro
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ParametroForm, self).__init__(*args, **kwargs)
        self.fields['estado'].queryset = Item.objects.ItemsPorCatalogoCodigo('EST')