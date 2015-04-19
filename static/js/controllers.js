var app = angular.module('app');

app.controller('menuControl', function ($scope) {

    $scope.aClick = function (event) {

        if ($(event.target).attr("class") == "accordion-toggle collapsed") {
            $(event.target).html('<span class="pull-right"><i class="icon-double-angle-down"></i></span>');
        } else {
            $(event.target).html('<span class="pull-right"><i class="icon-double-angle-up"></i></span>');
        }
    };
});

app.controller('catalogoControl', ['$scope', '$http', 'administrarCatalogos', 'constants' , function ($scope, $http, administrarCatalogos, constants) {
    $scope.alert = false;
    $scope.catalogos = [];
    $scope.estadosGenerales = [];
    $scope.catalogoActual = "";

    $scope.limpiarCampos = function() {
        $scope.id = "";
        $scope.codigo = "";
        $scope.nombre = "";
        $scope.descripcion = "";
        $scope.editable = false;
        $scope.padre = $scope.catalogos;
        $scope.estado = "";

        //limpiar errores
        $scope.limpiarErrores();
    };

    $scope.limpiarErrores = function(){
         $scope.errorCodigo = "";
    }


    $scope.submit = function () {
        $scope.limpiarErrores();
        var data = {
                "codigo": $scope.codigo,
                "nombre": $scope.nombre,
                "editable": $scope.editable,
                "estado": $scope.estado,
                "descripcion": $scope.descripcion
               };

        if( $scope.padre != null){
                 data["padre"] = $scope.padre.id;
            }

        if ($scope.id) {
            data["id"] = $scope.id;
            administrarCatalogos.updateCatalogo($scope.id, data)
                .success(function (data) {
                    console.log("catalogo actualizado correctamente");
                    $scope.alert = true;
                    $scope.status = constants.SUCCESS;
                    $scope.message = constants.UPDATE_SUCCESS;
                    $scope.reset = $scope.limpiarCampos();


                    administrarCatalogos.getCatalogos()
                        .success(function (data) {
                            $scope.catalogos = data;
                        })
                        .error(function (error) {

                        });
                })
                .error(function (errors) {
                    $scope.alert = true;
                    $scope.status = constants.ERROR;
                    $scope.message = constants.UPDATE_ERROR;
                    if(errors.codigo) $scope.errorCodigo = errors.codigo[0];
                    console.log(errors);
                });
        } else {
            administrarCatalogos.setCatalogo(data)
                .success(function (data) {
                    console.log("catalogo insertado correctamente");
                    $scope.alert = true;
                    $scope.status = constants.SUCCESS;
                    $scope.message = constants.CREATE_SUCCESS;
                    $scope.reset = $scope.limpiarCampos();

                    administrarCatalogos.getCatalogos()
                        .success(function (data) {
                            $scope.catalogos = data;
                        })
                        .error(function (error) {
                            $scope.status = 'Unable to load customer data: ' + error.message;
                        });
                })
                .error(function (errors) {
                    $scope.alert = true;
                    $scope.status = constants.ERROR;
                    $scope.message = constants.CREATE_ERROR;
                    if(errors.codigo) $scope.errorCodigo = errors.codigo[0];
                    console.log(errors);
                });
        }
    };

    administrarCatalogos.getItemsPorCatalogo(constants.CAT_ESTADOS_GENERALES)
        .success(function (data) {
            $scope.estadosGenerales = data;
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });

    administrarCatalogos.getCatalogos()
        .success(function (data) {
            $scope.catalogos = data;
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });

    $scope.MostrarInfoCatalogo = function (codigo) {

        $scope.codSelectedCatalogo = codigo;

        $scope.cat = $scope.catalogos.filter(function (el) {
            return el.codigo == codigo;
        });

        $scope.cat.forEach(function (c, posicion) {
            $scope.id = c.id;
            $scope.nombre = c.nombre;
            $scope.codigo = c.codigo;
            $scope.descripcion = c.descripcion;
            $scope.padre = c.padre;
            $scope.editable = c.editable;
            $scope.catalogos.forEach(function (ele, ident) {
                if (ele.id == c.padre) {
                    $scope.padre = $scope.catalogos[ident];
                }
            });

            $scope.estado = c.estado;

        });

        $scope.items = [];
        $http.get('/api-auth/item/?catalogo=' + codigo).
            success(function (data, status, headers, config) {
                $scope.items = data;
            }).
            error(function (data, status, headers, config) {
                console.log(data);
            });
    }

}]);

