'use strict';

angular.module('myApp.view1', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view1', {
    templateUrl: 'view1/view1.html',
    controller: 'View1Ctrl'
  });
}])

.controller('View1Ctrl', ['$scope', function($scope) {

    $scope.levelColors = [ "#a9d70b", "#f9c802", "#ff0000" ];
    $scope.reverseColors = [ "#ff0000", "#f9c802", "#a9d70b" ];

}]);
