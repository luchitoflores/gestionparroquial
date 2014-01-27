$(document).on('ready', inicio);
document.write('<script src="/static/js/tablas.js" type="text/javascript"></script>');

function inicio(){

	detectar_navegador();

	if(localStorage.nombre){
		if(localStorage.getItem('nombre')=='pequenia'){
			$('body').css('font-size', '1em');
		}else if (localStorage.getItem('nombre')=='mediana'){
			$('body').css('font-size', '1.25em');
		} else {
			$('body').css('font-size', '1.5em');
		}
	}

	prueba_localstore();
	combinacionTeclas();
	cancelar_modal();
	var map = '';
	var map2 = '';
	crear_padre('#id_form_crear_padre', '#id_padre','#id_crear_padre', 'm');
	crear_padre('#id_form_crear_madre', '#id_madre','#id_crear_madre', 'f');
	crear_secretaria('#id_form_crear_secretaria', '#id_persona','#id_crear_secretaria');
	// crear_nota($('#id_form_crear_nota'), '#id_fecha','#id_descripcion', '#id_crear_nota');
	autocomplete('#id_padre');
	asignar_padre();
	asignar_email();
	// usuarioCreate();
	crear_nota_marginal($('#id_form_crear_nota'),'#id_crear_nota','/api/nota/add/');
	crear_nota_marginal($('#id_form_crear_nota_matrimonio'),'#id_crear_nota_matrimonio','/api/nota_matrimonio/add/');
	tablas_estilo_bootstrap();
	modelo_tablas('#id_table_secretaria, #id_table_buscar, #id_table_libro,#id_table_asignar_parroquia,#id_table_log, #id_table_feligres, #id_table_matrimonio,#id_table_bautismo,#id_table_eucaristia,#id_table_confirmacion, #id_table_group, #id_table_parroquia, #id_table_provincia, #id_table_canton, #id_table_parroquia_civil, #id_table_sacerdotes');
	ocultar_tablas_aceptar('#id_buscar_feligreses');
	ocultar_tablas_aceptar('#id_buscar_hombres');
	ocultar_tablas_aceptar('#id_buscar_mujeres');
	ocultar_tablas_aceptar('#id_buscar_sacerdotes');
	limpiar_nota();
	radio_button();
	radio_button_sacerdotes();
	radio_button_hombres();
	radio_button_mujeres();
	deshabilitar_campos('#id_form_padre input:text, #id_form_padre select');
	deshabilitar_campos('#id_form_bautizado input:text, #id_form_bautizado select');
	cargar_tabla_usuarios_en_modal();
	cargar_tabla_hombres_en_modal();
	cargar_tabla_mujeres_en_modal();
	cargar_tabla_sacerdotes_en_modal();
	verificar_select_seleccionado();
	seleccionar_cantones('#id_provincia');
	seleccionar_parroquias('#id_canton');
	crear_direccion('#id_form_direccion');
	seleccionar_hora();
	controles_sacramentos();
	controles_feligres();	
	controles_reportes();
	controles_intenciones();
	controles_provincias();
}


// Función para añadir el widget multiselect
function widget_multiselect(identificador){
	$(identificador).multiSelect({
		selectableHeader: "<div style='background:#006dcc; color:white'>Permisos disponibles</div>",
		selectionHeader: "<div style='background:#006dcc; color:white'>Permisos elegidos</div>"
	});
	
	$('#id_select_all').click(function(){
		$(identificador).multiSelect('select_all');
		return false;
	});
	$('#id_delete_all').click(function(){
		$(identificador).multiSelect('deselect_all');
		return false;
	});
}

function mostrar_nota_marginal(idFieldSet){
	var v=$('#id_hidden').val();
	if(v!=0 & v>0){
		mostrar_html(idFieldSet);
	}

}  

function crear_nota_marginal(id_form,id_modal,url_rest){
	$(id_form).on('submit', function(e){
		// $('.alert').remove();
		// $('span').remove();
		e.preventDefault();
		var id=$('#id_hidden').val();
		var url = url_rest;
		var json = $(this).serialize()+"&id="+id+"";
		$.post(url, json, function(data){
			if(data.respuesta){
				$(id_modal).modal('hide');
				limpiar_campos('#id_descripcion');
				$('tbody tr').remove();
				$.each(data.tabla,function(index,element){
					$('tbody').append(element.tabla);
					habilitar_campos('#id_href');
				});
			} else{
				var mensaje = '<div class="alert alert-error">' + 
				'<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>'+
				'<img src="/static/img/error.png" alt=""> Los datos del formulario son incorrectos </div>';
				$('#id_mensaje_nota').html(mensaje);
				$.each(data.errores_nota, function(index, element){
					var mensajes_error = '<span>' + element+ '</span>';
					$("#id_errors_"+index).append(mensajes_error);
				});
				
			}
		});
	})
}



$(document).ajaxStart(function(){
	$('#spinner').show();
}).ajaxStop(function(){
	$('#spinner').hide();
});



function limpiar_campos(campos){
	$(campos).val('');
}

function habilitar_campos(campos){
	$(campos).prop('disabled', false);
}

function deshabilitar_campos(campos){
	$(campos).prop('disabled', true);
	// $(campos).attr('disabled', 'disabled');
}
function deshabilitar_campos2(campos){
	$(campos).prop('enabled', true);
	// $(campos).attr('disabled', 'disabled');
}

function mostrar_html(identificadorhtml){
	$(identificadorhtml).attr('style', 'display:auto');
	// $(identificadorhtml).css('display', 'auto');
}

