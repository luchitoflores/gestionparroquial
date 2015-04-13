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

app.controller('catalogoControl', function ($scope, $http, administrarCatalogos, constants) {
    $scope.alert = false;
    $scope.catalogos = [];
    $scope.estadosGenerales = [];
    $scope.catalogoActual = "";

    function limpiarCampos() {
        $scope.id = "";
        $scope.codigo = "";
        $scope.nombre = "";
        $scope.descripcion = "";
        $scope.editable = false;
        $scope.padre = $scope.catalogos;
        $scope.estado = $scope.estadosGenerales;
    };


    $scope.submit = function () {
        var data = {
                "codigo": $scope.codigo,
                "nombre": $scope.nombre,
                "editable": $scope.editable,
                "estado": $scope.estado.id,
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
                    $scope.reset = limpiarCampos();

                    administrarCatalogos.getCatalogos()
                        .success(function (data) {
                            $scope.catalogos = data;
                            $scope.alert = true;
                            $scope.status = constants.SUCCESS;
                            $scope.message = constants.UPDATE_SUCCESS;
                        })
                        .error(function (error) {

                        });
                })
                .error(function (errors) {
                    $scope.alert = true;
                    $scope.status = constants.ERROR;
                    $scope.message = constants.UPDATE_ERROR;
                    $scope.errorCodigo = errors.codigo[0];
                    console.log(errors);
                });
        } else {
            administrarCatalogos.setCatalogo(data)
                .success(function (data) {
                    console.log("catalogo insertado correctamente");
                    $scope.reset = limpiarCampos();

                    administrarCatalogos.getCatalogos()
                        .success(function (data) {
                            $scope.catalogos = data;
                            $scope.alert = true;
                            $scope.status = constants.SUCCESS;
                            $scope.message = constants.CREATE_SUCCESS;
                        })
                        .error(function (error) {
                            $scope.status = 'Unable to load customer data: ' + error.message;
                        });
                })
                .error(function (error) {
                    $scope.alert = true;
                    $scope.status = constants.ERROR;
                    $scope.message = constants.CREATE_ERROR;
                    console.log(error);
                });
        }
    };

    administrarCatalogos.getItemsPorCatalogo("EST")
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
            $scope.estadosGenerales.forEach(function (ele, ident) {
                if (ele.id == c.estado) {
                    $scope.estado = $scope.estadosGenerales[ident];
                }
            });
        });

        $scope.items = [];
        $http.get('http://127.0.0.1:666/api-auth/item/?catalogo=' + codigo).
            success(function (data, status, headers, config) {
                $scope.items = data;
            }).
            error(function (data, status, headers, config) {
                console.log(data);
            });
    }

});

app.controller('itemControl', function ($scope, $http, administrarCatalogos, administrarItems) {
    $scope.catalogos = [];
    $scope.estadosGenerales = [];
    $scope.items = [];
    $scope.catalogoActual = "";
    $scope.itemActual = "";
    $scope.itemsPadre = [];

    function limpiarCampos() {
        $scope.id = "";
        $scope.codigo = "";
        $scope.nombre = "";
        $scope.valor = "";
        $scope.descripcion = "";
        $scope.principal = false;
        $scope.estado = $scope.estadosGenerales;
        $scope.padre = $scope.itemsPadre;
    };

    administrarCatalogos.getItemsPorCatalogo("EST")
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

    $scope.MostrarItemsDelCatalogo = function (catalogo) {

        $scope.crud = false;
        $scope.codSelectedCatalogo = catalogo.codigo;

        administrarItems.getItemsPaginadosPorCatalogo(catalogo.codigo).
            success(function (data, status, headers, config) {
                $scope.items = data.results;
                $scope.pageprevious = data.previous;
                $scope.pagenext = data.next;
                $scope.pagecount = data.count;
                $scope.catalogoActual = catalogo;
                $scope.catalogo = $scope.catalogoActual.id;
                $scope.padreCodigo = $scope.catalogoActual.padreCodigo;
                $scope.reset = limpiarCampos();

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
                $scope.estadosGenerales.forEach(function (ele, ident) {
                    if (ele.id == e.estado) {
                        $scope.estado = $scope.estadosGenerales[ident];
                    }
                });

                $scope.itemsPadre.forEach(function (ele, ident) {
                if (ele.id == e.padre) {
                    $scope.padre = $scope.itemsPadre[ident];
                }
            });
            }
        });
    };

    $scope.guardarItem = function () {
        var data = {
            "catalogo": $scope.catalogo,
            "nombre": $scope.nombre,
            "codigo": $scope.codigo,
            "valor": $scope.valor,
            "descripcion": $scope.descripcion,
            "principal": $scope.principal,
            "estado": $scope.estado.id
        };

        if( $scope.padre != null){
                 data["padre"] = $scope.padre.id;
            };

        if ($scope.id) {
            data["id"] = $scope.id;
            administrarItems.updateItem($scope.id, data).
                success(function (data, status, headers, config) {
                    console.log("Actualizado correctamente");
                    $scope.reset = limpiarCampos();
                    $scope.crud = false;

                    administrarItems.getItemsPorCatalogo($scope.catalogoActual.codigo).
                        success(function (data, status, headers, config) {
                            $scope.items = data;
                        }).
                        error(function (data, status, headers, config) {
                            console.log(data);
                        });
                }).
                error(function (data, status, headers, config) {
                    console.log(data);
                });

        } else {
            administrarItems.setItem(data).
                success(function (data, status, headers, config) {
                    console.log("Creado correctamente");
                    $scope.crud = false;
                    $scope.reset = limpiarCampos();
                    administrarItems.getItemsPorCatalogo($scope.catalogoActual.codigo).
                        success(function (data, status, headers, config) {
                            $scope.items = data;
                        }).
                        error(function (data, status, headers, config) {
                            console.log(data);
                        });
                }).
                error(function (data, status, headers, config) {
                    console.log(data);
                });
        }

    };
});

