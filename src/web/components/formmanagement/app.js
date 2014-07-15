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

formmanagement.run(["Session", "showLoginDialog", function (Session, showLoginDialog) {

    Session.init.error(function () {
        showLoginDialog();
    });

}]);

formmanagement.controller("NavbarCtrl", ["$scope", "Session", "getUserClass", function ($scope, Session, getUserClass) {

    $scope.session = Session.get();

    $scope.logout = function () {
        Session.logout();
    };
}]);


