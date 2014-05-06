from django import template
from django import forms
register = template.Library()

@register.filter(is_safe=True)
def css_class(value, arg):
	return value,css_classes(extra_classes={'class':arg})
	# return value.label_tag(attrs={'class': arg})

@register.filter(is_safe=True)
def label_class(value, arg):
	return value.label_tag(attrs={'class': arg})

@register.filter(is_safe=True)
def field_attrs(value, attr, arg):
	# return value.as_widget(attrs={""+value+"": arg})
	return value.as_widget(attrs={value: arg})

@register.filter(is_safe=True)
def field_no_required(value):
	del value.field.widget.attrs['required']
	return value

@register.filter
def class_name(value):
    return value.__class__.__name__

@register.filter(is_safe=True)
def field_value(value, arg):
	print 'imprimiendo'
	print value
	field = value.form.fields[''+str(value.name)+''].initial= arg
	return value

@register.filter(is_safe=True)
def hidden_value(value, arg):
	form = value.form
	form.fields[''+str(value.name)+''].initial= arg
	form.fields[''+str(value.name)+''].widget = forms.HiddenInput()
	return value
