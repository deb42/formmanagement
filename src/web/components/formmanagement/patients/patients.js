"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var patients = angular.module("formmanagement.patients", [
    "ngRoute",
    "formmanagement.api"
]);

patients.controller("patientsCtrl", ["$scope", "Session", "Patient", "Physician", function ($scope, Session, Patient, Physician) {

    $scope.session = Session.get();
    $scope.patients = Patient.query();
    $scope.physicains = Physician.query();
    console.log($scope.patients);

}]);

patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/patients', {
        templateUrl: '/components/formmanagement/patients/patients.html'
    });
}]);

