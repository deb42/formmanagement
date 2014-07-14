"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var questionaire = angular.module("formmanagement.questionnaire", [
    "ngRoute",
    "formmanagement.api"
]);

questionaire.controller("questionaireCtrl", ["$scope", "Session", "Patient", "Physician", "Questionnaire", "Reply",
    function ($scope, Session, Patient, Physician, Questionnaire, Reply) {

        $scope.session = Session.get();
        $scope.questionnaires = Questionnaire.query();
        $scope.answers = new Array(new Array());

        $scope.selectedQuestionnaire = {"index": 0}
        $scope.selectQuesionnaire = function (index) {
            ++index;
            return Questionnaire.get(
                {id: index}, //params
                function (data) {   //success
                    $scope.questionnaire = data;
                },
                function (data) {   //failure
                    //error handling goes here
                });
        };

        $scope.selectQuesionnaire(0);

        $scope.proceed = function () {
            for (var i = 0; i < $scope.questionnaire.content.length; ++i) {
                if (!$scope.answers[$scope.selectedQuestionnaire.index][i]) {
                    alert("fehler");
                    return;
                }
            }
            $scope.selectQuesionnaire(++$scope.selectedQuestionnaire.index);
            $scope.answers[$scope.selectedQuestionnaire.index] = new Array();
        }

        $scope.save = function () {
            console.log($scope.answers.length);
            for (var i=0; i<$scope.answers.length; ++i) {
                console.log($scope.answers[i]);
                var reply = new Reply({
                        data: $scope.answers[i]
                    }
                );
                reply.$save({type: i, id: $scope.session.user.id});
            }
        };
    }]);

questionaire.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/questionnaire', {
        templateUrl: '/components/formmanagement/questionnaire/questionnaire.html'
    });
}]);

