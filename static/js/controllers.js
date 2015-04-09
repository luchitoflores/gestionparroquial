/**
 * Created by lucho on 21/10/2014.
 */

var app = angular.module('app', ['ngCookies']);
app.config([
    '$httpProvider',
    '$interpolateProvider',
    function ($httpProvider, $interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';

    }]).
    run([
        '$http',
        '$cookies',
        function ($http, $cookies) {
            $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        }]);


/////////------------------------------- FACTORIAS------------------------------------/////////////

app.factory("administrarCatalogos", ['$http', function ($http) {
    var catalogos = {};
    catalogos.getCatalogos = function () {
        return $http.get('http://127.0.0.1:666/api-auth/catalogo/');
    };

    catalogos.getItemsPorCatalogo = function (codCatalogo) {
        return $http.get('http://127.0.0.1:666/api-auth/item/?catalogo=' + codCatalogo);
    };

    catalogos.setCatalogo = function (data) {
        return $http.post('http://127.0.0.1:666/api-auth/catalogo/', data);
    };

    catalogos.updateCatalogo = function (id, data) {
        return $http.put('http://127.0.0.1:666/api-auth/catalogo/' + id, data);
    };

    return catalogos;
}]);

app.factory("administrarItems", ['$http', function ($http) {
    var items = {};

    items.getItemsPorCatalogo = function (codCatalogo) {
        return $http.get('http://127.0.0.1:666/api-auth/item/?catalogo=' + codCatalogo);
    };

    items.setItem = function (data) {
        return $http.post('http://127.0.0.1:666/api-auth/item/', data);
    };

    items.updateItem = function (id, data) {
        return $http.put('http://127.0.0.1:666/api-auth/item/' + id, data);
    };

    return items;
}]);

app.factory("administrarParametros", ['$http', function ($http) {
    var parametros = {};

    parametros.getParametros = function () {
        return $http.get('http://127.0.0.1:666/api-auth/parametro/');
    };

    parametros.setParametro = function (data) {
        return $http.post('http://127.0.0.1:666/api-auth/parametro/', data);
    };

    parametros.updateParametro = function (id, data) {
        return $http.put('http://127.0.0.1:666/api-auth/parametro/' + id, data);
    };

    return parametros;
}]);

app.factory("administrarModulos", ['$http', function ($http) {
    var modulos = {};

    modulos.getModulos = function () {
        return $http.get('http://127.0.0.1:666/api-auth/modulo/');
    };

    modulos.setModulo = function (data) {
        return $http.post('http://127.0.0.1:666/api-auth/modulo/', data);
    };

    modulos.updateModulo = function (id, data) {
        return $http.put('http://127.0.0.1:666/api-auth/modulo/' + id, data);
    };

    return modulos;
}]);

app.factory("administrarFuncionalidades", ['$http', function ($http) {
    var funcionalidades = {};

    funcionalidades.getFuncionalidades = function () {
        return $http.get('http://127.0.0.1:666/api-auth/funcionalidad/');
    };

    funcionalidades.setFuncionalidad = function (data) {
        return $http.post('http://127.0.0.1:666/api-auth/funcionalidad/', data);
    };

    funcionalidades.updateFuncionalidad = function (id, data) {
        return $http.put('http://127.0.0.1:666/api-auth/funcionalidad/' + id, data);
    };

    funcionalidades.getFuncionalidadesPorModulo = function (codModulo) {
        return $http.get('http://127.0.0.1:666/api-auth/funcionalidad/?modulo=' + codModulo);
    };

    funcionalidades.getGrupos = function () {
        return $http.get('http://127.0.0.1:666/api-auth/grupo/');
    };

    funcionalidades.getModulos = function () {
        return $http.get('http://127.0.0.1:666/api-auth/modulo/');
    };

    return funcionalidades;
}]);

/////////------------------------------- CONTROLADORES ------------------------------------/////////////

