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
    for (var i = 0; i < 3; i++) {
        $scope.answers[i] = [];
    }


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
        /*if($scope.selectedQuestionnaire.index === 0){
            //alert($scope.answers[0].length);
            for(var i=0; i<$scope.questionnaire.content.length; ++i){
                //alert(i);
                if(i % 2 === 0){
                    if(i === 0 || i === 4 || i === 7 || i === 8){
                        $scope.answers[0].anxiety_scale =+ $scope.answers[0].data[i];
                        alert("a1");
                    }
                    else{
                        $scope.answers[0].anxiety_scale =+ Math.abs($scope.answers[0].data[i] - 3);
                        alert("a2");
                    }
                }
            }
        console.log($scope.answers);
        }*/
        $scope.selectQuesionnaire(++$scope.selectedQuestionnaire.index);
    }

    $scope.save = function () {
       // Hads.save($scope.answers[0]);
        var id = $scope.session.user.id;
        var hads = new Hads({


                data: $scope.answers[0]


            }
        )
        hads.$save({type: 0, id: id});
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