function ocultar_html(identificadorhtml){
	$(identificadorhtml).attr('style', 'display:none');
	// $(identificadorhtml).css('display', 'none');
}
function ocultar_bottom(identificadorhtml){
	$(identificadorhtml).css('display', 'none');

}
function ocultar_tablas(identificadorhtml,id_radio1,id_radio2,id_div_form){
	$(identificadorhtml).css('display', 'none');
	$(id_radio1).removeClass('btn btn-primary');
	$(id_radio1).addClass('btn');
	$(id_radio2).removeClass('btn btn-primary');
	$(id_radio2).addClass('btn');
	$(id_div_form).css('display', 'none');
	
}
function limpiar_nota(){
	$('#id_cancelar_nota').on('click',function(e){
		limpiar_campos('#id_descripcion');
	});
}
function radio_button(){

	$('div.btn-group button').on('click', function(e){
		e.preventDefault();
		//console.log($(this).parents('div').attr('id'));
		if ($(this).attr('id')=='id_button_cedula'){
			$(this).addClass('btn btn-primary');
			$('#id_button_nombres').removeClass('btn btn-primary');
			$('#id_button_nombres').addClass('btn');
			$('#id_div_form_buscar').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_cedula').attr('style', 'display:inline-block');
			$('#id_div_mensaje').attr('style', 'display:none');
			$('#id_div_busqueda_nombres').attr('style', 'display:none');
			limpiar_campos('#id_query_nombres, #id_query_apellidos'); 
		}
		if ($(this).attr('id')=='id_button_nombres'){
			$(this).addClass('btn btn-primary');
			$('#id_button_cedula').removeClass('btn btn-primary');
			$('#id_button_cedula').addClass('btn');
			$('#id_div_form_buscar').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_nombres').attr('style', 'display:inline-block');
			$('#id_div_mensaje').attr('style', 'display:none');
			$('#id_div_busqueda_cedula').attr('style', 'display:none');
			limpiar_campos('#id_query_cedula'); 
		}
	});

}

function radio_button_hombres(){

	$('div.btn-group button').on('click', function(e){
		e.preventDefault();
		//console.log($(this).parents('div').attr('id'));
		if ($(this).attr('id')=='id_button_cedula_h'){
			$(this).addClass('btn btn-primary');
			$('#id_button_nombres_h').removeClass('btn btn-primary');
			$('#id_button_nombres_h').addClass('btn');
			$('#id_div_form_buscar_h').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_cedula_h').attr('style', 'display:inline-block');
			$('#id_div_mensaje_h').attr('style', 'display:none');
			$('#id_div_busqueda_nombres_h').attr('style', 'display:none');
			limpiar_campos('#id_query_nombres_h, #id_query_apellidos_h'); 
		}
		if ($(this).attr('id')=='id_button_nombres_h'){
			$(this).addClass('btn btn-primary');
			$('#id_button_cedula_h').removeClass('btn btn-primary');
			$('#id_button_cedula_h').addClass('btn');
			$('#id_div_form_buscar_h').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_nombres_h').attr('style', 'display:inline-block');
			$('#id_div_mensaje_h').attr('style', 'display:none');
			$('#id_div_busqueda_cedula_h').attr('style', 'display:none');
			limpiar_campos('#id_query_cedula_h'); 
		}
	});

}
function radio_button_mujeres(){

	$('div.btn-group button').on('click', function(e){
		e.preventDefault();
		//console.log($(this).parents('div').attr('id'));
		if ($(this).attr('id')=='id_button_cedula_m'){
			$(this).addClass('btn btn-primary');
			$('#id_button_nombres_m').removeClass('btn btn-primary');
			$('#id_button_nombres_m').addClass('btn');
			$('#id_div_form_buscar_m').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_cedula_m').attr('style', 'display:inline-block');
			$('#id_div_mensaje_m').attr('style', 'display:none');
			$('#id_div_busqueda_nombres_m').attr('style', 'display:none');
			limpiar_campos('#id_query_nombres_m, #id_query_apellidos_m'); 
		}
		if ($(this).attr('id')=='id_button_nombres_m'){
			$(this).addClass('btn btn-primary');
			$('#id_button_cedula_m').removeClass('btn btn-primary');
			$('#id_button_cedula_m').addClass('btn');
			$('#id_div_form_buscar_m').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_nombres_m').attr('style', 'display:inline-block');
			$('#id_div_mensaje_m').attr('style', 'display:none');
			$('#id_div_busqueda_cedula_m').attr('style', 'display:none');
			limpiar_campos('#id_query_cedula_m'); 
		}
	});

}

function radio_button_sacerdotes(){

	$('div.btn-group button').on('click', function(e){
		e.preventDefault();
		console.log($(this).parents('div').attr('id'));
		if ($(this).attr('id')=='id_button_cedula_s'){
			$(this).addClass('btn btn-primary');
			$('#id_button_nombres_s').removeClass('btn btn-primary');
			$('#id_button_nombres_s').addClass('btn');
			$('#id_div_form_buscar_s').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_cedula_s').attr('style', 'display:inline-block');
			$('#id_div_mensaje_sacerdote').attr('style', 'display:none');
			$('#id_div_busqueda_nombres_s').attr('style', 'display:none');
			limpiar_campos('#id_query_nombres_s, #id_query_apellidos_s'); 
		}
		if ($(this).attr('id')=='id_button_nombres_s'){
			$(this).addClass('btn btn-primary');
			$('#id_button_cedula_s').removeClass('btn btn-primary');
			$('#id_button_cedula_s').addClass('btn');
			$('#id_div_form_buscar_s').attr('style', 'display:auto; margin-top:20px');
			$('#id_div_busqueda_nombres_s').attr('style', 'display:inline-block');
			$('#id_div_mensaje_sacerdote').attr('style', 'display:none');
			$('#id_div_busqueda_cedula_s').attr('style', 'display:none');
			limpiar_campos('#id_query_cedula_s'); 
		}
	});

}

