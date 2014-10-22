# *-* coding:utf-8 *-* 
# Create your views here.
import json
from django.shortcuts import render,get_object_or_404, render_to_response,redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from sacramentos.models import (PerfilUsuario,
	Libro,Matrimonio,Bautismo,Eucaristia,Confirmacion,NotaMarginal,
	Parroquia, Intencion,
	AsignacionParroquia, PeriodoAsignacionParroquia,
	ParametrizaDiocesis,ParametrizaParroquia,
	)
from django.http import HttpResponse, HttpResponseRedirect


def index_view(request):
	return HttpResponseRedirect('/')

def home_view(request):
	if request.user.is_authenticated():
		return redirect('/home/')
	else:
		return redirect('/')

def buscar_sacramentos_view(request):
	if not request.user.is_authenticated():

		query = request.GET.get('q', '')
		results1=''
		results2=''
		results3=''
		results4=''
		results5=''
		if query:
			try:
				f = PerfilUsuario.objects.get(dni=query)
				results1=Bautismo.objects.filter(bautizado=f)
				results2=Eucaristia.objects.filter(feligres=f)
				results3=Confirmacion.objects.filter(confirmado=f)
				
				if f.sexo=='m':
					results4=Matrimonio.objects.filter(novio=f)
				else:
					results5=Matrimonio.objects.filter(novia=f)
			except ObjectDoesNotExist:
				return render_to_response("buscar.html",{"results1": results1,"results2":results2,
					"results3":results3,"results4":results4,"results5":results5})

		else:
			results1=[]
			results2=[]
			results3=[]
			results4=[]
			results5=[]
		return render_to_response("buscar.html",{"results1": results1,"results2":results2,"results3":results3,
		"results4":results4,"results5":results5})
	else:
		return HttpResponseRedirect('/home/')