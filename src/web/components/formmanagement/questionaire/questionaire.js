"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var questionaire = angular.module("formmanagement.questionaire", [
    "ngRoute",
    "formmanagement.api"
]);

questionaire.controller("questionaireCtrl", ["$scope", "Session", "Patient", "Physician", function ($scope, Session, Patient, Physician) {

    $scope.session = Session.get();
    $scope.questionaire = [
        {
            issue: "frage1",
            awnsers: [
                {content: "1"},
                {content: "2"},
                {content: "3"},
                {content: "4"}

            ],
            choice: ""
        },
        {issue: "frage2",
            awnsers: [
                {content: "1"},
                {content: "2"},
                {content: "3"},
                {content: "5"}


            ],
            choice: ""
        },
        {issue: "frage3",
            awnsers: [
                {content: "1"},
                {content: "2"},
                {content: "3"},
                {content: "6"}

            ],
            choice: ""
        }
    ];

    console.log($scope.questionaire);

    $scope.awnsers[4] ;
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