function ocultar_tablas_aceptar(id_modal){
	$(id_modal+' #id_aceptar').on('click',function(e){
		console.log('estoy en clic aceptar')
		ocultar_tablas('#id_table_busqueda_usuarios','#id_button_cedula','#id_button_nombres','#id_div_form_buscar');
		ocultar_bottom('.bottom');
		ocultar_tablas('#id_table_busqueda_hombres','#id_button_cedula_h','#id_button_nombres_h','#id_div_form_buscar_h');
		ocultar_bottom('.bottom');
		ocultar_tablas('#id_table_busqueda_mujeres','#id_button_cedula_m','#id_button_nombres_m','#id_div_form_buscar_m');
		ocultar_bottom('.bottom');
		ocultar_tablas('#id_table_busqueda_sacerdotes','#id_button_cedula_s','#id_button_nombres_s','#id_div_form_buscar_s');
		ocultar_bottom('.bottom');
		limpiar_campos('#id_query_nombres_s, #id_query_apellidos_s','#id_query_cedula_s');
		limpiar_campos('#id_query_nombres_h, #id_query_apellidos_h','#id_query_cedula_h');  
		limpiar_campos('#id_query_nombres_m, #id_query_apellidos_m','#id_query_cedula_m'); 
		limpiar_campos('#id_query_nombres, #id_query_apellidos','#id_query_cedula'); 
	});
}

// function crear_nota(identificador, idnota,idnota2, idmodal){
// 	$(identificador).on('submit', function(e){
// 		e.preventDefault();
// 		var url = '/api/nota/add/';
// 		var json = $(this).serialize();
// 		$.post(url, json , function(data){
// 			if(!data.respuesta){
// 				console.log(data.errores_nota);
// 			}else{
// 				$(idnota).html('< value="'+ data.fecha+'">'+'>');
// 				$(idnota2).html('< value="'+ data.descripcion+'">');
// 				$(idmodal).modal('hide');
// 			}

// 		});
// 	});
// }



// function usuarioCreate(){
// 	$('#id_form_usuario_create').on('submit', function(e){
// 		e.preventDefault();
// 		json = $('#id_form_usuario_create').serialize();
// 		url = '/usuario/add/';
// 		$.post(url, json, function(data, status, jqXHR){
// 			if(data.valido){
// 				// $('#id_confirm_usuario_create').modal('show');
// 				var mensaje = '<div class="alert alert-success">' + 
// 				'<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>'+
// 				'<img src="/static/img/success.png" alt=""> Usuario Creado exitosamente </div>';
// 				$('#id_mensaje').html(mensaje);
// 			} else {
// 				var mensaje = '<div class="alert alert-error">' + 
// 				'<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>'+
// 				'<img src="/static/img/error.png" alt=""> Uno o más datos no son correctos </div>';
// 				$('#id_mensaje').html(mensaje);
// 				console.log(data.errores_usuario);
// 				console.log(data.errores_perfil);
// 				$.each(data.errores_usuario, function(index, element){
// 					$("#id_"+index).addClass('invalid');
// 					console.log("#id_"+index);
// 					console.log("#id_"+element);
// 					var mensajes_error = '<span>' + element+ '</span>';
// 					console.log(mensajes_error);
// 					$("#id_errors_"+index).append(mensajes_error);
// 				});
// 				console.log(data.errores_perfil);
// 				$.each(data.errores_perfil, function(index, element){
// 					$("#id_"+index).addClass('invalid');
// 					console.log("#id_"+index);
// 					console.log("#id_"+element);
// 					var mensajes_error = '<span>' + element+ '</span>';
// 					console.log(mensajes_error);
// 					$("#id_errors_"+index).append(mensajes_error);
// 				});
// 			}
// 		});
// });
// }



//Muestra una tabla en un modal con los datos de feligreses después de una búsqueda
function cargar_tabla_usuarios_en_modal(){
	console.log('ejecutando: cargar tabla en modal usuarios');
	$('#id_form_busqueda').on('submit', function(e){
		e.preventDefault();
		var url= '/api/usuario/';
		var nombres = $('#id_query_nombres').val();
		var apellidos = $('#id_query_apellidos').val();
		var cedula = $('#id_query_cedula').val();
		var id= $('#id_hidden').val();
		mostrar_html("#id_table_busqueda_usuarios");
		var ctx = {'nombres':nombres, 'apellidos':apellidos, 'cedula':cedula, 'id_perfil': id};
		var columnas = [
		{"sType": "html","mData" : "full_name", "bSortable": true},
		{"mData" : "fecha_nacimiento", "bSortable": true},
		{"mData" : "lugar_nacimiento", "bSortable": true},
		{"mData" : "dni", "bSortable": true }];
		$.get(url, ctx, function(data){
			console.log(data.bandera);
			tablas_busqueda_ajax("#id_table_busqueda_usuarios", columnas, data.perfiles);
			map = almacenar_busqueda_en_map(data.perfiles);
			devolver_campos_a_sacramento(map,'#id_administrador');
			devolver_campos_a_sacramento(map,'#id_bautizado');
			devolver_campos_a_sacramento(map,'#id_feligres');
			devolver_campos_a_sacramento(map,'#id_confirmado');
			devolver_campos_a_secretaria(map, '#id_persona');
		});
	});
}