app.controller('itemControl', ['$scope', '$http', 'administrarCatalogos', 'administrarItems', 'constants', '$anchorScroll', '$location',
    function ($scope, $http, administrarCatalogos, administrarItems, constants, $anchorScroll, $location) {

    var idInfoItem = "idInfoItem";
    $scope.alert = false;
    $scope.catalogos = [];
    $scope.estadosGenerales = [];
    $scope.items = [];
    $scope.catalogoActual = "";
    $scope.itemActual = "";
    $scope.itemsPadre = [];

    $scope.limpiarCampos = function() {
        $scope.id = "";
        $scope.codigo = "";
        $scope.nombre = "";
        $scope.valor = "";
        $scope.descripcion = "";
        $scope.principal = false;
        $scope.estado = "";
        $scope.padre = $scope.itemsPadre;

        //limpiar errores
        $scope.limpiarErrores();
    };

    $scope.limpiarErrores = function(){
         $scope.errorCodigo = "";
    }

    $scope.nuevoItem = function(){
       $scope.limpiarCampos();
       $scope.crud = true;
    }

    administrarCatalogos.getItemsPorCatalogo(constants.CAT_ESTADOS_GENERALES)
        .success(function (data) {
            $scope.estadosGenerales = data;
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });

    administrarCatalogos.getCatalogos()
        .success(function (data) {
            $scope.catalogos = data;
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });

    $scope.CambiarPagina = function(pagina){
         $http.get(pagina).
            success(function (data, status, headers, config) {
                $scope.items = data.results;
                $scope.pageprevious = data.previous;
                $scope.pagenext = data.next;
                $scope.pagecount = data.count;
            }).
            error(function (data, status, headers, config) {
                console.log(data);
            });
    };

    $scope.getItemsPaginados = function(catalogo){
            administrarItems.getItemsPaginadosPorCatalogo(catalogo.codigo).
            success(function (data, status, headers, config) {
                $scope.items = data.results;
                $scope.pageprevious = data.previous;
                $scope.pagenext = data.next;
                $scope.pagecount = data.count;
                $scope.catalogoActual = catalogo;
                $scope.catalogo = $scope.catalogoActual.id;
                $scope.padreCodigo = $scope.catalogoActual.padreCodigo;
                $scope.reset = $scope.limpiarCampos();

                console.log('catalogo codigo: ' + catalogo);
                console.log('padre codigo: ' + $scope.padreCodigo);
                administrarCatalogos.getItemsPorCatalogo($scope.padreCodigo)
                    .success(function (data) {
                        $scope.itemsPadre = data;
                    })
                    .error(function (error) {
                        $scope.status = 'Unable to load customer data: ' + error.message;
                    });
            }).
            error(function (data, status, headers, config) {
                console.log(data);
            });
        };

    $scope.MostrarItemsDelCatalogo = function (catalogo) {
        $scope.getItemsPaginados(catalogo);
        $scope.crud = false;
        $scope.codSelectedCatalogo = catalogo.codigo;

    };

    $scope.CargarItem = function (id) {
        $scope.items.forEach(function (e, i) {
            if (e.id == id) {
                $scope.crud = true;
                $scope.id = e.id;
                $scope.catalogo = e.catalogo;
                $scope.codigo = e.codigo;
                $scope.nombre = e.nombre;
                $scope.valor = e.valor;
                $scope.descripcion = e.descripcion;
                $scope.principal = e.principal;
                $scope.estado = e.estado;
                $scope.itemsPadre.forEach(function (ele, ident) {
                    if (ele.id == e.padre) {
                        $scope.padre = $scope.itemsPadre[ident];
                    }
                });
            }
        });
        console.log(idInfoItem);
        //$location.hash(idInfoItem);
    };

    $scope.guardarItem = function () {

        $scope.limpiarErrores();

        var data = {
            "catalogo": $scope.catalogo,
            "nombre": $scope.nombre,
            "codigo": $scope.codigo,
            "valor": $scope.valor,
            "descripcion": $scope.descripcion,
            "principal": $scope.principal,
            "estado": $scope.estado
        };

        if( $scope.padre != null){
                 data["padre"] = $scope.padre.id;
            };

        if ($scope.id) {
            data["id"] = $scope.id;
            administrarItems.updateItem($scope.id, data).
                success(function (data, status, headers, config) {
                    console.log("Item Actualizado correctamente");
                    $scope.alert = true;
                    $scope.status = constants.SUCCESS;
                    $scope.message = constants.UPDATE_SUCCESS;
                    $scope.reset = $scope.limpiarCampos();
                    $scope.crud = false;
                    $scope.getItemsPaginados($scope.catalogoActual);

                    /*if ($location.hash() !== idInfoItem) {
                       $anchorScroll();
                    }*/

                    $anchorScroll();

                }).
                error(function (errors)
                {
                    console.log("Error al actualizar el item");
                    console.log(errors);
                    $scope.alert = true;
                    $scope.status = constants.ERROR;
                    $scope.message = constants.UPDATE_ERROR;
                    if(errors.non_field_errors) $scope.errorCodigo = errors.non_field_errors[0];
                    $anchorScroll();

                });

        } else {
            administrarItems.setItem(data).
                success(function (data, status, headers, config) {
                    console.log("Item Creado correctamente");
                    $scope.alert = true;
                    $scope.status = constants.SUCCESS;
                    $scope.message = constants.CREATE_SUCCESS;
                    $scope.crud = false;
                    $scope.reset = $scope.limpiarCampos();
                    $scope.getItemsPaginados($scope.catalogoActual);
                    $anchorScroll();
                }).
                error(function (errors) {
                    $scope.alert = true;
                    $scope.status = constants.ERROR;
                    $scope.message = constants.CREATE_ERROR;
                    if(errors.non_field_errors) $scope.errorCodigo = errors.non_field_errors[0];
                    console.log(errors);
                    $anchorScroll();
                });
        }

    };
}]);

