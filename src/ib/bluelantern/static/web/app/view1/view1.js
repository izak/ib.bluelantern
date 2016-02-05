'use strict';

angular.module('myApp.view1', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view1', {
    templateUrl: 'view1/view1.html',
    controller: 'View1Ctrl'
  });
}])

.controller('View1Ctrl', ['$scope', '$timeout', '$http',
function($scope, $timeout, $http) {

    $scope.levelColors = [ "#a9d70b", "#f9c802", "#ff0000" ];
    $scope.reverseColors = [ "#ff0000", "#f9c802", "#a9d70b" ];
    var timer = undefined;

    // Fake it for now.
    $scope.max_load = 1600;
    $scope.ac_load = 500;
    $scope.pv_watt = 200;
    $scope.bat_watt = 308;
    $scope.overall_load = (100.0 * $scope.ac_load)/$scope.max_load;

    (function updateloop(){
        timer = $timeout(function(){
            $http({
                method: 'GET',
                url: '/stats'
            }).success(function(data, stat, headers, config){
                $scope.ac_load = data.ac_load;
                $scope.pv_watt = data.pv_watt;
                $scope.bat_watt = data.bat_watt;
                $scope.overall_load = (100.0 * $scope.ac_load)/$scope.max_load;
                updateloop();
            });
        }, 5000);
    })();

    $scope.$on('$destroy', function(){ $timeout.cancel(timer); });

}]);