function cargar_tabla_hombres_en_modal(){
	console.log('ejecutando: cargar tabla en modal hombres');
	$('#id_form_busqueda_h').on('submit', function(e){
		e.preventDefault();
		var url= '/api/hombres/';
		var nombres = $('#id_query_nombres_h').val();
		var apellidos = $('#id_query_apellidos_h').val();
		var cedula = $('#id_query_cedula_h').val();
		var id= $('#id_hidden').val();
		mostrar_html("#id_table_busqueda_hombres");
		var ctx = {'nombres':nombres, 'apellidos':apellidos, 'cedula':cedula, 'id_perfil': id};
		var columnas = [
		{"sType": "html","mData" : "full_name", "bSortable": true},
		{"mData" : "fecha_nacimiento", "bSortable": true},
		{"mData" : "lugar_nacimiento", "bSortable": true},
		{"mData" : "dni", "bSortable": true }];
		$.get(url, ctx, function(data){
			console.log(data.bandera);
			tablas_busqueda_ajax("#id_table_busqueda_hombres", columnas, data.perfiles);
			map = almacenar_busqueda_en_map(data.perfiles);
			devolver_campos_de_lista(map,'#id_padre','#id_madre');
			devolver_campos_de_lista(map,'#id_novio','#id_novia');
			
		});
	});
}
function cargar_tabla_mujeres_en_modal(){
	console.log('ejecutando: cargar tabla en modal mujeres');
	$('#id_form_busqueda_m').on('submit', function(e){
		e.preventDefault();
		var url= '/api/mujeres/';
		var nombres = $('#id_query_nombres_m').val();
		var apellidos = $('#id_query_apellidos_m').val();
		var cedula = $('#id_query_cedula_m').val();
		var id= $('#id_hidden').val();
		mostrar_html("#id_table_busqueda_mujeres");
		var ctx = {'nombres':nombres, 'apellidos':apellidos, 'cedula':cedula, 'id_perfil': id};
		var columnas = [
		{"sType": "html","mData" : "full_name", "bSortable": true},
		{"mData" : "fecha_nacimiento", "bSortable": true},
		{"mData" : "lugar_nacimiento", "bSortable": true},
		{"mData" : "dni", "bSortable": true }];
		$.get(url, ctx, function(data){
			console.log(data.bandera);
			tablas_busqueda_ajax("#id_table_busqueda_mujeres", columnas, data.perfiles);
			map = almacenar_busqueda_en_map(data.perfiles);
			devolver_campos_de_lista(map,'#id_padre','#id_madre');
			devolver_campos_de_lista(map,'#id_novio','#id_novia');
			
		});
	});
}
/*//Muestra una tabla en un modal con los datos de feligreses después de una búsqueda
function cargar_tabla_usuarios_en_modal(){
	console.log('ejecutando: cargar tabla en modal');
	var url= '/api/usuario/';
	var nombres = $('#id_query_nombres').val();
	var apellidos = $('#id_query_apellidos').val();
	var cedula = $('#id_query_cedula').val();
	var id= $('#id_hidden').val();
	mostrar_html("#id_table_busqueda_usuarios");
	var ctx = {'nombres':nombres, 'apellidos':apellidos, 'cedula':cedula, 'id_perfil': id};
	var columnas = [
	{"sType": "html","mData" : "full_name", "bSortable": true},
	{"mData" : "lugar_nacimiento", "bSortable": true},
	{"mData" : "dni", "bSortable": true }];
	$.get(url, ctx, function(data){
		console.log(data.bandera);
		tablas_busqueda_ajax("#id_table_busqueda_usuarios", columnas, data.perfiles);
		map = almacenar_busqueda_en_map(data.perfiles);
		devolver_campos_de_lista(map,'#id_padre','#id_madre');
		devolver_campos_de_lista(map,'#id_novio','#id_novia');
		devolver_campos_a_sacramento(map,'#id_bautizado');
		devolver_campos_a_sacramento(map,'#id_feligres');
		devolver_campos_a_sacramento(map,'#id_confirmado');
		devolver_campos_a_secretaria(map, '#id_persona');
	});
	// return false;
}*/

function cargar_tabla_sacerdotes_en_modal(){
	console.log('entre a cargar sacerdotes');
	$('#id_form_busqueda_sacerdotes').on('submit', function(e){
		e.preventDefault();
		var url= '/api/sacerdote/';
		var nombres = $('#id_query_nombres_s').val();
		var apellidos = $('#id_query_apellidos_s').val();
		var cedula = $('#id_query_cedula_s').val();
		// var id= $('#id_hiddens').val();
		mostrar_html("#id_table_busqueda_sacerdotes");
		var ctx = {'nombres':nombres, 'apellidos':apellidos, 'cedula':cedula};
		var columnas = [
		{"sType": "html","mData" : "full_name", "bSortable": true},
		{"mData" : "fecha_nacimiento", "bSortable": true},
		{"mData": "lugar_nacimiento", "bSortable": true},
		{"mData": "dni", "bSortable": true }];
		$.get(url, ctx, function(data){
			tablas_busqueda_ajax("#id_table_busqueda_sacerdotes", columnas, data.perfiles);
			map2 = almacenar_busqueda_en_map(data.perfiles);
			devolver_campos_a_sacerdote(map2,'#id_celebrante');

		});
	});
}



function almacenar_busqueda_en_map(lista){
	var map = {};
	$.each(lista, function(index, element){
		map[element.id] = element; 
	}); 
	return map;
}