app.controller('moduloControl', ['$scope', '$http', 'administrarCatalogos', 'administrarModulos', 'constants', function ($scope, $http, administrarCatalogos, administrarModulos, constants) {
    $scope.modulos = [];
    $scope.estadosGenerales = [];
    $scope.moduloActual = "";
    $scope.limpiarCampos = function() {
        $scope.id = "";
        $scope.nombre = "";
        $scope.codigo = "";
        $scope.descripcion = "";
        $scope.orden = "";
        $scope.estado = "";

        //limpiar errores
        $scope.limpiarErrores();
    };

    $scope.limpiarErrores = function(){
         $scope.errorCodigo = "";
    }


    $scope.save = function () {

        $scope.limpiarErrores();
        var data = {
                "nombre": $scope.nombre,
                "codigo": $scope.codigo,
                "descripcion": $scope.descripcion,
                "orden": $scope.orden,
                "estado": $scope.estado
            }

        if ($scope.id) {
            data["id"]=  $scope.id;
            administrarModulos.updateModulo($scope.id, data)
                .success(function (data) {
                    console.log("módulo actualizado correctamente");
                    $scope.alert = true;
                    $scope.status = constants.SUCCESS;
                    $scope.message = constants.UPDATE_SUCCESS;
                    $scope.reset = $scope.limpiarCampos();

                    administrarModulos.getModulos()
                        .success(function (data) {
                            $scope.modulos = data;
                        })
                        .error(function (error) {
                            $scope.status = 'Unable to load customer data: ' + error.message;
                        });
                })
                .error(function (errors) {
                    console.log("Error al actualizar el módulo")
                    console.log(errors);
                    $scope.alert = true;
                    $scope.status = constants.ERROR;
                    $scope.message = constants.UPDATE_ERROR;
                    if(errors.codigo) $scope.errorCodigo = errors.codigo[0];

                });
        } else {
            var data = {"codigo": $scope.codigo, "nombre": $scope.nombre, "editable": $scope.editable, "estado": $scope.estado.id, "descripcion": $scope.descripcion  }
            administrarModulos.setModulo(data)
                .success(function (data) {
                    console.log("modulo insertado correctamente");
                    $scope.alert = true;
                    $scope.status = constants.SUCCESS;
                    $scope.message = constants.CREATE_SUCCESS;
                    $scope.reset = $scope.limpiarCampos();

                    administrarModulos.getModulos()
                        .success(function (data) {
                            $scope.modulos = data;
                        })
                        .error(function (error) {
                            $scope.status = 'Unable to load customer data: ' + error.message;
                        });
                })
                .error(function (errors) {
                    console.log("Error al insertar el módulo")
                    console.log(errors);
                    $scope.alert = true;
                    $scope.status = constants.ERROR;
                    $scope.message = constants.CREATE_ERROR;
                    if(errors.codigo) $scope.errorCodigo = errors.codigo[0];
                });
        }
    };

    administrarCatalogos.getItemsPorCatalogo(constants.CAT_ESTADOS_GENERALES)
        .success(function (data) {
            $scope.estadosGenerales = data;
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });

    administrarModulos.getModulos()
        .success(function (data) {
            $scope.modulos = data;
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });

    $scope.MostrarInfoModulo = function (modulo) {
        $scope.codSelectedModulo = modulo.codigo;
        $scope.moduloActual = $scope.modulos.filter(function (m) {
            return m.id == modulo.id;
        });

        $scope.id = $scope.moduloActual[0].id;
        $scope.nombre = $scope.moduloActual[0].nombre;
        $scope.codigo = $scope.moduloActual[0].codigo;
        $scope.descripcion = $scope.moduloActual[0].descripcion;
        $scope.orden = $scope.moduloActual[0].orden;
        $scope.estado = $scope.moduloActual[0].estado;

    }
}]);

