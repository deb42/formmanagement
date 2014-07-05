"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var questionaire = angular.module("formmanagement.questionaire", [
    "ngRoute",
    "formmanagement.api"
]);

questionaire.controller("questionaireCtrl", ["$scope", "Session", "Patient", "Physician", "Questionnaire", function ($scope, Session, Patient, Physician, Questionnaire) {

    $scope.session = Session.get();

    $scope.questionaire = Questionnaire.query();


    console.log($scope.questionaire.id);

    $scope.awnsers = new Array();

    $scope.setData = function(question, awnser){
        console.log("index: " + question + ", " + awnser);
        $scope.awnsers[question] = awnser;
        console.log($scope.awnsers);
    }

}]);

questionaire.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/questionaire', {
        templateUrl: '/components/formmanagement/questionaire/questionaire.html'
    });
}]);