// Funcion para buscar y asignar usuarios a Matrimonio 
function devolver_campos_de_lista(map,id_male,id_female){
	console.log('ejecutando: devolver campos de lista');
	console.log(map);
	$('tbody td a.id_click').on('click',function(e){
		console.log('estoy aqui');
		e.preventDefault();
		$("#id_buscar_mujeres").modal('hide'); 
		$("#id_buscar_hombres").modal('hide');
		var id =  $(this).parents('tr').attr('id');
		console.log('id: ' + id);
		var objeto = map[id];
		console.log('objeto: ' + objeto);
		if(objeto.sexo =='m'){
			$(id_male+' option').remove();
			$(id_male).append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');
			limpiar_campos('#id_query_nombres, #id_query_apellidos','#id_query_cedula');
			limpiar_campos('#id_query_nombres_h, #id_query_apellidos_h','#id_query_cedula_h');
			limpiar_campos('#id_query_nombres_m, #id_query_apellidos_m','#id_query_cedula_m');
			ocultar_tablas('#id_table_busqueda_usuarios','#id_button_cedula','#id_button_nombres','#id_div_form_buscar');
			ocultar_bottom('.bottom');
			ocultar_tablas('#id_table_busqueda_hombres','#id_button_cedula_h','#id_button_nombres_h','#id_div_form_buscar_h');
			ocultar_bottom('.bottom');
			ocultar_tablas('#id_table_busqueda_mujeres','#id_button_cedula_m','#id_button_nombres_m','#id_div_form_buscar_m');
			ocultar_bottom('.bottom');

		} 
		if (objeto.sexo =='f') {
			$(id_female+' option').remove();
			$(id_female).append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');
			limpiar_campos('#id_query_nombres, #id_query_apellidos','#id_query_cedula');
			limpiar_campos('#id_query_nombres_h, #id_query_apellidos_h','#id_query_cedula_h');
			limpiar_campos('#id_query_nombres_m, #id_query_apellidos_m','#id_query_cedula_m');
			ocultar_tablas('#id_table_busqueda_usuarios','#id_button_cedula','#id_button_nombres','#id_div_form_buscar');
			ocultar_bottom('.bottom');
			ocultar_tablas('#id_table_busqueda_hombres','#id_button_cedula_h','#id_button_nombres_h','#id_div_form_buscar_h');
			ocultar_bottom('.bottom');
			ocultar_tablas('#id_table_busqueda_mujeres','#id_button_cedula_m','#id_button_nombres_m','#id_div_form_buscar_m');
			ocultar_bottom('.bottom');

		}
	});
}


function prueba2(id){
	console.log('ejecutando: prueba2');
	console.log(map);
	console.log('estoy aqui');
	//e.preventDefault();
	$("#id_buscar_hombres").modal('hide');
	$("#id_buscar_mujeres").modal('hide');  
	$("#id_buscar_feligreses").modal('hide');    	
	//var id =  id;
	console.log('id: ' + id);
	var objeto = map[id];
	console.log('objeto: ' + objeto);
	if(objeto.sexo =='m'){
		$('#id_padre option').remove();
		$('#id_padre').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');	
		$('#id_novio option').remove();
		$('#id_novio').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');	
		$('#id_bautizado option').remove();
		$('#id_bautizado').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');	
		$('#id_feligres option').remove();
		$('#id_feligres').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');	
		$('#id_confirmado option').remove();
		$('#id_confirmado').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');	
		$('#id_persona option').remove();
		$('#id_persona').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');	
		$('#id_administrador option').remove();
		$('#id_administrador').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');	
		limpiar_campos('#id_query_nombres, #id_query_apellidos','#id_query_cedula');
		limpiar_campos('#id_query_nombres_h, #id_query_apellidos_h','#id_query_cedula_h');
		limpiar_campos('#id_query_nombres_m, #id_query_apellidos_m','#id_query_cedula_m');
		ocultar_tablas('#id_table_busqueda_usuarios','#id_button_cedula','#id_button_nombres','#id_div_form_buscar');
		ocultar_bottom('.bottom');
		ocultar_tablas('#id_table_busqueda_hombres','#id_button_cedula_h','#id_button_nombres_h','#id_div_form_buscar_h');
		ocultar_bottom('.bottom');
		ocultar_tablas('#id_table_busqueda_mujeres','#id_button_cedula_m','#id_button_nombres_m','#id_div_form_buscar_m');
		ocultar_bottom('.bottom');
		
	}
	if(objeto.sexo =='f'){
		$('#id_madre option').remove();
		$('#id_madre').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');
		$('#id_novia option').remove();
		$('#id_novia').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');
		$('#id_bautizado option').remove();
		$('#id_bautizado').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');
		$('#id_confirmado option').remove();
		$('#id_confirmado').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');
		$('#id_persona option').remove();
		$('#id_persona').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');
		$('#id_feligres option').remove();
		$('#id_feligres').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');	
		$('#id_administrador option').remove();
		$('#id_administrador').append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');	
		limpiar_campos('#id_query_nombres, #id_query_apellidos','#id_query_cedula');
		limpiar_campos('#id_query_nombres_h, #id_query_apellidos_h','#id_query_cedula_h');
		limpiar_campos('#id_query_nombres_m, #id_query_apellidos_m','#id_query_cedula_m');
		ocultar_tablas('#id_table_busqueda_usuarios','#id_button_cedula','#id_button_nombres','#id_div_form_buscar');
		ocultar_bottom('.bottom');
		ocultar_tablas('#id_table_busqueda_hombres','#id_button_cedula_h','#id_button_nombres_h','#id_div_form_buscar_h');
		ocultar_bottom('.bottom');
		ocultar_tablas('#id_table_busqueda_mujeres','#id_button_cedula_m','#id_button_nombres_m','#id_div_form_buscar_m');
		ocultar_bottom('.bottom');
	}
	
	
}

function prueba3(id){
	console.log('ejecutando: prueba3');
	console.log(map2);
	console.log('estoy aqui p3');
	//e.preventDefault();
	$("#id_buscar_sacerdotes").modal('hide'); 
	//var id =  id;
	var objeto1 = map2[id];
	console.log('id: ' + id);
	console.log('objeto: ' + objeto1);
	$('#id_celebrante option').remove();
	$('#id_celebrante').append('<option value=""> -- Seleccione --</option><option value='+objeto1.id+' selected>'+ objeto1.full_name+'</option>');
	limpiar_campos('#id_query_nombres_s, #id_query_apellidos_s','#id_query_cedula_s');
	ocultar_tablas('#id_table_busqueda_sacerdotes','#id_button_cedula_s','#id_button_nombres_s','#id_div_form_buscar_s');
	ocultar_bottom('.bottom');
	
	
}