app.controller('ParametroControl', function ($scope, $http, administrarParametros, administrarCatalogos) {
    $scope.parametros = [];
    $scope.estadosGenerales = [];
    $scope.parametroActual = "";

    function limpiarCampos() {
        $scope.id = "";
        $scope.codigo = "";
        $scope.nombre = "";
        $scope.descripcion = "";
        $scope.valor = "";
        $scope.estado = $scope.estadosGenerales;
    }

    $scope.submit = function () {
        var data = {
            "codigo": $scope.codigo,
            "nombre": $scope.nombre,
            "valor": $scope.valor,
            "descripcion": $scope.descripcion,
            "estado": $scope.estado.id
        }

        if ($scope.id) {
            data["id"] = $scope.id;
            administrarParametros.updateParametro($scope.id, data)
                .success(function (data) {
                    console.log("parámetro actualizado correctamente");
                    $scope.reset = limpiarCampos();

                    administrarParametros.getParametros()
                        .success(function (data) {
                            $scope.parametros = data;
                        })
                        .error(function (error) {
                            $scope.status = 'Unable to load customer data: ' + error.message;
                        });
                })
                .error(function (error) {
                    console.log("error al insertar parametros");
                    console.log(error);
                });

        } else {
            administrarParametros.setParametro(data)
                .success(function (data) {
                    console.log("parámetro insertado correctamente");
                    $scope.reset = limpiarCampos();

                    administrarParametros.getParametros()
                        .success(function (data) {
                            $scope.parametros = data;
                        })
                        .error(function (error) {
                            $scope.status = 'Unable to load customer data: ' + error.message;
                        });
                })
                .error(function (error) {
                    console.log("error al insertar parametros");
                    console.log(error);
                });
        }

    };

    administrarCatalogos.getItemsPorCatalogo("EST")
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
        $scope.cat = $scope.parametros.filter(function (el) {
            return el.codigo == codigo;
        });

        $scope.cat.forEach(function (c, posicion) {
            $scope.id = c.id;
            $scope.nombre = c.nombre;
            $scope.codigo = c.codigo;
            $scope.valor = c.valor;
            $scope.descripcion = c.descripcion;

            $scope.estadosGenerales.forEach(function (ele, ident) {
                if (ele.id == c.estado) {
                    $scope.estado = $scope.estadosGenerales[ident];
                }
            });
        });

        $scope.items = [];
        $http.get('http://127.0.0.1:666/api-auth/item/?catalogo=' + codigo).
            success(function (data, status, headers, config) {
                $scope.items = data;
            }).
            error(function (data, status, headers, config) {
                console.log(data);
            });
    }

});


