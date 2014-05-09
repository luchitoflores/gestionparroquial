# -*- coding:utf-8 -*-
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

# from sacramentos.rest import api_usuario_list
from sacramentos.views import (
	configuracion_inicial_view,
	usuarioCreateView, UsuarioListView,edit_usuario_view, UsuarioDetailView,
	usuario_reporte_honorabilidad,
	sacerdote_create_view, SacerdoteListView,  sacerdote_update_view,
	administrator_create_view, AdministradorListView, administrador_create_view, administrador_update_view,
	secretaria_update_view, 
	libro_create_view, libro_update_view ,LibroListView,libro_pdf,
	matrimonio_create_view,MatrimonioListView,matrimonio_update_view,matrimonio_vigencia_view,
	matrimonio_ajax_view,MatrimonioNoVigenteListView,
	matrimonio_certificado,
	bautismo_update_view, BautismoListView, bautismo_create_view,
	bautismo_acta,bautismo_certificado,
	eucaristia_create_view,eucaristia_update_view,EucaristiaListView,eucaristia_reporte,
	confirmacion_create_view,confirmacion_update_view,ConfirmacionListView,confirmacion_reporte,
	parroquia_create_view, parroquia_update_view, ParroquiaListView, DirectorioParroquiasListView, 
	IglesiaListView, IglesiaCreateView, IglesiaUpdateView,
	# AsignarParroquiaCreate, AsignarParroquiaUpdate, AsignarParroquiaList,
	asignar_parroquia_create, asignar_parroco_a_parroquia, asignar_parroquia_update, asignar_parroco_list, parroco_periodos_asignacion_list, parroco_periodos_asignacion_update, nuevo_periodo_asignacion,
	asignar_secretaria_create, asignar_secretaria_update, asignar_secretaria_list, SecretariaListView, 
	intencion_create_view, IntencionListView, intencion_edit_view,
	parametriza_diocesis_create,
	parametriza_parroquia_create,
	LogListView,exportar_csv_logs,
	reporte_anual_sacramentos,reporte_intenciones,reporte_permisos,reporte_parroquias_sacerdotes,
	reporte_sacerdotes_parroquias,
	redireccionar,redireccionar_parametros,
	)
# from sacramentos.rest import ParroquiaResource


# entry_resource = ParroquiaResource()