function prueba(nombre){
	console.log('ejecutando prueba');
	console.log('ejecutando prueba : ' + nombre);
	//$("#id_buscar_padre").modal('hide');
}


function devolver_campos_a_sacerdote(map, id_sacerdote){
	$('tbody td a.id_click').on('click', function(e){
		e.preventDefault();
		$("#id_buscar_sacerdotes").modal('hide');
		limpiar_campos('#id_query_nombres_s, #id_query_apellidos_s','#id_query_cedula_s');
		var id =  $(this).parents('tr').attr('id');
		var objeto = map2[id];
		$(id_sacerdote+' option').remove();
		$(id_sacerdote).append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>')
		ocultar_tablas('#id_table_busqueda_sacerdotes','#id_button_cedula_s','#id_button_nombres_s','#id_div_form_buscar_s');
		ocultar_bottom('.bottom');

	});
}

function devolver_campos_a_secretaria(map, id_persona){
	$('a.id_click').on('click', function(e){
		e.preventDefault();
		$("#id_buscar_secretaria").modal('hide');  		
		var id =  $(this).parents('tr').attr('id');
		var objeto = map[id];
		$(id_persona+' option').remove();
		$(id_persona).append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>')
		limpiar_campos('#id_query_nombres, #id_query_apellidos','#id_query_cedula');
		ocultar_tablas('#id_table_busqueda_usuarios','#id_button_cedula','#id_button_nombres','#id_div_form_buscar');
		ocultar_bottom('.bottom');
	});
}



// Funcion para buscar y asignar usuarios a Bautismo,Feligres,
// Confirmacion
function devolver_campos_a_sacramento(map,id_feligres){
	$('a.id_click').on('click', function(e){
		// alert('estoy aqui');
		e.preventDefault();
		$("#id_buscar_feligreses").modal('hide');  		
		var id =  $(this).parents('tr').attr('id');
		var objeto = map[id];
		$(id_feligres+' option').remove();
		$(id_feligres).append('<option value=""> -- Seleccione --</option><option value='+objeto.id+' selected>'+ objeto.full_name+'</option>');
		
	});
}


function asignar_padre(){
	$('#id_form_padre').on('submit', function(e){
		e.preventDefault();
		//obtener id del feligres
		//obtener id del padre
		var idfeligres = $('#id_perfil').val();
		var idpadre = $('#id_padre').val();
		console.log('padre' + idpadre);
		console.log('feligres'+idfeligres);
		var ctx = {'idfeligres': idfeligres, 'idpadre': idpadre};
		var url = '/api/asignarpadre/';
		$.post(url , ctx, function(data){
			if(data.bandera==true){
				console.log(data.bandera);
				$(location).attr('href','/usuario/');
			}else{
				console.log(data.bandera);
			}
		});

	});
}

function autocomplete(identificador){
	var labels = [];
	var datos = {};
	$(identificador).typeahead({
		source: function(query, process){
			labels = [];
			datos = {};
			var ctx = {'q': query};
			var url = '/api/usuario/';
			$.get(url, ctx, function(data){
				$.each(data.perfiles, function(index, element){

					labels.push(element.nombres);
					console.log(element.nombres);
					datos[element.nombres] = element;
					console.log(datos);
				});
				process(labels);
			});

		},
		minLength:3,
		highlighter: function(item){
			var p = datos[item];
			var itm = ''
			+ "<div class='typeahead_wrapper'>"
			+ "<div class='typeahead_labels'>"
			+ "<div class='typeahead_primary'>" + p.nombres + ' '+ p.apellidos +"</div>"
			+ "<div class='typeahead_secondary'>" + p.dni + '/' + p.lugar_nacimiento + "</div>"
			+ "</div>"
			+ "</div>";
			return itm;
		}
	});
}


function cancelar_modal(){
	var cancelar = $('.cancelar-modal').on('click', function(e){
		e.preventDefault();
			//limpiar_campos('#id_first_name, #id_last_name, #id_email, #id_nacionalidad, #id_fecha_nacimiento, #id_dni, #id_lugar_nacimiento, #id_estado_civil, #id_profesion, #id_sexo');
			limpiar_campos('#id_form_crear_padre :input');
			limpiar_campos('#id_form_crear_madre :input');
			limpiar_campos('#id_form_crear_secretaria :input');
		});
}

//  Esta función llama a un modal para crear un padre para un feligrés
function crear_padre(identificador, idpadre, idmodal, sexo){
	$(identificador).on('submit', function(e){
		$('span').remove();
		$('.alert').remove();

		e.preventDefault();
		var url = '/api/padre/add/';
		var json = $(this).serialize()+'&sexo='+sexo;
		$.post(url, json , function(data){
			if(!data.respuesta){
				var mensaje = '<div class="alert alert-error">' + 
				'<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>'+
				'<img src="/static/img/error.png" alt=""> Los datos del formulario son incorrectos </div>';
				$('.modal-header').append(mensaje);
				$.each(data.errores_usuario, function(index, element){
					var mensajes_error = '<span class="errors">' + element+ '</span>';
					$(identificador+" #id_errors_"+index).append(mensajes_error);
				});
				$.each(data.errores_perfil, function(index, element){
					var mensajes_error = '<span class="errors">' + element+ '</span>';
					$(identificador + " #id_errors_"+index).append(mensajes_error);
				});

				if(data.messages_error){
					var mensaje = '<div class="alert alert-error">' + 
					'<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>'+
					'<img src="/static/img/error.png" alt=""> '+data.messages_error+' </div>';
					$('.modal-header').append(mensaje);
				}

			}else{
				$(idpadre).html('<option value="">-- Seleccione --</option><option value="'+ data.id+'" selected>'+data.full_name+'</option>');
				$(idmodal).modal('hide');
				limpiar_campos('#id_form_crear_padre :input');
				limpiar_campos('#id_form_crear_madre :input');

			}

		});
});
}


