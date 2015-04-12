/**
 * Created by lucho on 11/04/2015.
 */
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


app.directive("messagesAlert", function () {
    return {
        templateUrl: "/include/messages/",
        //template: "<div ng-show='alert'><div class='alert alert-{[{status}]}'><button type='button' class='close' ng-click='hideAlert()'><i class='icon-remove'></i></button><img src='/static/img/{[{status}]}.png' alt=''> {[{ message }]}</div></div>",
        restrict: "E",
        controller:  ['$scope', function ($scope) {
            $scope.hideAlert = function(){
                $scope.alert = false;
            }
        }]
    }
});

