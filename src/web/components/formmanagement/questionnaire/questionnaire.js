"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var questionaire = angular.module("formmanagement.questionnaire", [
    "ngRoute",
    "formmanagement.api"
]);

questionaire.controller("questionaireCtrl", ["$scope", "Session", "Patient", "Physician", "Questionnaire", "Hads", function ($scope, Session, Patient, Physician, Questionnaire, Hads) {

    $scope.session = Session.get();
    $scope.questionnaires = Questionnaire.query();
    $scope.answers = new Array();


    $scope.selectedQuestionnaire = {"index": 0}
    $scope.selectQuesionnaire = function (questionnaire) {
        $scope.selectedQuestionnaire = questionnaire;
        $scope.selectedQuestionnaire.index = questionnaire.id - 1;

    }


    $scope.blub = function () {
        return Questionnaire.query(function (data) {
            for (var i = 0; i < data.length; ++i) {
                $scope.answers[i] = {data: []};
            }
            console.log($scope.answers);

        });
        alert("blbu");
        return "blub";
    }
    var test = $scope.blub();
    console.log(test.length);
    console.log($scope.answers);

    $scope.save = function () {
        $scope.selectedQuestionnaire.index++;
    }


}]);

questionaire.service('Answer', [function () {
    var self = this;
    var answers = Array();

    self.get = function (i) {
        console.log(answers);
        return answers[i];
    }

    self.all = function () {
        console.log(answers);
        return answers;
    }

    self.set = function (pAnswer, i) {
        console.log(answers[i]);
        answers[i] = pAnswer;
    }
}]);

questionaire.directive('questionnaireForm', [function () {
    return{
        restrict: "E",
        scope: {
            questionnaire: "=",
            index: "=",
            answers: "="
        },
        templateUrl: '/components/formmanagement/questionnaire/questionnaie-form.html',

        link: function (scope, element, attrs) {


            scope.setData = function (question, answer) {
                //console.log("index: " + question + ", " + answer);
                //scope.answers.data[question] = answer ;
                //console.log(scope.answers.data);

                //Answer.set(scope.answers.data, scope.questionnaire.id-1);
            };

            scope.save = function () {
                console.log(scope.answers);
                //scope.answers1[scope.index] = {data:[]};
                //Awer.set(scope.answers, scope.index);
            };
        }
    };
}]);

questionaire.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/questionnaire', {
        templateUrl: '/components/formmanagement/questionnaire/questionnaire.html'
    });
}]);

