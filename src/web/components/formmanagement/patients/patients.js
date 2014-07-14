"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var patients = angular.module("formmanagement.patients", [
    "ngRoute",
    "formmanagement.api"
]);

patients.controller("patientsCtrl", ["$scope", "Session", "Patient", "Physician", "Reply", "Questionnaire",
    function ($scope, Session, Patient, Physician, Reply, Questionnaire) {

        $scope.session = Session.get();
        $scope.patients = Patient.query({physician_id: $scope.session.user.id});
        $scope.physicains = Physician.query();
        $scope.questionnaires = Questionnaire.query();
        //$scope.replies = Reply.query({type: 9, id: 9})
        $scope.selectedQuestionnaire = {index: 0};
        $scope.selectedPatient = new Object(); //{birthday:"","email":"","forename":"","gender":"",id:9,"physician_id":null,"surname":"","type":1,"username":""}
        $scope.collapsed = true;
        //console.log($scope.selectedPatient.id)

        $scope.$watchCollection('[selectedQuestionnaire.index, patient]', function () {
            if ($scope.patient) {
                console.log($scope.patient.id)
                $scope.replies = new Array();
                for (var i = 0; i < $scope.questionnaires.length; ++i) {
                    $scope.replies.push(Reply.query({type: i + 9, id: $scope.patient.id}));
                }
                $scope.updateData($scope.replies)
            }
        },true);

        $scope.selectPatient = function(patient){
            console.log("selecht");
            $scope.patient = patient;
        }

        /*setInterval(function () {
         console.log($scope.replies)
         if ($scope.replies) {
         $scope.updateData($scope.replies);
         }
         }, 1000);*/

        $scope.selectQuestionnaire = function (index) {
            $scope.selectedQuestionnaire.index = index;
            // setTimeout(function(){
            $scope.updateData($scope.replies[index]);
            console.log($scope.replies[index])
            $scope.collapsed = true;
            //alert("data updated");
            // }, 3000)
        };

        $scope.toggle_collapse = function (replies) {
                    $scope.collapsed = !$scope.collapsed;
                    $scope.updateData(replies);
            };

        $scope.updateData = function (replies) {
            var colors = ["green", "blue", "yellow"];

            var dates = function () {
                var numberArray = [];
                for (var i = 0; i < replies.length; i++) {
                    numberArray.push(replies[i]["date"]);
                }
                return numberArray;
            };

            var data = {labels: dates(), datasets: [
                {pointColor: "#fffff", data: [0]}
            ]};

            for (var j = 0; j < $scope.questionnaires[$scope.selectedQuestionnaire.index].scores.length; ++j) {
                var scores = function () {
                    var numberArray = [];
                    for (var i = 0; i < replies.length; i++) {
                        numberArray.push(replies[i][$scope.questionnaires[$scope.selectedQuestionnaire.index].scores[j].type]);
                    }
                    return numberArray;
                };


                data.datasets.push(
                    {
                        fillColor: colors[j],
                        strokeColor: colors[j],
                        pointColor: colors[j],
                        pointStrokeColor: "#fff",
                        data: scores()
                    }
                );

            }
            $scope.myChart = {"data": data, "options": { scaleStartValue: 0, datasetFill: false} };
        };


        $scope.line = function () {
            document.getElementById('myCoolChart').setAttribute('type', 'Line');
            $scope.updateData();
        };

        $scope.bar = function () {
            document.getElementById('myCoolChart').setAttribute('type', 'Bar');
            $scope.updateData();
        };

        $scope.chooseReply = function (i) {
            $scope.selectedReply = i;
            $scope.showReply = true;
        }

        $scope.closeReply = function () {
            $scope.showReply = false;
        }
    }])
;

patients.directive('questionnaireLorm', [function () {
    return{
        restrict: "E",
        scope: {
            questionnaire: "=",
            index: "=",
            answers: "=",
            reply: "="
        },
        templateUrl: '/components/formmanagement/common/questionnaie-form.html',

        link: function (scope, element, attrs) {
            scope.save = function () {
                console.log(scope.answers);
                //scope.answers1[scope.index] = {data:[]};
                //Awer.set(scope.answers, scope.index);
            };
        }
    };
}]);

patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/patients', {
        templateUrl: '/components/formmanagement/patients/patients.html'
    });
}]);

