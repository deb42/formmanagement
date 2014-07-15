"use strict";

/**
 * Bankbook Main Module
 * Includes sub pages modules and declares controllers, directives, ... needed for basic bankbook frame functionality
 **/

var formmanagement = angular.module("formmanagement", [     // declaration of bankbook (main) module
    "ngRoute",                                  // ngRoute directive for realizing routing
    "formmanagement.api",                             // included bankbook modules
    "formmanagement.common",
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

formmanagement.run(["Session", "$rootScope","showLoginDialog", "$location", "isPatient", function (Session, $rootScope, showLoginDialog, $location, isPatient) {

    Session.init
        .error(function () {
            showLoginDialog();
        });


    var session = Session.get();
    // show modal for choosing advisor, if client and no advisor is set
    $rootScope.$watch(function () {
        return session.user;
    }, function () {
        /* jshint bitwise:false */
        var user = session.user;
        if (user && isPatient(user)) {
            $location.path("/questionnaire");
        }
    });

}]);

formmanagement.controller("NavbarCtrl", ["$scope", "Session", "isPhysician",function ($scope, Session, isPhysician) {

    $scope.session = Session.get();
    $scope.isPhysician = isPhysician;

    /*$scope.$watch($scope.session, function () {
        $scope.isPhysician = isPhysician($scope.session.user);
        console.log($scope.session);
    })*/

    $scope.logout = function () {
        Session.logout();
    };
}]);


