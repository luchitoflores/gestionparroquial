$(document).on('ready', inicio);
document.write('<script src="/static/js/tablas.js" type="text/javascript"></script>');

function inicio() {
    detectar_navegador();
    cargar_accion_logs();
    tabla_vacia();
    cancelar_modal();
    var map = '';
    var map2 = '';
    reporte_intenciones();
    crear_feligres('#id_crear_padre', '#id_padre', '#id_modal_padre');
    crear_feligres('#id_crear_madre', '#id_madre', '#id_modal_madre');
    crear_feligres('#id_crear_novio', '#id_novio', '#id_modal_padre');
    crear_feligres('#id_crear_novia', '#id_novia', '#id_modal_madre');
    crear_feligres('#id_crear_bautizado', '#id_bautizado', '#id_modal_feligres');
    crear_feligres('#id_crear_feligres', '#id_feligres', '#id_modal_feligres');
    crear_feligres('#id_crear_confirmado', '#id_confirmado', '#id_modal_feligres');
    crear_sacerdote('#id_crear_sacerdote');
    crear_iglesia('#id_crear_iglesia');
    crear_libro_sacramental('#id_libro_bautismo');
    crear_libro_sacramental('#id_libro_eucaristia');
    crear_libro_sacramental('#id_libro_confirmacion');
    crear_libro_sacramental('#id_libro_matrimonio');
    crear_libro('#id_crear_libro');
    crear_secretaria('#id_form_crear_secretaria', '#id_persona', '#id_crear_secretaria');
    asignar_padre();
    asignar_email();
    crear_nota_marginal('#id_form_crear_nota', '#id_crear_nota', '/api/crear/nota/');
    crear_nota_marginal('#id_form_crear_nota_matrimonio', '#id_crear_nota_matrimonio', '/api/crear/nota_matrimonio/');
    tablas_estilo_bootstrap();
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
    acordeon();
    $(".dateinput").datepicker();
    //Inicializar todos los tooltips
    $('[data-toggle="tooltip"]').tooltip({'placement': 'top'});
    $('[data-toggle="popover"]').popover();

    /*jQuery.each($("select[multiple]"), function () {
        // "Locations" can be any label you want
        SelectFilter.init(this.id, "Locations", 0, "/media/");
    })*/

    /*campo_no_requerido('#id_bautizado, #id_feligres, #id_confirmado');*/
    /*modelo_tablas('#id_table_asignar_parroquia');*/

}

function cargar_accion_logs(){
    var action_flag = $('#id_hidden_action_flag').val();
    $("#id_action_flag").val(action_flag);
}


//Mantener la eleccion del acordeon
function acordeon() {
    var last = $.cookie('activeAccordionGroup');
    if (last != null) {
        //remove default collapse settings
        $("#accordion .collapse").removeClass('in');
        //show the last visible group
        $("#" + last).collapse("show");
    }

    $("#accordion").bind('shown', function () {
        var active = $("#accordion .in").attr('id');
        $.cookie('activeAccordionGroup', active)
    });
}


//Función para verificar si una tabla está vacía
function tabla_vacia() {
    var tbody = $('table').attr('tbody');
    //cuenta el total de columnas del thead de una tabla
    var total_columnas = $('table > thead > tr > th').length
    //cuenta el total de filas del tbody de una tabla
    var total_filas = $('table > tbody > tr > td').length
    if (total_filas == 0) {
        $('table > tbody:last').append('<tr><td colspan=' + total_columnas + '>No existen registros disponibles</td></tr>');
    }

}

// Función para añadir el widget multiselect
function widget_multiselect(identificador) {
    $(identificador).multiSelect({
        selectableHeader: "<div style='background:#006dcc; color:white'>Permisos disponibles</div>",
        selectionHeader: "<div style='background:#006dcc; color:white'>Permisos elegidos</div>"
    });

    $('#id_select_all').click(function () {
        $(identificador).multiSelect('select_all');
        return false;
    });
    $('#id_delete_all').click(function () {
        $(identificador).multiSelect('deselect_all');
        return false;
    });
}

function mostrar_nota_marginal(idFieldSet) {
    var v = $('#id_hidden').val();
    if (v != 0 & v > 0) {
        mostrar_html(idFieldSet);
    }

}

function campo_no_requerido(identificador) {
    $(identificador).removeAttr('required');
}


function limpiar_campos(campos) {
    $(campos).val('');
}

function habilitar_campos(campos) {
    $(campos).prop('disabled', false);
}

function deshabilitar_campos(campos) {
    $(campos).prop('disabled', true);
    // $(campos).attr('disabled', 'disabled');
}
function deshabilitar_campos2(campos) {
    $(campos).prop('enabled', true);
    // $(campos).attr('disabled', 'disabled');
}

function mostrar_html(identificadorhtml) {
    $(identificadorhtml).attr('style', 'display:auto');
    // $(identificadorhtml).css('display', 'auto');
}

