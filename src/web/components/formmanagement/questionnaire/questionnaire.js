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
            //$scope.selectedQuestionnaire = $scope.questionnaire;
            //$scope.selectedQuestionnaire.index = questionnaire.id - 1;

        };

        console.log($scope.selectQuesionnaire(0).content);


        $scope.blub = function () {
            return Questionnaire.query(function () {
            })
        };


        var test = $scope.blub();


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
            answers: "=",
            reply: "="
        },
        templateUrl: '/components/formmanagement/questionnaire/questionnaie-form.html',

        link: function (scope, element, attrs) {
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

