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

app.factory("administrarCatalogos", ['$http', function ($http) {
    var catalogos = {};
    catalogos.getCatalogos = function () {
        return $http.get('http://127.0.0.1:666/api-auth/catalogo/');
    };

    catalogos.getItemPorCatalogo = function (codCatalogo) {
        return $http.get('http://127.0.0.1:666/api-auth/item/?catalogo=' + codCatalogo);
    };

    catalogos.setCatalogo = function (data) {
        return $http.post('http://127.0.0.1:666/api-auth/catalogo/', data);
    };

    return catalogos;
}]);

app.factory("administrarItems", ['$http', function ($http) {
    var items = {};

    items.getItemPorCatalogo = function (codCatalogo) {
        return $http.get('http://127.0.0.1:666/api-auth/item/?catalogo=' + codCatalogo);
    };

    items.setItem = function (data) {
        return $http.post('http://127.0.0.1:666/api-auth/item/', data);
    };

    return items;
}]);

app.controller('primerControl', function ($scope, $http, $log) {
    $scope.click1 = true;
    $scope.click2 = true;

    $scope.show = function () {
        $scope.click1 = false;
        $scope.click2 = false;
    };

    $scope.hide = function () {
        $scope.click1 = true;
        $scope.click2 = true;
    };

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


    $scope.submit = function () {
        console.log($scope.estado.id);
        var data = {"codigo": $scope.codigo, "nombre": $scope.nombre, "editable": $scope.editable, "estado": $scope.estado.id, "descripcion": $scope.descripcion  }
        administrarCatalogos.setCatalogo(data)
            .success(function (data) {
                console.log("insertar catalogos");
                $scope.codigo = "";
                $scope.nombre = "";
                $scope.descripcion = "";
                $scope.editable = false;

                console.log(data);
            })
            .error(function (error) {
                console.log("error al insertar catálogos");
                console.log(error);
            });
    };

    administrarCatalogos.getItemPorCatalogo("EST")
        .success(function (data) {
            $scope.estadosGenerales = data;
            console.log(data);
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

    $scope.initialize = function (data) {
        $log.log('initialize', data);
        $scope.initData = data;
    };

    $scope.MostrarInfoCatalogo = function (codigo) {
        console.log($scope.estadosGenerales);
        $scope.cat = $scope.catalogos.filter(function (el) {
            return el.codigo == codigo;
        });

        $scope.cat.forEach(function (c, posicion) {
            $scope.nombre = c.nombre;
            $scope.codigo = c.codigo;
            $scope.descripcion = c.descripcion;
            $scope.padre = c.padre;
            $scope.editable = c.editable;
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

    administrarCatalogos.getItemPorCatalogo("EST")
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

    $scope.MostrarItemsDelCatalogo = function (codigo) {
        $http.get('http://127.0.0.1:666/api-auth/item/?catalogo=' + codigo).
            success(function (data, status, headers, config) {
                $scope.items = data;
                $scope.catalogo = "";
                $scope.codigo = "";
                $scope.nombre = "";
                $scope.valor = "";
                $scope.descripcion = "";
                $scope.principal = false;
                $scope.estado = $scope.estadosGenerales;
            }).
            error(function (data, status, headers, config) {
                console.log(data);
            });
    };

    $scope.CargarItem = function (id) {
        $scope.items.forEach(function (e, i) {
            if (e.id == id) {
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
            }
        });
    };

    $scope.guardarItem = function () {
        console.log("estado" + $scope.estado.id);
        var data = {
            "catalogo": $scope.catalogo,
            "nombre": $scope.nombre,
            "codigo": $scope.codigo,
            "valor": $scope.valor,
            "descripcion": $scope.descripcion,
            "principal": $scope.principal,
            "estado": $scope.estado.id
        }

        administrarItems.setItem(data).
            success(function (data, status, headers, config) {
                console.log(data);
                $scope.catalogo = "";
                $scope.codigo = "";
                $scope.nombre = "";
                $scope.valor = "";
                $scope.descripcion = "";
                $scope.principal = false;
                $scope.estado = $scope.estadosGenerales;


            }).
            error(function (data, status, headers, config) {
                console.log(data);
            });
    };
});