app.controller('funcionalidadControl', ['$scope', '$http', 'administrarCatalogos', 'administrarFuncionalidades', 'administrarModulos', 'constants', '$anchorScroll', '$location',
    function ($scope, $http, administrarCatalogos, administrarFuncionalidades, administrarModulos, constants, $anchorScroll, $location) {
    $scope.funcionalidades = [];
    $scope.gruposUsuarios = [];
    $scope.gruposActuales = []
    $scope.estadosGenerales = [];
    $scope.moduloActual = "";
    $scope.modulos = [];
    $scope.limpiarCampos = function() {
        $scope.id = "";
        $scope.codigo = "",
        $scope.nombre = "";
        $scope.descripcion = "";
        $scope.url = "";
        $scope.grupos = "";
        $scope.orden = null;
        $scope.icono = null;
        $scope.estado = "";
        $scope.modulo = $scope.modulos;

        //Limpiar errores
        $scope.limpiarErrores();

    };

    $scope.limpiarErrores = function(){
         $scope.errorCodigo = "";
         $scope.errorUrl = "";
    }

    $scope.nuevaFuncionalidad = function(){
       $scope.limpiarCampos();
       $scope.crud = true;
    }

    administrarModulos.getModulos()
        .success(function (data) {
            $scope.modulos = data;
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });

    administrarCatalogos.getItemsPorCatalogo(constants.CAT_ESTADOS_GENERALES)
        .success(function (data) {
            $scope.estadosGenerales = data;
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });

    administrarFuncionalidades.getGrupos()
        .success(function (data) {
            $scope.gruposUsuarios = data;
            console.log('grupos de usuarios');
            console.log(data);
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });

    $scope.MostrarFuncionalidadesDelModulo = function(modulo){
        $scope.crud = false;
        administrarFuncionalidades.getFuncionalidadesPorModulo(modulo.codigo)
        .success(function (data) {
            $scope.codSelectedModulo = modulo.codigo;
            $scope.funcionalidades = data;
            $scope.moduloActual = modulo;
            $scope.idModulo = modulo.id;
            $scope.reset = $scope.limpiarCampos();
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });
    };

    $scope.save = function () {

        $scope.limpiarErrores();
        $scope.grupos.forEach(function(ele, id){
            $scope.gruposActuales.push(ele.id)
        });

        var data = {
            "modulo": $scope.modulo.id,
            "nombre": $scope.nombre,
            "codigo": $scope.codigo,
            "url": $scope.url,
            "descripcion": $scope.descripcion,
            //"grupos": $scope.grupos,
            "grupos": $scope.gruposActuales,
            "estado": $scope.estado,
            "orden": $scope.orden,
            "icono": $scope.icono
        };

        console.log("orden");
        console.log($scope.orden);

        if ($scope.id) {
            data["id"] = $scope.id;
            administrarFuncionalidades.updateFuncionalidad($scope.id, data).
                success(function (data, status, headers, config) {
                    console.log("Actualizado correctamente");
                    $scope.alert = true;
                    $scope.status = constants.SUCCESS;
                    $scope.message = constants.UPDATE_SUCCESS;
                    $scope.reset = $scope.limpiarCampos();
                    $scope.crud = false;

                    administrarFuncionalidades.getFuncionalidadesPorModulo($scope.moduloActual.codigo).
                        success(function (data, status, headers, config) {
                            $scope.funcionalidades = data;
                        }).
                        error(function (data, status, headers, config) {
                            console.log(data);
                        });
                }).
                error(function (errors) {
                    console.log("Error al actualizar la funcionalidad")
                    console.log(errors);
                    $scope.alert = true;
                    $scope.status = constants.ERROR;
                    $scope.message = constants.UPDATE_ERROR;
                    if(errors.codigo) $scope.errorCodigo = errors.codigo[0];
                    if(errors.url) $scope.errorUrl = errors.url[0];
                    $scope.crud = true;

                });

        } else {
            administrarFuncionalidades.setFuncionalidad(data).
                success(function (data, status, headers, config) {
                    console.log("Creado correctamente");
                    $scope.alert = true;
                    $scope.status = constants.SUCCESS;
                    $scope.message = constants.CREATE_SUCCESS;
                    $scope.reset = $scope.limpiarCampos();
                    $scope.crud = false;
                    administrarFuncionalidades.getFuncionalidadesPorModulo($scope.moduloActual.codigo).
                        success(function (data, status, headers, config) {
                            $scope.funcionalidades = data;
                        }).
                        error(function (data, status, headers, config) {
                            console.log(data);
                        });
                }).
                error(function (errors) {
                    console.log("Error al insertar la funcionalidad")
                    console.log(errors);
                    $scope.alert = true;
                    $scope.status = constants.ERROR;
                    $scope.message = constants.CREATE_ERROR;
                    if(errors.codigo) $scope.errorCodigo = errors.codigo[0];
                    if(errors.url) $scope.errorUrl = errors.url[0];
                    $scope.crud = true;
                });
        }

        $anchorScroll();


    };

    $scope.CargarFuncionalidad = function (id) {
        $scope.funcionalidades.forEach(function (e, i) {
            $scope.crud = true;
            if (e.id == id) {
                $scope.id = e.id;
                $scope.codigo = e.codigo;
                $scope.nombre = e.nombre;
                $scope.url = e.url;
                $scope.descripcion = e.descripcion;
                $scope.orden = e.orden;
                $scope.icono = e.icono;
                $scope.estado = e.estado;
                $scope.modulos.forEach(function (ele, ident) {
                    if (ele.id == e.modulo) {
                        $scope.modulo = $scope.modulos[ident];
                    }
                });
                var array = []
                $scope.gruposUsuarios.forEach(function (ele, ident) {
                    if (e.grupos.indexOf(ele.id) != -1) {
                        console.log("llegue aqui 2");
                        array.push(ele);
                    }
                });
                $scope.grupos = array
            }
        });
    };

}]);

