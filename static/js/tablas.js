function modelo_tablas(valor){
	$(valor).dataTable({
		"fnDrawCallback": function(){
			$(valor).footable(
			{
				breakpoints: {
					phone: 320,
					tablet: 768
				}
			})
		},

		"sDom": "<'top' <'row-fluid' <'span5' l><'span5' f>>>t<'bottom' p>",
		"aLengthMenu": [[5, 10, 25, 50, 100, -1], [5, 10, 25, 50, 100, 'Todos']],
		"sPaginationType": "bootstrap",
		"iDisplayLength": 25,
		'bsort': true,
		"oLanguage": {
			"sInfo": "Mostrando _START_ a _END_ de _TOTAL_ elementos",
		//"sInfo": "Got a total of _TOTAL_ entries to show (_START_ to _END_)",
		"sInfoEmpty":"Mostrando 0 to 0 de 0 Elementos",
		"sLengthMenu": "Ver _MENU_ registros",
		"sSearch": "Buscar:",
		"sEmptyTable": "No existen datos disponibles en la tabla",
		"sInfoFiltered": " (Filtrado de _MAX_ Elementos)",
		"sZeroRecords": "No existen registros con ese criterio de búsqueda",
		"oPaginate": {
			"sFirst": "",
			"sLast": "",
			"sNext": "Siguiente",
			"sPrevious": "Anterior"}
		}
	});
}

function tablas_estilo_bootstrap(){
	// Agregar iconos para decir que una tabla se puede ordenar
	$('th').each(function(){ 
		if($(this).text() != ''){
			$(this).addClass('dropdown-toggle');
			$(this).attr('dropdown-toggle', 'dropdown');
			$(this).append('<span><img class="sorted" src="/static/img/black-unsorted.gif"></img></span>');
		}
	});

	$.fn.dataTableExt.oApi.fnPagingInfo = function ( oSettings )
	{
		return {
			"iStart":         oSettings._iDisplayStart,
			"iEnd":           oSettings.fnDisplayEnd(),
			"iLength":        oSettings._iDisplayLength,
			"iTotal":         oSettings.fnRecordsTotal(),
			"iFilteredTotal": oSettings.fnRecordsDisplay(),
			"iPage":          oSettings._iDisplayLength === -1 ?
			0 : Math.ceil( oSettings._iDisplayStart / oSettings._iDisplayLength ),
			"iTotalPages":    oSettings._iDisplayLength === -1 ?
			0 : Math.ceil( oSettings.fnRecordsDisplay() / oSettings._iDisplayLength )
		};
	}

	$.extend( $.fn.dataTableExt.oStdClasses, {
		"sSortAsc": "header headerSortDown",
		"sSortDesc": "header headerSortUp",
		"sSortable": "header",
	});

	/* Bootstrap style pagination control */
	$.extend( $.fn.dataTableExt.oPagination, {
		"bootstrap": {
			"fnInit": function( oSettings, nPaging, fnDraw ) {
				var oLang = oSettings.oLanguage.oPaginate;
				var fnClickHandler = function ( e ) {
					e.preventDefault();
					if ( oSettings.oApi._fnPageChange(oSettings, e.data.action) ) {
						fnDraw( oSettings );
					}
				};

				$(nPaging).addClass('pagination').append(
					'<ul>'+
					'<li class="prev disabled"><a href="#">&larr; '+oLang.sPrevious+'</a></li>'+
					'<li class="next disabled"><a href="#">'+oLang.sNext+' &rarr; </a></li>'+
					'</ul>'
					);
				var els = $('a', nPaging);
				$(els[0]).bind( 'click.DT', { action: "previous" }, fnClickHandler );
				$(els[1]).bind( 'click.DT', { action: "next" }, fnClickHandler );
			},

			"fnUpdate": function ( oSettings, fnDraw ) {
				var iListLength = 5;
				var oPaging = oSettings.oInstance.fnPagingInfo();
				var an = oSettings.aanFeatures.p;
				var i, j, sClass, iStart, iEnd, iHalf=Math.floor(iListLength/2);

				if ( oPaging.iTotalPages < iListLength) {
					iStart = 1;
					iEnd = oPaging.iTotalPages;
				}
				else if ( oPaging.iPage <= iHalf ) {
					iStart = 1;
					iEnd = iListLength;
				} else if ( oPaging.iPage >= (oPaging.iTotalPages-iHalf) ) {
					iStart = oPaging.iTotalPages - iListLength + 1;
					iEnd = oPaging.iTotalPages;
				} else {
					iStart = oPaging.iPage - iHalf + 1;
					iEnd = iStart + iListLength - 1;
				}

				for ( i=0, iLen=an.length ; i<iLen ; i++ ) {
                  // Remove the middle elements
                  $('li:gt(0)', an[i]).filter(':not(:last)').remove();

                  // Add the new list items and their event handlers
                  for ( j=iStart ; j<=iEnd ; j++ ) {
                  	sClass = (j==oPaging.iPage+1) ? 'class="active"' : '';
                  	$('<li '+sClass+'><a href="#">'+j+'</a></li>')
                  	.insertBefore( $('li:last', an[i])[0] )
                  	.bind('click', function (e) {
                  		e.preventDefault();
                  		oSettings._iDisplayStart = (parseInt($('a', this).text(),10)-1) * oPaging.iLength;
                  		fnDraw( oSettings );
                  	} );
                  }

                  // Add / remove disabled classes from the static elements
                  if ( oPaging.iPage === 0 ) {
                  	$('li:first', an[i]).addClass('disabled');
                  } else {
                  	$('li:first', an[i]).removeClass('disabled');
                  }

                  if ( oPaging.iPage === oPaging.iTotalPages-1 || oPaging.iTotalPages === 0 ) {
                  	$('li:last', an[i]).addClass('disabled');
                  } else {
                  	$('li:last', an[i]).removeClass('disabled');
                  }
              }
          }
      }
  } 


  );
}