//  Esta función llama a un modal para crear una secretaria
function crear_secretaria(identificador, idsecretaria, idmodal){
	$(identificador).on('submit', function(e){
		$('span').remove();
		$('.alert').remove();
		e.preventDefault();
		var url = '/api/secretaria/add/';
		var json = $(this).serialize();
		$.post(url, json , function(data){
			if(!data.respuesta){
				var mensaje = '<div class="alert alert-error">' + 
				'<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>'+
				'<img src="/static/img/error.png" alt=""> Los datos del formulario son incorrectos </div>';
				$('.modal-header').append(mensaje);
				$.each(data.errores_usuario, function(index, element){
					var mensajes_error = '<span class="errors">' + element+ '</span>';
					$("#id_errors_"+index).append(mensajes_error);
				});
				$.each(data.errores_perfil, function(index, element){
					var mensajes_error = '<span class="errors">' + element+ '</span>';
					$("#id_errors_"+index).append(mensajes_error);
				});
			}else{
				$(idsecretaria).html('<option value="">-- Seleccione --</option><option value="'+ data.id+'" selected>'+data.full_name+'</option>');
				$(idmodal).modal('hide');
				limpiar_campos('#id_form_crear_secretaria :input');
			}

		});
	});
}


//Permite crear via ajax una direccion
function crear_direccion(identificador){
	$(identificador).on('submit', function(e){
		e.preventDefault();
		var url = '/ciudades/direccion/add/'
		var json = $(this).serialize()
		$.post(url, json, function(data){
			if(data.respuesta){
				$('#id_modal_direccion').modal('hide');
			} else{
				console.log('Existen errores');
				console.log(data.errores);
			}
		});
	})
}

// Permite elegir los cantones de acuerdo a sus respectivas provincias
function seleccionar_cantones(identificador){
	$(identificador).on('change', function(e){
		$('#id_canton option').remove();
		$('#id_canton').prop('disabled', true);
		$('#id_parroquia option').remove();
		$('#id_parroquia').append('<option>-- Seleccione --</option>')
		$('#id_parroquia').prop('disabled', true);

		e.preventDefault();
		var url = '/api/ciudades/select/';
		var provincia = $(identificador + ' option:selected').text();
		var ctx = {'provincia': provincia}

		$.get(url, ctx, function(data){
			console.log(data.cantones)
			$.each(data.cantones, function(index, element){
				console.log(element);
				$('#id_canton').prop('disabled', false);
				$('#id_canton').append(element.option)
			});
		});
	})
}

// Permite elegir las parroquias de acuerdo a sus respectivos cantones
function seleccionar_parroquias(identificador){
	$(identificador).on('change', function(e){
		$('#id_parroquia option').remove();
		$('#id_parroquia').prop('disabled', true);
		e.preventDefault();
		var url = '/api/ciudades/select/';
		var canton = $(identificador + ' option:selected').text();
		var ctx = {'canton': canton}

		$.get(url, ctx, function(data){
			console.log(data.parroquias)
			$.each(data.parroquias, function(index, element){
				$('#id_parroquia').prop('disabled', false);
				$('#id_parroquia').append(element.option)
			});
		});
	})
}

// Permite verificar si un select tiene algun valor seleccionado
function verificar_select_seleccionado(){
	if($("#id_provincia option:selected").text()!= '-- Seleccione --'){
		$('#id_canton').prop('disabled', false);
		$('#id_parroquia').prop('disabled', false);
	}
}

function seleccionar_hora(){
	$('#id_tipo').on('change', function(e){
		
		console.log('Change de tipo')

		if ($('#id_tipo option:selected').text()=='Diario') {
			e.preventDefault();
			console.log('Entre al If de cambio');
			($('#id_div_hora')).css('display', 'inline-block');

			
		}else{
			($('#id_div_hora')).css('display', 'none');

		}
		
	});
}

function controles_sacramentos(){

	($('#id_pagina').numeric());
	($('#id_numero_acta').numeric());
	($('#id_numero_libro').numeric());
	($('#id_lugar_sacramento').alpha({allow:" "}));
	($('#id_iglesia').alpha({allow:" "}));
	($('#id_padrino').alpha({allow:" "}));
	($('#id_madrina').alpha({allow:" "}));
	($('#id_abuelo_paterno').alpha({allow:" "}));
	($('#id_abuela_paterna').alpha({allow:" "}));
	($('#id_abuelo_materno').alpha({allow:" "}));
	($('#id_abuela_materna').alpha({allow:" "}));
	($('#id_vecinos_paternos').alpha({allow:" "}));
	($('#id_vecinos_maternos').alpha({allow:" "}));
	($('#id_testigo_novio').alpha({allow:" "}));
	($('#id_testigo_novia').alpha({allow:" "}));
	// para nota marginal
	($('#id_descripcion').alpha({allow:" "}));

}

function controles_feligres(){

	($('#id_first_name').alpha({allow:" "}));
	($('#id_last_name').alpha({allow:" "}));
	($('#id_profesion').alpha({allow:" "}));
	($('#id_lugar_nacimiento').alpha({allow:" "}));
	($('#id_celular').numeric());
}
function controles_intenciones(){
	($('#id_intencion').alpha({allow:" "}));
	($('#id_oferente').alpha({allow:" "}));
	($('#id_ofrenda').numeric({allow:"."}));

}
function controles_reportes(){
	($('#id_form_anio #id_anio').numeric());
}

