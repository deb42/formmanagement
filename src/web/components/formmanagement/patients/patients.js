"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var patients = angular.module("formmanagement.patients", [
    "ngRoute",
    "formmanagement.api"
]);

patients.controller("patientsCtrl", ["$scope", "Patient", "Physician", function($scope, Patient, Physician){
        $scope.patients = Patient.query();
        $scope.physicains = Physician.query();
        console.log($scope.patients);
        $scope.test = "testing";
}]);

patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/patients', {
        templateUrl: '/components/formmanagement/patients/patients.html'
    });
}]);

