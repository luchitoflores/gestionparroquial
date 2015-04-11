# -*- coding: utf-8 -*-
__author__ = 'lucho'

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, NoReverseMatch, resolve
from django.http import HttpResponseRedirect, Http404

def validate_url_name(url):
    print 'me ejecute yo'
    print url
    try:
        reverse(url)
    except NoReverseMatch:
        raise ValidationError('Nombre de url no valida')

def validate_url(url):
    print 'me ejecute'
    print url
    try:
        urlname = resolve(url)
        print urlname
    except Http404:
        print 'se lanzo 2 excepcion'
        raise ValidationError('La url proporcionada no es válida')