function tablas_busqueda_ajax(identificador_tabla, columnas_tabla, datos){
	console.log('ejecutando: tablas');
	$(identificador_tabla).dataTable({
		"fnDrawCallback": function() {
			$(identificador_tabla).footable(
			{
				breakpoints: {
					phone: 320,
					tablet: 768
				}
			})
		},

		"sDom": "<'top't><'bottom'p><'clear'>",
		"sPaginationType": "bootstrap",
		"iDisplayLength": 10,
		"bPaginate": true,
		// "bInfo": true,
		"bSorted": true,
		// "bFilter": true,
		// "bLengthChange": true,
		// "aLengthMenu": [[2, 5, 10, -1], [2, 5, 10, "Todos"]],
		"aaData": datos,
		"bDestroy": true,
		"aoColumns" : columnas_tabla,
		"oLanguage": {
			"sInfo": "Mostrando _END_ de _TOTAL_  Elementos",
			"sLengthMenu": "Mostrar _MENU_ registros",
			"sSearch": "Filtrar:",
			"sEmptyTable": "No existen datos disponibles en la tabla",
			"sInfoFiltered": " (Filtrado de _MAX_ Elementos)",
			"sZeroRecords": "No existen registros con ese criterio de búsqueda",
			"oPaginate": {
				"sFirst": "",
				"sLast": "",
				"sNext": "Siguiente",
				"sPrevious": "Anterior"}
			}
		}); 
}

function tablas_busqueda_ajax_prueba(){
	var url = '/api/datatables/';
	var columnas = [
	{ 'sName':"user.first_name", "mData": "Nombres", "sWidth": "40px" }, //El sName es el nombre de la variable que va al servidor
	{ 'sName': "dni", "mData": "Dni", "sWidth": "25px"}
	]

	$('#id_data_tables').dataTable({
		"bProcessing": true,
		"bServerSide": true,
		"sAjaxSource": url,
		"sPaginationType": "bootstrap",
		"bPaginate": true,
		"bInfo": true,
        // "bSorted": true,
        // "bFilter": true,
        "bLengthChange": true,
        "aLengthMenu": [[2, 5, 10, -1], [2, 5, 10, "Todos"]],
		// "aaData": [{'Nombres': 'Jose', 'Dni': 222 }, {'Nombres': 'Luis', 'Dni': 11111}],
		"bDestroy": true,
		"aoColumns" : columnas,
		"oLanguage": {
			"sInfo": "Mostrando _END_ de _TOTAL_  Elementos",
			"sLengthMenu": "Mostrar _MENU_ registros",
			"sSearch": "Buscar:",
			"sEmptyTable": "No existen datos disponibles en la tabla",
			"sInfoFiltered": " (Total: _MAX_ elementos en la BD)",
			"sZeroRecords": "No existen registros con ese criterio de búsqueda",
			"oPaginate": {
				"sFirst": "",
				"sLast": "",
				"sNext": "Siguiente",
				"sPrevious": "Anterior"}
			}
		}); 
}