app.controller('ParametroControl', ['$scope', '$http', 'administrarParametros', 'administrarCatalogos', 'constants', function ($scope, $http, administrarParametros, administrarCatalogos, constants) {
    $scope.parametros = [];
    $scope.estadosGenerales = [];
    $scope.parametroActual = "";

    $scope.limpiarCampos = function() {
        $scope.id = "";
        $scope.codigo = "";
        $scope.nombre = "";
        $scope.descripcion = "";
        $scope.valor = "";
        $scope.estado = "";

        //limpiar errores
        $scope.limpiarErrores();
    }

    $scope.limpiarErrores = function(){
         $scope.errorCodigo = "";
    }

    $scope.submit = function () {

        $scope.limpiarErrores();

        var data = {
            "codigo": $scope.codigo,
            "nombre": $scope.nombre,
            "valor": $scope.valor,
            "descripcion": $scope.descripcion,
            "estado": $scope.estado
        }

        if ($scope.id) {
            data["id"] = $scope.id;
            administrarParametros.updateParametro($scope.id, data)
                .success(function (data) {
                    console.log("parámetro actualizado correctamente");
                    $scope.alert = true;
                    $scope.status = constants.SUCCESS;
                    $scope.message = constants.UPDATE_SUCCESS;
                    $scope.reset = $scope.limpiarCampos();

                    administrarParametros.getParametros()
                        .success(function (data) {
                            $scope.parametros = data;
                        })
                        .error(function (error) {
                            $scope.status = 'Unable to load customer data: ' + error.message;
                        });
                })
                .error(function (errors) {
                    console.log("error al actualizar parametros");
                    $scope.alert = true;
                    $scope.status = constants.ERROR;
                    $scope.message = constants.UPDATE_ERROR;
                    if(errors.codigo) $scope.errorCodigo = errors.codigo[0];
                    console.log(errors);
                });

        } else {
            administrarParametros.setParametro(data)
                .success(function (data) {
                    console.log("parámetro insertado correctamente");
                    $scope.alert = true;
                    $scope.status = constants.SUCCESS;
                    $scope.message = constants.CREATE_SUCCESS;
                    $scope.reset = $scope.limpiarCampos();

                    administrarParametros.getParametros()
                        .success(function (data) {
                            $scope.parametros = data;
                        })
                        .error(function (error) {
                            $scope.status = 'Unable to load customer data: ' + error.message;
                        });
                })
                .error(function (errors) {
                    console.log("error al insertar parametros");
                    console.log(errors);
                    $scope.alert = true;
                    $scope.status = constants.ERROR;
                    $scope.message = constants.CREATE_ERROR;
                    if(errors.codigo) $scope.errorCodigo = errors.codigo[0];
                    console.log(errors);
                });
        }

    };

    administrarCatalogos.getItemsPorCatalogo(constants.CAT_ESTADOS_GENERALES)
        .success(function (data) {
            $scope.estadosGenerales = data;
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });

    administrarParametros.getParametros()
        .success(function (data) {
            $scope.parametros = data;
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });

    $scope.MostrarInfoParametro = function (codigo) {

        $scope.codSelectedParametro = codigo;

        $scope.cat = $scope.parametros.filter(function (el) {
            return el.codigo == codigo;
        });

        $scope.cat.forEach(function (c, posicion) {
            $scope.id = c.id;
            $scope.nombre = c.nombre;
            $scope.codigo = c.codigo;
            $scope.valor = c.valor;
            $scope.descripcion = c.descripcion;
            $scope.estado = c.estado;
        });

        $scope.items = [];
        $http.get('/api-auth/item/?catalogo=' + codigo).
            success(function (data, status, headers, config) {
                $scope.items = data;
            }).
            error(function (data, status, headers, config) {
                console.log(data);
            });
    }

}]);

