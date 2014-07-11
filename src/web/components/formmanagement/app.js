"use strict";

/**
 * Bankbook Main Module
 * Includes sub pages modules and declares controllers, directives, ... needed for basic bankbook frame functionality
 **/

var formmanagement = angular.module("formmanagement", [     // declaration of bankbook (main) module
    "ngRoute",                                  // ngRoute directive for realizing routing
    "formmanagement.api",                             // included bankbook modules
    "formmanagement.patients",
    "formmanagement.questionnaire"
]);

// create routing functionality on singleton $routeProvider and declare default route for non-existing sub pages

formmanagement.config(['$routeProvider',
    function ($routeProvider) {
        // default route for non-existing routes
        $routeProvider.otherwise({
            redirectTo: "/"
        });
}]);

formmanagement.run(["Session", "showLoginDialog", function (Session, showLoginDialog) {

    Session.init.error(function () {
        showLoginDialog();
    });

}]);

formmanagement.controller("NavbarCtrl", ["$scope", "Session", "getUserClass", function ($scope, Session, getUserClass) {

    $scope.session = Session.get();
    //console.log($scope.session.user);
   // $scope.userClass = getUserClass($scope.session.user.type);

    $scope.logout = function(){
       Session.logout();
   } ;
}]);

formmanagement.directive('chart', function () {
    var baseWidth = 600;
    var baseHeight = 400;

    return {
      restrict: 'E',
      template: '<canvas></canvas>',
      scope: {
        chartObject: "=value"
      },
      link: function (scope, element, attrs) {
        var canvas  = element.find('canvas')[0],
            context = canvas.getContext('2d'),
            chart;

        var options = {
          type:   attrs.type   || "Line",
          width:  attrs.width  || baseWidth,
          height: attrs.height || baseHeight
        };
        canvas.width = options.width;
        canvas.height = options.height;
        chart = new Chart(context);

        scope.$watch(function(){ return element.attr('type'); }, function(value){
          if(!value) return;
          options.type = value;
          var chartType = options.type;
          chart[chartType](scope.chartObject.data, scope.chartObject.options);
        });

        //Update when charts data changes
        scope.$watch(function() { return scope.chartObject; }, function(value) {
          if(!value) return;
          var chartType = options.type;
          chart[chartType](scope.chartObject.data, scope.chartObject.options);
        });
      }

    }
  });