function controles_provincias(){

	($('#id_nombre').alpha({allow:" "}));
	($('#id_abreviatura').numeric());

	// para campo name de grupos

	($('#id_name').alpha({allow:" "}));

	// para parametriza diocesis
	($('#id_diocesis').alpha({allow:" "}));
	($('#id_obispo').alpha({allow:" "}));
	($('#id_telefono').numeric());
	($('#id_buscar_sacramentos').numeric());
}



function asignar_email(){
	$('#id_form_email').on('submit', function(e){
		e.preventDefault();
		var ctx = $(this).serialize()
		var url = '/api/email/add/'
		$.post(url, ctx, function(data){
			if (data.respuesta) {
				$('#id_modal_email').modal('hide');
			} else {
				console.log('hay errores')
				var mensaje = '<br/><div class="alert alert-error">' + 
				'<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>'+
				'<img src="/static/img/error.png" alt=""> El email ingresado no es válido </div>';
				$('.modal-header').append(mensaje);

				$.each(data.errores, function(index, element){
					var mensajes_error = '<span class="errors">' + element+ '</span>';
					$('#id_email' + " #id_errors_"+index).append(mensajes_error);
				});
			}
		});
	});
}


function combinacionTeclas(){
	Mousetrap.bind('ctrl+f1', function(){
		document.location.href='/home/';
	});


	Mousetrap.bind('mod+f2', function(){
		document.location.href='/group/';
	});

	Mousetrap.bind('ctrl+f3', function(){
		document.location.href='/log/';
	});


	Mousetrap.bind(['mod+f6', 'meta+f6'], function(e){
		if (e.preventDefault) {
			e.preventDefault();
		} else {
			e.returnValue = false;
		}

		document.location.href='/administrador/';
	});

	Mousetrap.bind(['ctrl+f7', 'meta+f7'], function(e){
		if (e.preventDefault) {
			e.preventDefault();
		} else {
			e.returnValue = false;
		}

		document.location.href='/usuario/';
	});

	Mousetrap.bind('mod+f8', function(){
		document.location.href='/sacerdote/';
	});

	Mousetrap.bind('mod+f9', function(){
		document.location.href='/asignar/secretaria/';
	});

	Mousetrap.bind('mod+f10', function(){
		document.location.href='/ciudades/provincia/';
	});

	Mousetrap.bind('mod+f11', function(){
		document.location.href='/ciudades/canton/';
	});

	Mousetrap.bind(['mod+f12', 'meta+f12'], function(e){
		if (e.preventDefault) {
			e.preventDefault();
		} else {
			e.returnValue = false;
		}

		document.location.href='/ciudades/parroquia/';
	});

	Mousetrap.bind('shift+alt+l', function(e){
		document.location.href='/libro/';
	});

	Mousetrap.bind('mod+b', function(){
		document.location.href='/bautismo/';
	});																																																																								

	Mousetrap.bind('mod+alt+e', function(e){
		document.location.href='/eucaristia/';
	});

	Mousetrap.bind('mod+c', function(){
		document.location.href='/confirmacion/';
	});

	Mousetrap.bind('mod+m', function(){
		document.location.href='/matrimonio/';
	});

	Mousetrap.bind('mod+alt+i', function(){
		document.location.href='/intencion/';
	});

	Mousetrap.bind('mod+alt+p', function(e){
		document.location.href='/parroquia/';
	});

	
}

function prueba_localstore(){
	$('#pequenia').on('click', function(e){
		e.preventDefault();
		if(!localStorage.nombre){
			localStorage.nombre='pequenia';
		} else {
			localStorage.setItem('nombre', 'pequenia');
		}
		$('body').css('font-size', '1em');

	});
	$('#mediana').on('click', function(e){
		e.preventDefault();
		if(!localStorage.nombre){
			localStorage.nombre='media';
		} else {
			localStorage.setItem('nombre', 'media');
		}
		$('body').css('font-size', '1.25em');
	});
	$('#grande').on('click', function(e){
		e.preventDefault();
		if(!localStorage.nombre){
			localStorage.nombre='grande';
		} else {
			localStorage.setItem('nombre', 'grande');
		}
		$('body').css('font-size', '1.5em');
	});
}



// Script para detectar el navegador que está utilizando el usuario
function detectar_navegador(){
	var BrowserDetect = 
	{
		init: function () 
		{
			this.browser = this.searchString(this.dataBrowser) || "Other";
			this.version = this.searchVersion(navigator.userAgent) ||       this.searchVersion(navigator.appVersion) || "Unknown";
		},

		searchString: function (data) 
		{
			for (var i=0 ; i < data.length ; i++)   
			{
				var dataString = data[i].string;
				this.versionSearchString = data[i].subString;

				if (dataString.indexOf(data[i].subString) != -1)
				{
					return data[i].identity;
				}
			}
		},

		searchVersion: function (dataString) 
		{
			var index = dataString.indexOf(this.versionSearchString);
			if (index == -1) return;
			return parseFloat(dataString.substring(index+this.versionSearchString.length+1));
		},

		dataBrowser: 
		[
		{ string: navigator.userAgent, subString: "Chrome",  identity: "Chrome" },
		{ string: navigator.userAgent, subString: "MSIE",    identity: "Explorer" },
		{ string: navigator.userAgent, subString: "Firefox", identity: "Firefox" },
		{ string: navigator.userAgent, subString: "Safari",  identity: "Safari" },
		{ string: navigator.userAgent, subString: "Opera",   identity: "Opera" }
		]

	};

	BrowserDetect.init();

	if (BrowserDetect.browser == "Explorer"){ 
		if (BrowserDetect.version<9){
			alert('Se recomienda utilizar Internet Explorer 9 o superior, Chrome, Firefox u Opera para el ingreso al sistema.');
		}
	} 

	if (BrowserDetect.browser == "Safari"){
		alert('Se recomienda utilizar Chrome, Firefox u Opera para el ingreso al sistema');
	}

}