urlpatterns = patterns('', 
	url(r'^configuracion/inicial/$', configuracion_inicial_view, name='configuracion_inicial'),
	#url para el home de personas
	# url(r'^personas/$', login_required(TemplateView.as_view(template_name='personas.html'),login_url='/login/'), 
	# 	name='personas'),
	url(r'^personas/$', redireccionar, name='personas'),
	#urls de usuarios
	url(r'^usuario/$', UsuarioListView.as_view(), name='usuario_list'),
	url(r'^crear/usuario/$', usuarioCreateView, name='usuario_create'),
	url(r'^detalle/usuario/(?P<pk>\d+)/$', UsuarioDetailView.as_view(), name='usuario_detail'),
	url(r'^usuario/(?P<pk>\d+)/$', edit_usuario_view, name='usuario_update'),
	# url(r'^padre/crear/$', padre_create_view, name='padre_create'),
	# url(r'^feligres/crear/$', feligres_create_view, name='feligres_create'),
	url(r'^sacerdote/$', SacerdoteListView.as_view(), name='sacerdote_list'),
	url(r'^crear/sacerdote/$', sacerdote_create_view, name='sacerdote_create'),
	url(r'^sacerdote/(?P<pk>\d+)/$', sacerdote_update_view, name='sacerdote_update'),
	url(r'^reporte/sacerdote/(?P<pk>\d+)/$', reporte_sacerdotes_parroquias, name='reporte_sacerdotes'),
	url(r'^usuario_certificado/(?P<pk>\d+)/$',usuario_reporte_honorabilidad, name='usuario_certificado'),
	# Urls Administradores
	url(r'^administrador/$', AdministradorListView.as_view(), name='administrador_list'),
	url(r'^administrador/(?P<pk>\d+)/$', administrador_update_view, name='administrador_update'),
	url(r'^crear/administrador/$', administrador_create_view, name='administrador_create'),
	url(r'^crear/administrator/$', administrator_create_view, name='administrator_create'),
	
	#urls para asignar secretarias
	url(r'^crear/asignar/secretaria/$', asignar_secretaria_create , name='asignar_secretaria_create'),
	url(r'^asignar/secretaria/(?P<pk>\d+)/$', asignar_secretaria_update , name='asignar_secretaria_update'),
	# url(r'^asignar/secretaria/$', asignar_secretaria_list , name='asignar_secretaria_list'),
	url(r'^asignar/secretaria/$', SecretariaListView.as_view() , name='asignar_secretaria_list'),
	url(r'^secretaria/(?P<pk>\d+)/$', secretaria_update_view, name='secretaria_update'),
	
	#urls del api rest usuarios
	url(r'^api/usuario/$', 'sacramentos.rest.buscar_usuarios', name='api_usuario_list'),
	url(r'^api/hombres/$', 'sacramentos.rest.buscar_hombres', name='buscar_hombres'),
	url(r'^api/mujeres/$', 'sacramentos.rest.buscar_mujeres', name='buscar_mujeres'),
	url(r'^api/sacerdote/$', 'sacramentos.rest.buscar_sacerdotes', name='api_sacerdote_list'),
	url(r'^api/crear/sacerdote/$', 'sacramentos.rest.sacerdote_create_ajax', name='api_create_sacerdote'),
	url(r'^api/asignarpadre/$', 'sacramentos.rest.edit_padre_viewapi', name='api_setear_padre'),
	url(r'^api/crear/padre/$', 'sacramentos.rest.padre_create_ajax', name='api_create_padre'),
	url(r'^api/crear/iglesia/$', 'sacramentos.rest.iglesia_api_create', name='api_iglesia_create'),
	url(r'^api/crear/libro/$', 'sacramentos.rest.libro_api_create', name='api_libro_create'),


	# urls de libro
	url(r'^libro/$',LibroListView.as_view(),name='libro_list'),
	url(r'^crear/libro/$',libro_create_view, name='libro_create'),
	url(r'^libro/(?P<pk>\d+)/$',libro_update_view, name='libro_update'),
	# url(r'^libro/(?P<pk>\d+)/$',libro_pdf, name='libro_update'),

	#urls de sacramentos
	url(r'^sacramentos/$', login_required(TemplateView.as_view(template_name='sacramentos.html'), login_url='/login/'), 
		name='sacramentos'),
	url(r'^reporte/$', login_required(TemplateView.as_view(template_name='reportes.html'), login_url='/login/'), 
		name='reportes'),
	url(r'^parametro/$',redireccionar_parametros, name='redireccionar_parametros'),
	# url(r'^parametro/$', login_required(TemplateView.as_view(template_name='parametros.html'), login_url='/login/'), 
	# 	name='parametros'),


	#urls de matrimonio y reporte
	
	url(r'^matrimonio/$',MatrimonioListView.as_view(),name='matrimonio_list'),
	url(r'^matrimonio/no_vigentes/$',MatrimonioNoVigenteListView.as_view(),name='matrimonio_list_no_vigentes'),
	url(r'^crear/matrimonio/$',matrimonio_create_view, name='matrimonio_create'),
	url(r'^matrimonio/(?P<pk>\d+)/$',matrimonio_update_view, name='matrimonio_update'),
	url(r'^matrimonio/ajax/$',matrimonio_ajax_view, name='matrimonio_ajax'),
	url(r'^matrimonio/(?P<pk>\d+)/vigencia/$',matrimonio_vigencia_view, name='matrimonio_vigencia'),
	url(r'^matrimonio_certificado/(?P<pk>\d+)/$',matrimonio_certificado, name='matrimonio_certificado'),

	#urls de Nota Marginal para crear con bautismo y matrimonios

	url(r'^api/crear/nota/$', 'sacramentos.rest.nota_marginal_create_ajax', 
		name='api_create_nota'),
	
	url(r'^api/crear/nota_matrimonio/$', 'sacramentos.rest.nota_create_matrimonio_ajax', 
		name='api_create_nota_matrimonio'),

	#urls de Bautismo
	# url(r'^usuario/(?P<id_fel>\d+)/bautismo/crear/$',bautismo_create_view, 
	# 	name='bautismo_create'),
	url(r'^bautismo/$',BautismoListView.as_view(),name='bautismo_list'),
	url(r'^crear/bautismo/$',bautismo_create_view, name='bautismo_create'),
	url(r'^bautismo/(?P<pk>\d+)/$',bautismo_update_view, name='bautismo_update'),
	url(r'^bautismo_acta/(?P<pk>\d+)/$',bautismo_acta, name='bautismo_acta'),
	url(r'^bautismo_certificado/(?P<pk>\d+)/$',bautismo_certificado, name='bautismo_certificado'),



	#urls de Eucaristia
	url(r'^primeracomunion/$',EucaristiaListView.as_view(),name='eucaristia_list'),
	url(r'^crear/primeracomunion/$',eucaristia_create_view,name='eucaristia_create'),
	url(r'^primeracomunion/(?P<pk>\d+)/$',eucaristia_update_view, name='eucaristia_update'),
	url(r'^reporte/primeracomunion/(?P<pk>\d+)/$',eucaristia_reporte, name='eucaristia_reporte'),


	#urls de Confirmacion
	url(r'^confirmacion/$',ConfirmacionListView.as_view(),name='confirmacion_list'),
	url(r'^crear/confirmacion/$',confirmacion_create_view, name='confirmacion_create'),
	url(r'^confirmacion/(?P<pk>\d+)/$',confirmacion_update_view, name='confirmacion_update'),
	url(r'^reporte/confirmacion(?P<pk>\d+)/$',confirmacion_reporte, name='confirmacion_reporte'),

	#urls de parroquia eclesiástica
	url(r'^parroquia/$', ParroquiaListView.as_view(), name='parroquia_list'),
	url(r'^crear/parroquia/$', parroquia_create_view, name='parroquia_create'),
	url(r'^parroquia/(?P<pk>\d+)/$', parroquia_update_view, name='parroquia_update'),
	url(r'^reporte/parroquia/(?P<pk>\d+)/$', reporte_parroquias_sacerdotes, 
		name='reporte_parroquias_sacerdotes'),
	url(r'^directorio/parroquias/$', DirectorioParroquiasListView.as_view(), name='directorio_parroquias'),

	#urls para Iglesias
	url(r'^iglesia/$', IglesiaListView.as_view(), name='iglesia_list'),
	url(r'^crear/iglesia/$', IglesiaCreateView.as_view(), name='iglesia_create'),
	url(r'^iglesia/(?P<pk>\d+)/$',IglesiaUpdateView.as_view(), name='iglesia_update'),
	
	
	#urls para asignación de parroquias a los párrocos
	# Permite agregar un nuevo párroco a una nueva parroquia
	url(r'^crear/asignar/parroquia/parroco/$', asignar_parroquia_create , name='asignar_parroco'),
	# Permite agregar un párroco a una parroquia preestablecida
	url(r'^crear/asignar/parroquia/(?P<pk>\d+)/parroco/$', asignar_parroco_a_parroquia , name='asignar_parroco_a_parroquia'),
	#Permite editar y ver todas las asignaciones de un sacerdote en una parroquia
	url(r'^asignar/parroquia/parroco/(?P<pk>\d+)/$', asignar_parroquia_update , name='asignar_parroco_update'),
	# Lista de los periodos de asignación de un párroco a una parroquia
	url(r'^parroco/periodos/asignacion/(?P<pk>\d+)/$', parroco_periodos_asignacion_list , name='parroco_periodos_asignacion_list'),
	url(r'^crear/parroco/periodo/asignacion/(?P<pk>\d+)/$', nuevo_periodo_asignacion , name='nuevo_periodo_asignacion'),
	# Edición de los periodos de asignación de un párroco a una parroquia
	url(r'^parroco/periodos/(?P<pk>\d+)/asignacion/$', parroco_periodos_asignacion_update , name='parroco_periodos_asignacion_update'),
	#Muestra los párrocos que están asignados a una parroquia
	url(r'^parrocos/parroquia/(?P<pk>\d+)/$', asignar_parroco_list , name='asignar_parroco_list'),
	

	#urls para intenciones de misa
	url(r'^intencion/$', IntencionListView.as_view(), name='intencion_list'),
	url(r'^crear/intencion/$', intencion_create_view, name='intencion_create'),
	url(r'^intencion/(?P<pk>\d+)/$', intencion_edit_view, name='intencion_update'),


	#urls del api rest usuarios
	url(r'^api/usuario/$', 'sacramentos.rest.buscar_usuarios', name='api_usuario_list'),
	url(r'^api/crear/padre/$', 'sacramentos.rest.padre_create_ajax', name='api_create_padre'),
	url(r'^api/crear/secretaria/$', 'sacramentos.rest.secretaria_create_ajax', name='api_create_secretaria'),
	url(r'^api/crear/email/$', 'sacramentos.rest.agregar_email', name='agregar_email'),
	
	# urls de parameetrizacion de la diocesis(general)
	url(r'^crear/parametros/diocesis/$', parametriza_diocesis_create, name='parametriza_create'),
	
	# urls de parametrizacion de las parroquias

	url(r'^crear/parametros/parroquia/$', parametriza_parroquia_create, name='parametriza_parroquia_create'),
	

	#urls del api rest parroquias
	# (r'^api/', include(entry_resource.urls)),


	url(r'^api/datatables/$', 'sacramentos.rest.data_tables'),
	url(r'^datatables/$', TemplateView.as_view(template_name="data_tables.html")), 

	# urls de los logs de ekklesia
	url(r'^log/$', LogListView.as_view(), name='log_list'),
	url(r'^log/csv/$', exportar_csv_logs, name='logs_csv'),

	#reportes
	
	url(r'^reporte/anual/$', reporte_anual_sacramentos, name='reporte_anual'),
	url(r'^reporte/intenciones/$', reporte_intenciones, name='reporte_intenciones'),
	url(r'^reporte/permisos/$', reporte_permisos, name='reporte_permiso'),


	)