function ocultar_html(identificadorhtml) {
    $(identificadorhtml).attr('style', 'display:none');
    // $(identificadorhtml).css('display', 'none');
}
function ocultar_bottom(identificadorhtml) {
    $(identificadorhtml).css('display', 'none');

}
function ocultar_tablas(identificadorhtml, id_radio1, id_radio2, id_div_form) {
    $(identificadorhtml).css('display', 'none');
    $(id_radio1).removeClass('btn btn-primary');
    $(id_radio1).addClass('btn');
    $(id_radio2).removeClass('btn btn-primary');
    $(id_radio2).addClass('btn');
    $(id_div_form).css('display', 'none');

}
function limpiar_nota() {
    $('#id_cancelar_nota').on('click', function (e) {
        limpiar_campos('#id_descripcion');
    });
}
function radio_button() {

    $('div.btn-group button').on('click', function (e) {
        e.preventDefault();
        //console.log($(this).parents('div').attr('id'));
        if ($(this).attr('id') == 'id_button_cedula') {
            $(this).addClass('btn btn-primary');
            $('#id_button_nombres').removeClass('btn btn-primary');
            $('#id_button_nombres').addClass('btn');
            $('#id_div_form_buscar').attr('style', 'display:auto; margin-top:20px');
            $('#id_div_busqueda_cedula').attr('style', 'display:inline-block');
            $('#id_div_mensaje').attr('style', 'display:none');
            $('#id_div_busqueda_nombres').attr('style', 'display:none');
            limpiar_campos('#id_query_nombres, #id_query_apellidos');
        }
        if ($(this).attr('id') == 'id_button_nombres') {
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

function radio_button_hombres() {

    $('div.btn-group button').on('click', function (e) {
        e.preventDefault();
        //console.log($(this).parents('div').attr('id'));
        if ($(this).attr('id') == 'id_button_cedula_h') {
            $(this).addClass('btn btn-primary');
            $('#id_button_nombres_h').removeClass('btn btn-primary');
            $('#id_button_nombres_h').addClass('btn');
            $('#id_div_form_buscar_h').attr('style', 'display:auto; margin-top:20px');
            $('#id_div_busqueda_cedula_h').attr('style', 'display:inline-block');
            $('#id_div_mensaje_h').attr('style', 'display:none');
            $('#id_div_busqueda_nombres_h').attr('style', 'display:none');
            limpiar_campos('#id_query_nombres_h, #id_query_apellidos_h');
        }
        if ($(this).attr('id') == 'id_button_nombres_h') {
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
function radio_button_mujeres() {

    $('div.btn-group button').on('click', function (e) {
        e.preventDefault();
        //console.log($(this).parents('div').attr('id'));
        if ($(this).attr('id') == 'id_button_cedula_m') {
            $(this).addClass('btn btn-primary');
            $('#id_button_nombres_m').removeClass('btn btn-primary');
            $('#id_button_nombres_m').addClass('btn');
            $('#id_div_form_buscar_m').attr('style', 'display:auto; margin-top:20px');
            $('#id_div_busqueda_cedula_m').attr('style', 'display:inline-block');
            $('#id_div_mensaje_m').attr('style', 'display:none');
            $('#id_div_busqueda_nombres_m').attr('style', 'display:none');
            limpiar_campos('#id_query_nombres_m, #id_query_apellidos_m');
        }
        if ($(this).attr('id') == 'id_button_nombres_m') {
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

function radio_button_sacerdotes() {

    $('div.btn-group button').on('click', function (e) {
        e.preventDefault();
        console.log($(this).parents('div').attr('id'));
        if ($(this).attr('id') == 'id_button_cedula_s') {
            $(this).addClass('btn btn-primary');
            $('#id_button_nombres_s').removeClass('btn btn-primary');
            $('#id_button_nombres_s').addClass('btn');
            $('#id_div_form_buscar_s').attr('style', 'display:auto; margin-top:20px');
            $('#id_div_busqueda_cedula_s').attr('style', 'display:inline-block');
            $('#id_div_mensaje_sacerdote').attr('style', 'display:none');
            $('#id_div_busqueda_nombres_s').attr('style', 'display:none');
            limpiar_campos('#id_query_nombres_s, #id_query_apellidos_s');
        }
        if ($(this).attr('id') == 'id_button_nombres_s') {
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

function ocultar_tablas_aceptar(id_modal) {
    $(id_modal + ' #id_aceptar').on('click', function (e) {
        console.log('estoy en clic aceptar')
        ocultar_tablas('#id_table_busqueda_usuarios', '#id_button_cedula', '#id_button_nombres', '#id_div_form_buscar');
        ocultar_bottom('.bottom');
        ocultar_tablas('#id_table_busqueda_hombres', '#id_button_cedula_h', '#id_button_nombres_h', '#id_div_form_buscar_h');
        ocultar_bottom('.bottom');
        ocultar_tablas('#id_table_busqueda_mujeres', '#id_button_cedula_m', '#id_button_nombres_m', '#id_div_form_buscar_m');
        ocultar_bottom('.bottom');
        ocultar_tablas('#id_table_busqueda_sacerdotes', '#id_button_cedula_s', '#id_button_nombres_s', '#id_div_form_buscar_s');
        ocultar_bottom('.bottom');
        limpiar_campos('#id_query_nombres_s, #id_query_apellidos_s', '#id_query_cedula_s');
        limpiar_campos('#id_query_nombres_h, #id_query_apellidos_h', '#id_query_cedula_h');
        limpiar_campos('#id_query_nombres_m, #id_query_apellidos_m', '#id_query_cedula_m');
        limpiar_campos('#id_query_nombres, #id_query_apellidos', '#id_query_cedula');
    });
}


//Muestra una tabla en un modal con los datos de feligreses después de una búsqueda
function cargar_tabla_usuarios_en_modal() {
    $('#id_form_busqueda').on('submit', function (e) {
        e.preventDefault();
        var url = '/api/usuario/';
        var nombres = $('#id_query_nombres').val();
        var apellidos = $('#id_query_apellidos').val();
        var cedula = $('#id_query_cedula').val();
        var id = $('#id_hidden').val();
        mostrar_html("#id_table_busqueda_usuarios");
        var ctx = {'nombres': nombres, 'apellidos': apellidos, 'cedula': cedula, 'id_perfil': id};
        var columnas = [
            {"sType": "html", "mData": "full_name", "bSortable": true},
            {"mData": "fecha_nacimiento", "bSortable": true},
            {"mData": "lugar_nacimiento", "bSortable": true},
            {"mData": "dni", "bSortable": true }
        ];
        $.get(url, ctx, function (data) {
            console.log(data.bandera);
            tablas_busqueda_ajax("#id_table_busqueda_usuarios", columnas, data.perfiles);
            map = almacenar_busqueda_en_map(data.perfiles);
            devolver_campos_a_sacramento(map, '#id_administrador');
            devolver_campos_a_sacramento(map, '#id_bautizado');
            devolver_campos_a_sacramento(map, '#id_feligres');
            devolver_campos_a_sacramento(map, '#id_confirmado');
            devolver_campos_a_secretaria(map, '#id_persona');
        });
    });
}

function cargar_tabla_hombres_en_modal() {
    $('#id_form_busqueda_h').on('submit', function (e) {
        e.preventDefault();
        var url = '/api/hombres/';
        var nombres = $('#id_query_nombres_h').val();
        var apellidos = $('#id_query_apellidos_h').val();
        var cedula = $('#id_query_cedula_h').val();
        var id = $('#id_hidden').val();
        mostrar_html("#id_table_busqueda_hombres");
        var ctx = {'nombres': nombres, 'apellidos': apellidos, 'cedula': cedula, 'id_perfil': id};
        var columnas = [
            {"sType": "html", "mData": "full_name", "bSortable": true},
            {"mData": "fecha_nacimiento", "bSortable": true},
            {"mData": "lugar_nacimiento", "bSortable": true},
            {"mData": "dni", "bSortable": true }
        ];
        $.get(url, ctx, function (data) {
            console.log(data.bandera);
            tablas_busqueda_ajax("#id_table_busqueda_hombres", columnas, data.perfiles);
            map = almacenar_busqueda_en_map(data.perfiles);
            devolver_campos_de_lista(map, '#id_padre', '#id_madre');
            devolver_campos_de_lista(map, '#id_novio', '#id_novia');

        });
    });
}
function cargar_tabla_mujeres_en_modal() {
    $('#id_form_busqueda_m').on('submit', function (e) {
        e.preventDefault();
        var url = '/api/mujeres/';
        var nombres = $('#id_query_nombres_m').val();
        var apellidos = $('#id_query_apellidos_m').val();
        var cedula = $('#id_query_cedula_m').val();
        var id = $('#id_hidden').val();
        mostrar_html("#id_table_busqueda_mujeres");
        var ctx = {'nombres': nombres, 'apellidos': apellidos, 'cedula': cedula, 'id_perfil': id};
        var columnas = [
            {"sType": "html", "mData": "full_name", "bSortable": true},
            {"mData": "fecha_nacimiento", "bSortable": true},
            {"mData": "lugar_nacimiento", "bSortable": true},
            {"mData": "dni", "bSortable": true }
        ];
        $.get(url, ctx, function (data) {
            console.log(data.bandera);
            tablas_busqueda_ajax("#id_table_busqueda_mujeres", columnas, data.perfiles);
            map = almacenar_busqueda_en_map(data.perfiles);
            devolver_campos_de_lista(map, '#id_padre', '#id_madre');
            devolver_campos_de_lista(map, '#id_novio', '#id_novia');

        });
    });
}


function cargar_tabla_sacerdotes_en_modal() {
    $('#id_form_busqueda_sacerdotes').on('submit', function (e) {
        e.preventDefault();
        var url = '/api/sacerdote/';
        var nombres = $('#id_query_nombres_s').val();
        var apellidos = $('#id_query_apellidos_s').val();
        var cedula = $('#id_query_cedula_s').val();
        // var id= $('#id_hiddens').val();
        mostrar_html("#id_table_busqueda_sacerdotes");
        var ctx = {'nombres': nombres, 'apellidos': apellidos, 'cedula': cedula};
        var columnas = [
            {"sType": "html", "mData": "full_name", "bSortable": true},
            {"mData": "fecha_nacimiento", "bSortable": true},
            {"mData": "lugar_nacimiento", "bSortable": true},
            {"mData": "dni", "bSortable": true }
        ];
        $.get(url, ctx, function (data) {
            tablas_busqueda_ajax("#id_table_busqueda_sacerdotes", columnas, data.perfiles);
            map2 = almacenar_busqueda_en_map(data.perfiles);
            devolver_campos_a_sacerdote(map2, '#id_celebrante');

        });
    });
}


function almacenar_busqueda_en_map(lista) {
    var map = {};
    $.each(lista, function (index, element) {
        map[element.id] = element;
    });
    return map;
}


// Funcion para buscar y asignar usuarios a Matrimonio 
function devolver_campos_de_lista(map, id_male, id_female) {
    console.log('ejecutando: devolver campos de lista');
    console.log(map);
    $('tbody td a.id_click').on('click', function (e) {
        console.log('estoy aqui');
        e.preventDefault();
        $("#id_buscar_mujeres").modal('hide');
        $("#id_buscar_hombres").modal('hide');
        var id = $(this).parents('tr').attr('id');
        console.log('id: ' + id);
        var objeto = map[id];
        console.log('objeto prueba: ' + objeto);
        if (objeto.sexo == 'M') {
            $(id_male + ' option').remove();
            $(id_male).append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
            limpiar_campos('#id_query_nombres, #id_query_apellidos', '#id_query_cedula');
            limpiar_campos('#id_query_nombres_h, #id_query_apellidos_h', '#id_query_cedula_h');
            limpiar_campos('#id_query_nombres_m, #id_query_apellidos_m', '#id_query_cedula_m');
            ocultar_tablas('#id_table_busqueda_usuarios', '#id_button_cedula', '#id_button_nombres', '#id_div_form_buscar');
            ocultar_bottom('.bottom');
            ocultar_tablas('#id_table_busqueda_hombres', '#id_button_cedula_h', '#id_button_nombres_h', '#id_div_form_buscar_h');
            ocultar_bottom('.bottom');
            ocultar_tablas('#id_table_busqueda_mujeres', '#id_button_cedula_m', '#id_button_nombres_m', '#id_div_form_buscar_m');
            ocultar_bottom('.bottom');

        }
        if (objeto.sexo == 'F') {
            $(id_female + ' option').remove();
            $(id_female).append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
            limpiar_campos('#id_query_nombres, #id_query_apellidos', '#id_query_cedula');
            limpiar_campos('#id_query_nombres_h, #id_query_apellidos_h', '#id_query_cedula_h');
            limpiar_campos('#id_query_nombres_m, #id_query_apellidos_m', '#id_query_cedula_m');
            ocultar_tablas('#id_table_busqueda_usuarios', '#id_button_cedula', '#id_button_nombres', '#id_div_form_buscar');
            ocultar_bottom('.bottom');
            ocultar_tablas('#id_table_busqueda_hombres', '#id_button_cedula_h', '#id_button_nombres_h', '#id_div_form_buscar_h');
            ocultar_bottom('.bottom');
            ocultar_tablas('#id_table_busqueda_mujeres', '#id_button_cedula_m', '#id_button_nombres_m', '#id_div_form_buscar_m');
            ocultar_bottom('.bottom');

        }
    });
}


function prueba2(id) {
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
    if (objeto.sexo == 'M') {
        $('#id_padre option').remove();
        $('#id_padre').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        $('#id_novio option').remove();
        $('#id_novio').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        $('#id_bautizado option').remove();
        $('#id_bautizado').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        $('#id_feligres option').remove();
        $('#id_feligres').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        $('#id_confirmado option').remove();
        $('#id_confirmado').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        $('#id_persona option').remove();
        $('#id_persona').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        $('#id_administrador option').remove();
        $('#id_administrador').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        limpiar_campos('#id_query_nombres, #id_query_apellidos', '#id_query_cedula');
        limpiar_campos('#id_query_nombres_h, #id_query_apellidos_h', '#id_query_cedula_h');
        limpiar_campos('#id_query_nombres_m, #id_query_apellidos_m', '#id_query_cedula_m');
        ocultar_tablas('#id_table_busqueda_usuarios', '#id_button_cedula', '#id_button_nombres', '#id_div_form_buscar');
        ocultar_bottom('.bottom');
        ocultar_tablas('#id_table_busqueda_hombres', '#id_button_cedula_h', '#id_button_nombres_h', '#id_div_form_buscar_h');
        ocultar_bottom('.bottom');
        ocultar_tablas('#id_table_busqueda_mujeres', '#id_button_cedula_m', '#id_button_nombres_m', '#id_div_form_buscar_m');
        ocultar_bottom('.bottom');

    }
    if (objeto.sexo == 'F') {
        $('#id_madre option').remove();
        $('#id_madre').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        $('#id_novia option').remove();
        $('#id_novia').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        $('#id_bautizado option').remove();
        $('#id_bautizado').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        $('#id_confirmado option').remove();
        $('#id_confirmado').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        $('#id_persona option').remove();
        $('#id_persona').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        $('#id_feligres option').remove();
        $('#id_feligres').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        $('#id_administrador option').remove();
        $('#id_administrador').append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');
        limpiar_campos('#id_query_nombres, #id_query_apellidos', '#id_query_cedula');
        limpiar_campos('#id_query_nombres_h, #id_query_apellidos_h', '#id_query_cedula_h');
        limpiar_campos('#id_query_nombres_m, #id_query_apellidos_m', '#id_query_cedula_m');
        ocultar_tablas('#id_table_busqueda_usuarios', '#id_button_cedula', '#id_button_nombres', '#id_div_form_buscar');
        ocultar_bottom('.bottom');
        ocultar_tablas('#id_table_busqueda_hombres', '#id_button_cedula_h', '#id_button_nombres_h', '#id_div_form_buscar_h');
        ocultar_bottom('.bottom');
        ocultar_tablas('#id_table_busqueda_mujeres', '#id_button_cedula_m', '#id_button_nombres_m', '#id_div_form_buscar_m');
        ocultar_bottom('.bottom');
    }


}

function prueba3(id) {
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
    $('#id_celebrante').append('<option value=""> -- Seleccione --</option><option value=' + objeto1.id + ' selected>' + objeto1.full_name + '</option>');
    limpiar_campos('#id_query_nombres_s, #id_query_apellidos_s', '#id_query_cedula_s');
    ocultar_tablas('#id_table_busqueda_sacerdotes', '#id_button_cedula_s', '#id_button_nombres_s', '#id_div_form_buscar_s');
    ocultar_bottom('.bottom');


}


function prueba(nombre) {
    console.log('ejecutando prueba');
    console.log('ejecutando prueba : ' + nombre);
    //$("#id_buscar_padre").modal('hide');
}


function devolver_campos_a_sacerdote(map, id_sacerdote) {
    $('tbody td a.id_click').on('click', function (e) {
        e.preventDefault();
        $("#id_buscar_sacerdotes").modal('hide');
        limpiar_campos('#id_query_nombres_s, #id_query_apellidos_s', '#id_query_cedula_s');
        var id = $(this).parents('tr').attr('id');
        var objeto = map2[id];
        $(id_sacerdote + ' option').remove();
        $(id_sacerdote).append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>')
        ocultar_tablas('#id_table_busqueda_sacerdotes', '#id_button_cedula_s', '#id_button_nombres_s', '#id_div_form_buscar_s');
        ocultar_bottom('.bottom');

    });
}

function devolver_campos_a_secretaria(map, id_persona) {
    $('a.id_click').on('click', function (e) {
        e.preventDefault();
        $("#id_buscar_secretaria").modal('hide');
        var id = $(this).parents('tr').attr('id');
        var objeto = map[id];
        $(id_persona + ' option').remove();
        $(id_persona).append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>')
        limpiar_campos('#id_query_nombres, #id_query_apellidos', '#id_query_cedula');
        ocultar_tablas('#id_table_busqueda_usuarios', '#id_button_cedula', '#id_button_nombres', '#id_div_form_buscar');
        ocultar_bottom('.bottom');
    });
}


// Funcion para buscar y asignar usuarios a Bautismo,Feligres,
// Confirmacion
function devolver_campos_a_sacramento(map, id_feligres) {
    $('a.id_click').on('click', function (e) {
        // alert('estoy aqui');
        e.preventDefault();
        $("#id_buscar_feligreses").modal('hide');
        var id = $(this).parents('tr').attr('id');
        var objeto = map[id];
        $(id_feligres + ' option').remove();
        $(id_feligres).append('<option value=""> -- Seleccione --</option><option value=' + objeto.id + ' selected>' + objeto.full_name + '</option>');

    });
}


function asignar_padre() {
    $('#id_form_padre').on('submit', function (e) {
        e.preventDefault();
        //obtener id del feligres
        //obtener id del padre
        var idfeligres = $('#id_perfil').val();
        var idpadre = $('#id_padre').val();
        console.log('padre' + idpadre);
        console.log('feligres' + idfeligres);
        var ctx = {'idfeligres': idfeligres, 'idpadre': idpadre};
        var url = '/api/asignarpadre/';
        $.post(url, ctx, function (data) {
            if (data.bandera == true) {
                console.log(data.bandera);
                $(location).attr('href', '/usuario/');
            } else {
                console.log(data.bandera);
            }
        });

    });
}

function cancelar_modal() {
    var cancelar = $('.cancelar-modal').on('click', function (e) {
        e.preventDefault();
        //limpiar_campos('#id_first_name, #id_last_name, #id_email, #id_nacionalidad, #id_fecha_nacimiento, #id_dni, #id_lugar_nacimiento, #id_estado_civil, #id_profesion, #id_sexo');
        limpiar_campos('#id_form_crear_padre :input');
        limpiar_campos('#id_form_crear_madre :input');
        limpiar_campos('#id_form_crear_secretaria :input');
    });
}

function crear_nota_marginal(id_form, id_modal, url_rest) {
    $(id_form).on('submit', function (e) {
        $(id_form + ' #id_guardar').append("<i id='id_spinner' class='icon-refresh icon-spin'></i> ");
        e.preventDefault();
        var id = $('#id_hidden').val();
        var url = url_rest;
        var json = $(this).serialize() + "&id=" + id + "";
        $.post(url, json, function (data) {
            if (data.respuesta) {
                $(id_modal).modal('hide');
                limpiar_campos('#id_descripcion');
                $('tbody tr').remove();
                $.each(data.tabla, function (index, element) {
                    $('tbody').append(element.tabla);
                    habilitar_campos('#id_href');
                });
                $('#id_spinner').remove();
            } else {
                var mensaje = '<div class="alert alert-error">' +
                    '<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>' +
                    '<img src="/static/img/error.png" alt=""> Los datos del formulario son incorrectos </div>';
                $('#id_mensaje_nota').html(mensaje);
                $.each(data.errores_nota, function (index, element) {
                    var mensajes_error = '<span>' + element + '</span>';
                    $(id_form + " #id_errors_" + index).append(mensajes_error);
                });
                $('#id_spinner').remove();
            }
        });
    })
}
// Función para crear una Iglesia via Ajax
function crear_iglesia(identificador) {
    $(identificador).on('submit', function (e) {
        $('span').remove();
        $('.alert').remove();
        $(identificador + ' #id_guardar').append("<i id='id_spinner' class='icon-refresh icon-spin'></i> ");
        e.preventDefault();
        // Quita el elemento seleccionado por defecto
        $('#id_iglesia option:selected').removeAttr("selected");
        var html_inicial = $('#id_iglesia').html();
        var url = "/api/crear/iglesia/";
        var json = $(this).serialize();

        $.post(url, json, function (data) {
            if (!data.respuesta) {
                var error = '<div class="alert alert-error">' +
                    '<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>' +
                    '<img src="/static/img/error.png" alt=""> Los datos del formulario son incorrectos </div>';

                $(identificador + ' .modal-header').append(error);

                $.each(data.errores, function (index, element) {
                    var mensajes_error = '<span class="errors">' + element + '</span>';
                    $(identificador + " #id_errors_" + index).append(mensajes_error);
                });
                $('#id_spinner').remove();
            } else {
                $('#id_iglesia').html('<option value="' + data.id + '" selected="selected">' + data.nombre + '</option>' + html_inicial);
                $(".modal").modal('hide');
                limpiar_campos('#id_crear_iglesia :input');
                $('#id_spinner').remove();
            }
        });

    });
}

// Función para crear un Libro de cualquier tipo de sacramento via Ajax
function crear_libro(identificador) {
    $(identificador).on('submit', function (e) {
        $('span').remove();
        $('.alert').remove();
        $(identificador + ' #id_guardar').append("<i id='id_spinner' class='icon-refresh icon-spin'></i> ");
        e.preventDefault();
        // Quita el elemento seleccionado por defecto
        $('#id_libro option:selected').removeAttr("selected");
        var html_inicial = $('#id_libro').html();
        var url = "/api/crear/libro/";
        var json = $(this).serialize() + '&tipo_libro=' + $('#id_hidden_sacramento').val();
        console.log(json);

        $.post(url, json, function (data) {
            if (!data.respuesta) {
                var error = '<div class="alert alert-error">' +
                    '<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>' +
                    '<img src="/static/img/error.png" alt=""> Los datos del formulario son incorrectos </div>';
                $(identificador + ' .modal-header').append(error);
                $.each(data.errores, function (index, element) {
                    var mensajes_error = '<span class="errors">' + element + '</span>';
                    $(identificador + " #id_errors_" + index).append(mensajes_error);
                });
                $(identificador + ' #id_spinner').remove();
            } else {
                $('#id_libro').html('<option value="' + data.id + '" selected="selected">' + data.nombre + '</option>' + html_inicial);
                $(".modal").modal('hide');
                limpiar_campos('#id_crear_libro :input');
                $(identificador + ' #id_spinner').remove();
            }
        });

    });
}


// Función para crear un Libro de cualquier tipo de sacramento via Ajax
function crear_libro_sacramental(identificador) {
    $(identificador).on('submit', function (e) {
        $('span').remove();
        $('.alert').remove();
        $(identificador + ' #id_guardar').append("<i id='id_spinner' class='icon-refresh icon-spin'></i> ");
        e.preventDefault();
        var url = "/api/crear/libro/";
        var json = $(this).serialize();
        console.log(json);
        $.post(url, json, function (data) {
            if (!data.respuesta) {
                var error = '<div class="alert alert-error">' +
                    '<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>' +
                    '<img src="/static/img/error.png" alt=""> Los datos del formulario son incorrectos </div>';
                $('#errores').append(error);
                $.each(data.errores, function (index, element) {
                    var mensajes_error = '<span class="errors">' + element + '</span>';
                    $(identificador + " #id_errors_" + index).append(mensajes_error);
                });
                $(identificador + ' #id_spinner').remove();
            } else {
                sacramento = $(identificador + ' #id_tipo_libro').val();
                console.log(sacramento)
                /*$(identificador).remove();*/
                switch (sacramento) {
                    case 'bautismo':
                        $('#' + sacramento).html('<div><strong>Libro de Bautismos</strong><span class="pull-right">100%</span><div class="progress"><div class="bar bar-success" style="width: 100%;"></div></div></div>');
                        break;
                    case 'eucaristia':
                        $('#' + sacramento).html('<div><strong>Libro de Primeras Comuniones</strong><span class="pull-right">100%</span><div class="progress"><div class="bar bar-success" style="width: 100%;"></div></div></div>');
                        break;
                    case 'confirmacion':
                        $('#' + sacramento).html('<div><strong>Libro de Confirmaciones</strong><span class="pull-right">100%</span><div class="progress"><div class="bar bar-success" style="width: 100%;"></div></div></div>');
                        break;
                    case 'matrimonio':
                        $('#' + sacramento).html('<div><strong>Libro de Matrimonios</strong><span class="pull-right">100%</span><div class="progress"><div class="bar bar-success" style="width: 100%;"></div></div></div>');
                        break;
                }
            }
        });

    });
}

//  Esta función llama a un modal para crear un padre para un feligrés
function crear_feligres(identificador, idpadre, idmodal) {
    $(identificador).on('submit', function (e) {
        $('span').remove();
        $('.alert').remove();
        $(identificador + ' #id_guardar').append(" <i id='id_spinner' class='icon-refresh icon-spin'></i> ");
        e.preventDefault();
        var url = '/api/crear/padre/';
        var json = $(this).serialize();
        $.post(url, json, function (data) {
            if (!data.respuesta) {
                var mensaje = '<div class="alert alert-error">' +
                    '<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>' +
                    '<img src="/static/img/error.png" alt=""> Los datos del formulario son incorrectos </div>';
                $(identificador + ' .modal-header').append(mensaje);
                $.each(data.errores_usuario, function (index, element) {
                    var mensajes_error = '<span class="errors">' + element + '</span>';
                    $(identificador + " #id_errors_" + index).append(mensajes_error);
                });
                $.each(data.errores_perfil, function (index, element) {
                    var mensajes_error = '<span class="errors">' + element + '</span>';
                    $(identificador + " #id_errors_" + index).append(mensajes_error);
                });

                if (data.messages_error) {
                    var mensaje = '<div class="alert alert-error">' +
                        '<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>' +
                        '<img src="/static/img/error.png" alt=""> ' + data.messages_error + ' </div>';
                    $(identificador + ' .modal-header').append(mensaje);
                }
                $('#id_spinner').remove();

            } else {
                $(idpadre).html('<option value="">-- Seleccione --</option><option value="' + data.id + '" selected>' + data.full_name + '</option>');
                $(idmodal).modal('hide');
                limpiar_campos(identificador + ' :input');
                $('#id_spinner').remove();
            }
        });
    });
}

//  Esta función llama a un modal para crear un sacerdote
function crear_sacerdote(identificador) {
    $(identificador).on('submit', function (e) {
        $('span').remove();
        $('.alert').remove();
        $(identificador + ' #id_guardar').append("<i id='id_spinner' class='icon-refresh icon-spin'></i> ");
        e.preventDefault();
        var url = '/api/crear/sacerdote/';
        var json = $(this).serialize();
        $.post(url, json, function (data) {
            if (!data.respuesta) {
                var error = '<div class="alert alert-error">' +
                    '<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>' +
                    '<img src="/static/img/error.png" alt=""> Los datos del formulario son incorrectos </div>';

                $(identificador + ' .modal-header').append(error);

                $.each(data.errores_usuario, function (index, element) {
                    var mensajes_error = '<span class="errors">' + element + '</span>';
                    $(identificador + " #id_errors_" + index).append(mensajes_error);
                });

                $.each(data.errores_perfil, function (index, element) {
                    var mensajes_error = '<span class="errors">' + element + '</span>';
                    $(identificador + " #id_errors_" + index).append(mensajes_error);
                });
                $('#id_spinner').remove();

            } else {
                $('#id_celebrante').html('<option value="">-- Seleccione --</option><option value="' + data.id + '" selected>' + data.full_name + '</option>');
                $('.modal').modal('hide');
                limpiar_campos(id_crear_sacerdote + ' :input');
                $('#id_spinner').remove();
            }

        });
    });
}


//  Esta función llama a un modal para crear una secretaria
function crear_secretaria(identificador, idsecretaria, idmodal) {
    $(identificador).on('submit', function (e) {
        $('span').remove();
        $('.alert').remove();
        $(identificador + ' #id_guardar').append("<i id='id_spinner' class='icon-refresh icon-spin'></i> ");
        e.preventDefault();
        var url = '/api/crear/secretaria/';
        var json = $(this).serialize();
        $.post(url, json, function (data) {
            if (!data.respuesta) {
                var mensaje = '<div class="alert alert-error">' +
                    '<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>' +
                    '<img src="/static/img/error.png" alt=""> Los datos del formulario son incorrectos </div>';
                $(identificador + ' .modal-header').append(mensaje);
                $.each(data.errores_usuario, function (index, element) {
                    var mensajes_error = '<span class="errors">' + element + '</span>';
                    $(identificador + " #id_errors_" + index).append(mensajes_error);
                });
                $.each(data.errores_perfil, function (index, element) {
                    var mensajes_error = '<span class="errors">' + element + '</span>';
                    $(identificador + " #id_errors_" + index).append(mensajes_error);
                });
                $('#id_spinner').remove();
            } else {
                $(idsecretaria).html('<option value="">-- Seleccione --</option><option value="' + data.id + '" selected>' + data.full_name + '</option>');
                $(idmodal).modal('hide');
                limpiar_campos('#id_form_crear_secretaria :input');
                $('#id_spinner').remove();
            }

        });
    });
}


//Permite crear via ajax una direccion
function crear_direccion(identificador) {
    $(identificador).on('submit', function (e) {
        e.preventDefault();
        $('#id_guardar').append("<i id='id_spinner' class='icon-refresh icon-spin'></i> ");
        var url = '/crear/ciudades/direccion/'
        var json = $(this).serialize()
        $.post(url, json, function (data) {
            if (data.respuesta) {
                $('#id_modal_direccion').modal('hide');
                $('#id_spinner').remove();
            } else {
                console.log('Existen errores');
                console.log(data.errores);
                $('#id_spinner').remove();
            }
        });
    })
}

// Permite elegir los cantones de acuerdo a sus respectivas provincias
function seleccionar_cantones(identificador) {
    $(identificador).on('change', function (e) {
        e.preventDefault();
        $('#id_canton option').remove();
        $('#id_canton').prop('disabled', true);
        $('#id_parroquia option').remove();
        $('#id_parroquia').append('<option>-- Seleccione --</option>')
        $('#id_parroquia').prop('disabled', true);

        var url = '/api/ciudades/select/';
        var provincia = $(identificador + ' option:selected').val();
        var ctx = {'provincia': provincia}
        $.get(url, ctx, function (data) {
            $.each(data.cantones, function (index, element) {
                $('#id_canton').prop('disabled', false);
                $('#id_canton').append(element.option)
            });
        });
    })
}

// Permite elegir las parroquias de acuerdo a sus respectivos cantones
function seleccionar_parroquias(identificador) {
    $(identificador).on('change', function (e) {
        $('#id_parroquia option').remove();
        $('#id_parroquia').prop('disabled', true);
        e.preventDefault();
        var url = '/api/ciudades/select/';
        var canton = $(identificador + ' option:selected').val();
        var ctx = {'canton': canton}
        $.get(url, ctx, function (data) {
            $.each(data.parroquias, function (index, element) {
                $('#id_parroquia').prop('disabled', false);
                $('#id_parroquia').append(element.option)
            });
        });
    })
}

// Permite verificar si un select tiene algun valor seleccionado
function verificar_select_seleccionado() {
    if ($("#id_provincia option:selected").text() != '-- Seleccione --') {
        $('#id_canton').prop('disabled', false);
        $('#id_parroquia').prop('disabled', false);
    }
}

            $('#id_fecha').val("");
            $('#id_fecha_final').val("");
            $('#id_hora').val("");
            $('#id_anio').val("");

function seleccionar_hora() {
    $('#id_tipo').on('change', function (e) {
        console.log('Change de tipo')
        if ($('#id_tipo option:selected').val() == 'h') {
            e.preventDefault();
            ($('#id_div_hora')).css('display', 'inline-block');
            ($('#id_div_anio')).css('display', 'none');
            $('#id_fecha').val("");
            ($('#id_div_fecha_inicial')).css('display', 'inline-block');
            ($('#id_div_fecha_final')).css('display', 'inline-block');
        } else if($('#id_tipo option:selected').val() == 'r') {
            ($('#id_div_hora')).css('display', 'none');
            ($('#id_div_anio')).css('display', 'none');
            $('#id_hora').val("");
            $('#id_anio').val("");
            ($('#id_div_fecha_inicial')).css('display', 'inline-block');
            ($('#id_div_fecha_final')).css('display', 'inline-block');
        } else if($('#id_tipo option:selected').val() == 'a'){
            ($('#id_div_hora')).css('display', 'none');
            ($('#id_div_fecha_inicial')).css('display', 'none');
            ($('#id_div_fecha_final')).css('display', 'none');
            $('#id_fecha').val("");
            $('#id_fecha_final').val("");
            $('#id_hora').val("");
            ($('#id_div_anio')).css('display', 'inline-block');
        } else if($('#id_tipo option:selected').val() == 'd') {
            ($('#id_div_fecha_inicial')).css('display', 'inline-block');
            ($('#id_div_fecha_final')).css('display', 'none');
            ($('#id_div_hora')).css('display', 'none');
            ($('#id_div_anio')).css('display', 'none');
            $('#id_fecha_final').val("");
            $('#id_hora').val("");
            $('#id_anio').val("");
        } else {
            ($('#id_div_fecha_inicial')).css('display', 'inline-block');
            ($('#id_div_fecha_final')).css('display', 'none');
            ($('#id_div_hora')).css('display', 'inline-block');
            ($('#id_div_anio')).css('display', 'none');
            $('#id_fecha_final').val("");
            $('#id_anio').val("");
        }


    });
}

function controles_sacramentos() {

    ($('#id_pagina').numeric());
    ($('#id_numero_acta').numeric());
    ($('#id_numero_libro').numeric());
    ($('#id_lugar_sacramento').alpha({allow: " "}));
    ($('#id_iglesia').alpha({allow: " "}));
    ($('#id_padrino').alpha({allow: " "}));
    ($('#id_madrina').alpha({allow: " "}));
    ($('#id_abuelo_paterno').alpha({allow: " "}));
    ($('#id_abuela_paterna').alpha({allow: " "}));
    ($('#id_abuelo_materno').alpha({allow: " "}));
    ($('#id_abuela_materna').alpha({allow: " "}));
    ($('#id_vecinos_paternos').alpha({allow: " "}));
    ($('#id_vecinos_maternos').alpha({allow: " "}));
    ($('#id_testigo_novio').alpha({allow: " "}));
    ($('#id_testigo_novia').alpha({allow: " "}));
    // para nota marginal
    ($('#id_descripcion').alpha({allow: " "}));

}

function controles_feligres() {

    ($('#id_first_name').alpha({allow: " "}));
    ($('#id_last_name').alpha({allow: " "}));
    ($('#id_profesion').alpha({allow: " "}));
    ($('#id_lugar_nacimiento').alpha({allow: " "}));
    ($('#id_celular').numeric());
}
function controles_intenciones() {
    ($('#id_intencion').alpha({allow: " "}));
    ($('#id_oferente').alpha({allow: " "}));
    ($('#id_ofrenda').numeric({allow: "."}));

}
function controles_reportes() {
    ($('#id_form_anio #id_anio').numeric());
}

function controles_provincias() {

    ($('#id_nombre').alpha({allow: " "}));
    ($('#id_abreviatura').numeric());
    // para campo name de grupos
    ($('#id_name').alpha({allow: " "}));
    // para parametriza diocesis
    ($('#id_diocesis').alpha({allow: " "}));
    ($('#id_obispo').alpha({allow: " "}));
    ($('#id_telefono').numeric());
    ($('#id_buscar_sacramentos').numeric());
}


function reporte_intenciones(){
        console.log('Change de tipo prueba')
        console.log($('#id_tipo option:selected').val());
        if ($('#id_tipo option:selected').val() == '') {
            ($('#id_div_hora')).css('display', 'none');
            ($('#id_div_anio')).css('display', 'none');
            ($('#id_div_fecha_inicial')).css('display', 'none');
            ($('#id_div_fecha_final')).css('display', 'none');
        } else if ($('#id_tipo option:selected').val() == 'h') {
            e.preventDefault();
            ($('#id_div_hora')).css('display', 'inline-block');
            ($('#id_div_anio')).css('display', 'none');
            ($('#id_div_fecha_inicial')).css('display', 'inline-block');
            ($('#id_div_fecha_final')).css('display', 'inline-block');
        } else if($('#id_tipo option:selected').val() == 'r') {
            ($('#id_div_hora')).css('display', 'none');
            ($('#id_div_anio')).css('display', 'none');
            ($('#id_div_fecha_inicial')).css('display', 'inline-block');
            ($('#id_div_fecha_final')).css('display', 'inline-block');
        } else if($('#id_tipo option:selected').val() == 'a'){
            ($('#id_div_hora')).css('display', 'none');
            ($('#id_div_fecha_inicial')).css('display', 'none');
            ($('#id_div_fecha_final')).css('display', 'none');
            ($('#id_div_anio')).css('display', 'inline-block');
        } else if($('#id_tipo option:selected').val() == 'd') {
            ($('#id_div_fecha_inicial')).css('display', 'inline-block');
            ($('#id_div_fecha_final')).css('display', 'none');
            ($('#id_div_hora')).css('display', 'none');
            ($('#id_div_anio')).css('display', 'none');
        } else {
            ($('#id_div_fecha_inicial')).css('display', 'inline-block');
            ($('#id_div_fecha_final')).css('display', 'none');
            ($('#id_div_hora')).css('display', 'inline-block');
            ($('#id_div_anio')).css('display', 'none');
        }
}

function asignar_email() {
    $('#id_form_email').on('submit', function (e) {
        e.preventDefault();
        var ctx = $(this).serialize()
        var url = '/api/crear/email/'
        $.post(url, ctx, function (data) {
            if (data.respuesta) {
                $('#id_modal_email').modal('hide');
            } else {
                console.log('hay errores')
                var mensaje = '<br/><div class="alert alert-error">' +
                    '<button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>' +
                    '<img src="/static/img/error.png" alt=""> El email ingresado no es válido </div>';
                $('.modal-header').append(mensaje);

                $.each(data.errores, function (index, element) {
                    var mensajes_error = '<span class="errors">' + element + '</span>';
                    $('#id_email' + " #id_errors_" + index).append(mensajes_error);
                });
            }
        });
    });
}

// Script para detectar el navegador que está utilizando el usuario
function detectar_navegador() {
    var BrowserDetect =
    {
        init: function () {
            this.browser = this.searchString(this.dataBrowser) || "Other";
            this.version = this.searchVersion(navigator.userAgent) || this.searchVersion(navigator.appVersion) || "Unknown";
        },

        searchString: function (data) {
            for (var i = 0; i < data.length; i++) {
                var dataString = data[i].string;
                this.versionSearchString = data[i].subString;

                if (dataString.indexOf(data[i].subString) != -1) {
                    return data[i].identity;
                }
            }
        },

        searchVersion: function (dataString) {
            var index = dataString.indexOf(this.versionSearchString);
            if (index == -1) return;
            return parseFloat(dataString.substring(index + this.versionSearchString.length + 1));
        },

        dataBrowser: [
            { string: navigator.userAgent, subString: "Chrome", identity: "Chrome" },
            { string: navigator.userAgent, subString: "MSIE", identity: "Explorer" },
            { string: navigator.userAgent, subString: "Firefox", identity: "Firefox" },
            { string: navigator.userAgent, subString: "Safari", identity: "Safari" },
            { string: navigator.userAgent, subString: "Opera", identity: "Opera" }
        ]

    };

    BrowserDetect.init();

    if (BrowserDetect.browser == "Explorer") {
        if (BrowserDetect.version < 9) {
            alert('Se recomienda utilizar Internet Explorer 9 o superior, Chrome, Firefox u Opera para el ingreso al sistema.');
        }
    }

    if (BrowserDetect.browser == "Safari") {
        alert('Se recomienda utilizar Chrome, Firefox u Opera para el ingreso al sistema');
    }

}