app.controller('ScheduleController', ['$scope', 'AdministrarAgenda', 'constants', function ($scope,AdministrarAgenda, constants) {
    $scope.dia = true;
    $scope.semana = false;
    $scope.mes = false;
    $scope.rango = 'dia'
    $scope.contador = 0;
    var fecha = new Date();
    var fechaVariable = new Date();
    $scope.fechaActual = fecha.getFullYear()+"-"+(fecha.getMonth()+1)+"-"+fecha.getDate();

    $scope.getEventos = function(){
       /* if(rango == "dia"){
            $scope.rango = 'dia'
            $scope.dia = true;
            $scope.semana = false;
            $scope.mes = false;
        } else if(rango == "semana"){
            $scope.rango = 'semana'
            $scope.dia = false;
            $scope.semana = true;
            $scope.mes = false;
        }else if(rango == "mes"){
            $scope.rango = 'mes'
            $scope.dia = false;
            $scope.semana = false;
            $scope.mes = true;
        }*/
        AdministrarAgenda.getEventos("fecha="+$scope.fechaActual+"&rango="+$scope.rango+"&contador="+$scope.contador)
    .      success(function (data, status, headers, config) {
                 $scope.eventos = data.agenda;
                 $scope.textoCabeceraAgenda = data.textoCabeceraAgenda;
                console.log(data);
            }).
            error(function (errors) {
                console.log(errors);
            });
    };

    $scope.eventos = $scope.getEventos();

    $scope.getEventosActuales = function(){
            $scope.contador = 0;
            $scope.eventos = $scope.getEventos();
    }

    $scope.fechaAnterior = function(){
        $scope.contador = $scope.contador - 1;
        $scope.eventos = $scope.getEventos();
    }

    $scope.fechaSiguiente = function(){
        $scope.contador = $scope.contador + 1;
        $scope.eventos = $scope.getEventos();
    }
}]);






