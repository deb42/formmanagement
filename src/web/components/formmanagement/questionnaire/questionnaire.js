"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var questionaire = angular.module("formmanagement.questionnaire", [
    "ngRoute",
    "formmanagement.api"
]);

questionaire.controller("questionaireCtrl", ["$scope", "$location", "Session", "Patient", "Physician", "Questionnaire", "Reply",
    function ($scope, $location, Session, Patient, Physician, Questionnaire, Reply) {

        $scope.session = Session.get();
        $scope.questionnaires = Questionnaire.query();
        $scope.answers = new Array(new Array());

        if ($location.path() === "/questionnaire/new") {
            $scope.new = true;
            $scope.followUp = false;
        }
        if ($location.path() === "/questionnaire/followup") {
            $scope.followUp = true;
            $scope.new = false;
        }

        $scope.$watch('selectedQuestionnaire.index', function () {
            console.log($location.path());
            if ($location.path() === "/questionnaire/new" && $scope.selectedQuestionnaire.index === 2) {
                $scope.selectedQuestionnaire.index++;
                $scope.answers[$scope.selectedQuestionnaire.index] = new Array();
            }
        }, true);

        $scope.filterQuestionnaire = function (questionnaire) {
            if (questionnaire.id === 1 || questionnaire.id === 2) {
                return true;
            }
            if (questionnaire.id === 3) {
                return $scope.followUp;
            }
            if (questionnaire.id === 4) {
                return $scope.new;
            }
        };

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
            console.log($scope.answers);
            for (var i = 0; i < $scope.answers.length; ++i) {
                if($scope.new && i===2){
                    ++i;
                }
                var reply = new Reply({
                        data: $scope.answers[i]
                    }
                );
                reply.$save({type: i, id: $scope.session.user.id});
            }
        };
    }]);

questionaire.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/questionnaire/new', {
        templateUrl: '/components/formmanagement/questionnaire/questionnaire.html'
    });
}]);

questionaire.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/questionnaire/followup', {
        templateUrl: '/components/formmanagement/questionnaire/questionnaire.html'
    });
}]);

