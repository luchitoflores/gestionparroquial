app.factory("administrarCatalogos", ['$http', function($http){
    var catalogos = {};
        catalogos.getCatalogos = function(){
            return $http.get('http://127.0.0.1:666/api-auth/catalogo/');
        };

        catalogos.getItemsPorCatalogo = function(codCatalogo){
            return $http.get('http://127.0.0.1:666/api-auth/item/?catalogo='+codCatalogo);
        };

         catalogos.setCatalogo = function(data){
            return $http.post('http://127.0.0.1:666/api-auth/catalogo/', data);
        };

     return catalogos;
}]);

app.factory("administrarItems", ['$http', function($http){
    var items = {};

        items.getItemsPorCatalogo = function(codCatalogo){
            return $http.get('http://127.0.0.1:666/api-auth/item/?catalogo='+codCatalogo);
        };

         items.setItem = function(data){
            return $http.post('http://127.0.0.1:666/api-auth/item/', data);
        };

     return items;
}]);