app.controller('menuControl', function ($scope) {

    $scope.aClick = function (event) {

        if ($(event.target).attr("class") == "accordion-toggle collapsed") {
            $(event.target).html('<span class="pull-right"><i class="icon-double-angle-down"></i></span>');
        } else {
            $(event.target).html('<span class="pull-right"><i class="icon-double-angle-up"></i></span>');

        }
    };

    /*$scope.click1 = true;
     $scope.click2 = true;*/

    /*$scope.show = function (self) {
     cosole.log(self);
     $scope.click1 = false;
     $scope.click2 = false;
     };

     $scope.hide = function (self) {
     cosole.log(self);
     $scope.click1 = true;
     $scope.click2 = true;
     };*/

    $scope.variable = "Hello";

    $scope.initialize = function (data) {
        $log.log('initialize', data);
        $scope.initData = data;
    };

    $scope.BuscarFeligresPorId = function () {
        $scope.feligres = $http({method: 'GET', url: '/api-auth/usuario/?dni=' + $scope.dni}).
            success(function (data, status, headers, config) {
                $scope.dni = data[0]["lugar_nacimiento"];
                console.log(data);
            }).
            error(function (data, status, headers, config) {
                console.log('error');
            })
    }

});

app.controller('catalogoControl', function ($scope, $http, administrarCatalogos) {

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

        console.log('catPadre: ' + $scope.padre);
        var data = {
                "codigo": $scope.codigo,
                "nombre": $scope.nombre,
                "editable": $scope.editable,
                "estado": $scope.estado.id,
                "descripcion": $scope.descripcion
                //"padre": $scope.padre.id
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
                        })
                        .error(function (error) {
                            $scope.status = 'Unable to load customer data: ' + error.message;
                        });
                })
                .error(function (error) {
                    console.log("error al insertar catálogos");
                    console.log(error);
                });
        } else {


            administrarCatalogos.setCatalogo(data)
                .success(function (data) {
                    console.log("catalogo insertado correctamente");
                    $scope.reset = limpiarCampos();

                    administrarCatalogos.getCatalogos()
                        .success(function (data) {
                            $scope.catalogos = data;
                        })
                        .error(function (error) {
                            $scope.status = 'Unable to load customer data: ' + error.message;
                        });
                })
                .error(function (error) {
                    console.log("error al insertar catálogos");
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

    $scope.MostrarItemsDelCatalogo = function (catalogo) {
        administrarCatalogos.getItemsPorCatalogo(catalogo.codigo).
            success(function (data, status, headers, config) {
                $scope.items = data;
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
    $scope.estadosGenerales = [];
    $scope.moduloActual = "";
    function limpiarCampos() {
        $scope.id = "";
        $scope.codigo = "",
        $scope.nombre = "";
        $scope.descripcion = "";
        $scope.url = "";
        $scope.grupos = $scope.gruposUsuarios;
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
        })
        .error(function (error) {
            $scope.status = 'Unable to load customer data: ' + error.message;
        });

    $scope.MostrarFuncionalidadesDelModulo = function(modulo){
        administrarFuncionalidades.getFuncionalidadesPorModulo(modulo.codigo)
        .success(function (data) {
            console.log(data);
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
        var data = {
            "modulo": $scope.idModulo,
            "nombre": $scope.nombre,
            "codigo": $scope.codigo,
            "url": $scope.url,
            "descripcion": $scope.descripcion,
            "grupos": $scope.grupos.id,
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
                $scope.gruposUsuarios.forEach(function (ele, ident) {
                    if (ele.id == e.grupo) {
                        $scope.grupos = $scope.grupos[ident];
                    }
                });
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

    $scope.MostrarInfoModulo = function (id) {
        $scope.moduloActual = $scope.modulos.filter(function (m) {
            return m.id == id;
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



///////////////////////------------------------- DIRECTIVAS
app.directive("isActive", function () {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            scope.$watch(function () {
                //console.log("antiguo valor: "+element.attr('id'));
                return element.attr('class');
            }, function (newValue, oldValue) {
                if(newValue === "accordion-body in collapse"){
                    //console.log(">>");
                } else {
                    //console.log("<<");
                }
                //console.log("nuevo valor: "+newValue);
                // console.log("viejo valor: "+oldValue);
            });
        }

        //template: '<div></div>',
        //replace: true
    };

});







