"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var patients = angular.module("formmanagement.patients", [
    "ngRoute",
    "formmanagement.api"
]);

patients.controller("PatientsNewCtrl", ["$scope", "Session", "Patient", "Questionnaire",
    function ($scope, Session, Patient, Questionnaire) {

        $scope.session = Session.get();
        $scope.patients = Patient.query({type: 0});
        $scope.questionnaires = Questionnaire.query();

        $scope.choosePatient = function (pPatient) {
            if (pPatient) {
                var patient = new Patient({physician_id: $scope.session.user.id})
                patient.$save({id: pPatient.id})
                $scope.patientChoosen = true;
                $scope.choosenPatient = new Array(pPatient);
            } else {
                $scope.noNewPatient = true;
            }

        }

    }]);

patients.controller("PatientsTodayCtrl", ["$scope", "Session", "Patient", "Questionnaire",
    function ($scope, Session, Patient, Questionnaire) {

        $scope.session = Session.get();
        $scope.patients = Patient.query({type: 2}); //1}); //
        $scope.questionnaires = Questionnaire.query();

        $scope.$watchCollection('[patient]', function () {
            if ($scope.patient) {
                $scope.patientChoosen = true;
                $scope.choosenPatient = $scope.patient;
            }
        }, true);


    }]);

patients.controller("PatientsAllCtrl", ["$scope", "Session", "Patient", "Questionnaire",
    function ($scope, Session, Patient, Questionnaire) {

        $scope.session = Session.get();
        $scope.patients = Patient.query({type: 1});
        $scope.questionnaires = Questionnaire.query();

        $scope.choosePatient = function (pPatient) {
            $scope.patientChoosen = true;
            $scope.choosenPatient = pPatient;
        };
    }]);

patients.directive('patientOverview', ["Questionnaire", "Reply", function (Questionnaire, Reply) {
    return{
        restrict: "E",
        scope: {
            patient: "=",
            questionnaires: "="
        },
        templateUrl: '/components/formmanagement/patients/patients-overview.html',

        link: function (scope, element, attrs) {

            console.log(scope.patient);
            for (var i = 0; i < 3; ++i) {
                console.log("test");
                console.log(scope.patient);
            }

            //scope.questionnaires = Questionnaire.query();
            scope.selectedQuestionnaire = {index: 0};


            //scope.patient = {id: patients;

            scope.collapsed = true;

            scope.$watchCollection('[selectedQuestionnaire.index, patient]', function () {
                if (scope.patient) {
                    scope.replies = new Array();
                    for (var i = 0; i < scope.questionnaires.length; ++i) {
                        scope.replies.push(Reply.query({type: i + 9, id: scope.patient.id}));
                    }
                    scope.updateData(scope.replies)
                }
            }, true);

            scope.selectQuestionnaire = function (index) {
                scope.selectedQuestionnaire.index = index;
                scope.collapsed = true;
            };

            scope.toggle_collapse = function (replies) {
                scope.collapsed = !scope.collapsed;
                scope.updateData(replies);
            };

            scope.updateData = function (replies) {
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

                for (var j = 0; j < scope.questionnaires[scope.selectedQuestionnaire.index].scores.length; ++j) {
                    var scores = function () {
                        var numberArray = [];
                        for (var i = 0; i < replies.length; i++) {
                            numberArray.push(replies[i][scope.questionnaires[scope.selectedQuestionnaire.index].scores[j].type]);
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
                scope.myChart = {"data": data, "options": { scaleStartValue: 0, datasetFill: false} };
            };

            scope.chooseReply = function (i) {
                scope.selectedReply = i;
                scope.showReply = true;
            };

            scope.closeReply = function () {
                scope.showReply = false;
            };

        }
    };
}]);

patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/patients/new', {
        templateUrl: '/components/formmanagement/patients/patients-new.html'
    });
}]);

patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/patients/today', {
        templateUrl: '/components/formmanagement/patients/patients-today.html'
    });
}]);
patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/patients/all', {
        templateUrl: '/components/formmanagement/patients/patients-all.html'
    });
}]);
