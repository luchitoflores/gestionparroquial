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

app.controller('primerControl', function($scope, $http, $log) {
    $scope.variable = "Hello";

    $scope.initialize = function (data) {
        $log.log('initialize', data);
        $scope.initData = data;
    };

    $scope.BuscarFeligresPorId = function(){
        $scope.feligres = $http({method: 'GET', url: '/api-auth/usuario/?dni='+$scope.dni}).
        success(function (data, status, headers, config) {
                $scope.dni = data[0]["lugar_nacimiento"];
            console.log(data);
        }).
        error(function (data, status, headers, config) {
            console.log('error');
        })
    }



});



