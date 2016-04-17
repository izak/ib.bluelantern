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
    var timer = undefined,
        backoff = 1;

    $scope.ac_max_load = 1000;
    $scope.ac_load = 0;
    $scope.pv_watt = 0;
    $scope.pv_max_watt = 1000;
    $scope.bat_watt = 0;
    $scope.bat_range = 1000;
    $scope.charge_flow = 0;
    $scope.discharge_flow = 0;

    var cf = document.querySelector('.chargeflow'),
        cfwidth = cf.clientWidth,
        df = document.querySelector('.dischargeflow'),
        dfwidth = df.clientWidth;

    (function updateloop(){
        timer = $timeout(function(){
            $http({
                method: 'GET',
                url: '/stats'
            }).success(function(data, stat, headers, config){
                backoff = 1;
                $scope.ac_max_load = data.ac_max_load;
                $scope.ac_load = data.ac_load;
                $scope.pv_watt = data.pv_watt;
                $scope.pv_max_watt = data.pv_max_watt;
                $scope.bat_watt = data.bat_watt;
                $scope.bat_range = Math.max(data.ac_max_load, data.pv_max_watt);

                // Animate charge flow
                var mflow = Math.max(data.pv_max_watt, data.ac_max_load),
                    coff = (cfwidth * data.pv_watt) / (7 * mflow),
                    doff = (dfwidth * data.ac_load) / (7 * mflow);
                $scope.charge_flow = ($scope.charge_flow + coff) % (20*cfwidth);
                $scope.discharge_flow = ($scope.discharge_flow + doff) % (20*dfwidth);

                updateloop();
            }).error(function(){
                // On error, back off exponentially up to a minute
                backoff = Math.min(backoff*2, 32);
                updateloop();
            });
        }, 2000 * backoff);
    })();

    $scope.$on('$destroy', function(){ $timeout.cancel(timer); });

}]);