app.controller('funcionalidadControl', function ($scope, $http, administrarCatalogos, administrarFuncionalidades) {
    $scope.funcionalidades = [];
    $scope.gruposUsuarios = [];
    $scope.gruposActuales = []
    $scope.estadosGenerales = [];
    $scope.moduloActual = "";
    function limpiarCampos() {
        $scope.id = "";
        $scope.codigo = "",
        $scope.nombre = "";
        $scope.descripcion = "";
        $scope.url = "";
        $scope.grupos = "";
        $scope.orden = "";
        $scope.icono = "";
        $scope.estado = $scope.estadosGenerales;
    };

    administrarCatalogos.getItemsPorCatalogo("EST")
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
        administrarFuncionalidades.getFuncionalidadesPorModulo(modulo.codigo)
        .success(function (data) {
            $scope.codSelectedModulo = modulo.codigo;
            $scope.funcionalidades = data;
            $scope.moduloActual = modulo;
            $scope.idModulo = modulo.id;
            $scope.reset = limpiarCampos();
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });
    };

    $scope.save = function () {

        $scope.grupos.forEach(function(ele, id){
            $scope.gruposActuales.push(ele.id)
        });

        console.log('grupos actuales: ');
        console.log($scope.gruposActuales);

        var data = {
            "modulo": $scope.idModulo,
            "nombre": $scope.nombre,
            "codigo": $scope.codigo,
            "url": $scope.url,
            "descripcion": $scope.descripcion,
            //"grupos": $scope.grupos,
            "grupos": $scope.gruposActuales,
            "estado": $scope.estado.id,
            "orden": $scope.orden,
            "icono": $scope.icono
        };
        console.log(data);
        if ($scope.id) {
            data["id"] = $scope.id;
            administrarFuncionalidades.updateFuncionalidad($scope.id, data).
                success(function (data, status, headers, config) {
                    console.log("Actualizado correctamente");
                    $scope.reset = limpiarCampos();

                    administrarFuncionalidades.getFuncionalidadesPorModulo($scope.moduloActual.codigo).
                        success(function (data, status, headers, config) {
                            $scope.funcionalidades = data;
                        }).
                        error(function (data, status, headers, config) {
                            console.log(data);
                        });
                }).
                error(function (data, status, headers, config) {
                    console.log(data);
                });

        } else {
            administrarFuncionalidades.setFuncionalidad(data).
                success(function (data, status, headers, config) {
                    console.log("Creado correctamente");
                    $scope.reset = limpiarCampos();
                    administrarFuncionalidades.getFuncionalidadesPorModulo($scope.moduloActual.codigo).
                        success(function (data, status, headers, config) {
                            $scope.funcionalidades = data;
                        }).
                        error(function (data, status, headers, config) {
                            console.log(data);
                        });
                }).
                error(function (data, status, headers, config) {
                    console.log(data);
                });
        }

    };

    $scope.CargarFuncionalidad = function (id) {
        $scope.funcionalidades.forEach(function (e, i) {
            if (e.id == id) {
                $scope.id = e.id;
                $scope.codigo = e.codigo;
                $scope.nombre = e.nombre;
                $scope.url = e.url;
                $scope.descripcion = e.descripcion;
                $scope.orden = e.orden;
                $scope.icono = e.icono;
                $scope.estadosGenerales.forEach(function (ele, ident) {
                    if (ele.id == e.estado) {
                        $scope.estado = $scope.estadosGenerales[ident];
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

});

app.controller('moduloControl', function ($scope, $http, administrarCatalogos, administrarModulos) {
    $scope.modulos = [];
    $scope.estadosGenerales = [];
    $scope.moduloActual = "";
    function limpiarCampos() {
        $scope.id = "";
        $scope.nombre = "";
        $scope.codigo = "";
        $scope.descripcion = "";
        $scope.orden = "";
        $scope.estado = $scope.estadosGenerales;
    };


    $scope.save = function () {

        var data = {
                "nombre": $scope.nombre,
                "codigo": $scope.codigo,
                "descripcion": $scope.descripcion,
                "orden": $scope.orden,
                "estado": $scope.estado.id
            }

        if ($scope.id) {
            data["id"]=  $scope.id;
            administrarModulos.updateModulo($scope.id, data)
                .success(function (data) {
                    console.log("módulo actualizado correctamente");
                    $scope.reset = limpiarCampos();

                    administrarModulos.getModulos()
                        .success(function (data) {
                            $scope.modulos = data;
                        })
                        .error(function (error) {
                            $scope.status = 'Unable to load customer data: ' + error.message;
                        });
                })
                .error(function (error) {
                    console.log("error al insertar modulo");
                    console.log(error);
                });
        } else {
            var data = {"codigo": $scope.codigo, "nombre": $scope.nombre, "editable": $scope.editable, "estado": $scope.estado.id, "descripcion": $scope.descripcion  }
            administrarModulos.setModulo(data)
                .success(function (data) {
                    console.log("modulo insertado correctamente");
                    $scope.reset = limpiarCampos();

                    administrarModulos.getModulos()
                        .success(function (data) {
                            $scope.modulos = data;
                        })
                        .error(function (error) {
                            $scope.status = 'Unable to load customer data: ' + error.message;
                        });
                })
                .error(function (error) {
                    console.log("error al insertar modulo");
                    console.log(error);
                });
        }
    };

    administrarCatalogos.getItemsPorCatalogo("EST")
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
        $scope.estadosGenerales.forEach(function (ele, ident) {
            if (ele.id == $scope.moduloActual[0].estado) {
                $scope.estado = $scope.estadosGenerales[ident];
            }
        });
    }
});




