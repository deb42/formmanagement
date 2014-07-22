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

formmanagement.run(["Session", "$rootScope", "showLoginDialog", "$location", "isPatient", "isPhysician",
    function (Session, $rootScope, showLoginDialog, $location, isPatient, isPhysician) {

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
                if (user.physician_id === 0) {
                    $location.path("/questionnaire/new");
                } else {
                    $location.path("/questionnaire/followup");
                }

            }
            if (user && isPhysician(user)) {
                $location.path("/patients/all");
            }
        });

    }]);

formmanagement.controller("NavbarCtrl", ["$scope", "$location", "Session", "isPhysician", "isPatient", "isAdmin", "AssignedPatients",
    function ($scope, $location, Session, isPhysician, isPatient, isAdmin, AssignedPatients) {

        $scope.session = Session.get();
        $scope.isPhysician = isPhysician;
        $scope.isPatient = isPatient;
        $scope.isAdmin = isAdmin;

        $scope.assignedPatients = AssignedPatients.query();

        $scope.getNavActiveClass = function (path) {
            if (path === "/") {
                return $location.path() === "/" ? "active" : "";
            }
            if ($location.path().substr(0, path.length) === path) {
                return "navbar-element-selected";
            } else {
                return "";
            }
        };
        $scope.logout = function () {
            $location.path('/');
            Session.logout();
        };
    }]);


