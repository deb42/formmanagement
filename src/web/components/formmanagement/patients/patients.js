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
        $scope.colors = ["green", "blue", "yellow"];

        $scope.choosePatient = function (pPatient) {
            if (pPatient) {
                var patient = new Patient({physician_id: $scope.session.user.id})
                patient.$save({type: pPatient.id})
                $scope.patientChoosen = true;
                $scope.choosenPatient = pPatient;
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

patients.controller("PatientsAssignCtrl", ["$scope", "Session", "AssignedPatients", "Questionnaire",
    function ($scope, Session, AssignedPatients, Questionnaire) {

        $scope.session = Session.get();
        $scope.patients = AssignedPatients.query();
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
        $scope.colors = ["green", "blue", "yellow"];

        $scope.choosePatient = function (pPatient) {
            $scope.patientChoosen = true;
            $scope.choosenPatient = pPatient;
        };
    }]);

patients.directive('patientOverview', ["Questionnaire", "Reply", "showDiagnosisParticipantsDialog",
    function (Questionnaire, Reply, showDiagnosisParticipantsDialog) {
        return{
            restrict: "E",
            scope: {
                patient: "=",
                questionnaires: "="
            },
            templateUrl: '/components/formmanagement/patients/patients-overview.html',

            link: function (scope, element, attrs) {

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
                        //scope.updateData(scope.replies)
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
                    scope.colors = ["green", "blue", "yellow"];

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
                                fillColor: scope.colors[j],
                                strokeColor: scope.colors[j],
                                pointColor: scope.colors[j],
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

                scope.diagnosisParticipants = function (patient_id) {
                    console.log("test");
                    showDiagnosisParticipantsDialog(patient_id);
                }
            }
        };
    }]);

common.factory('showDiagnosisParticipantsDialog', ['$modal', '$http', 'Session', 'Physician', 'DiagnosisParticipants',
    function ($modal, $http, Session, Physician, DiagnosisParticipants) {

        var DiagnosisParticipantsCtrl = function ($scope, $modalInstance, patient_id) {

            $scope.patient_id = patient_id;
            $scope.physicians = Physician.query();
            $scope.choosenDiagnosisParticipants = DiagnosisParticipants.query({patient: patient_id});

            $scope.choosenPhysicians = new Array();
            $scope.deletedPhysician = new Array();

            $scope.choosePhysicians = function (physician) {
                $scope.choosenPhysicians.push(physician)
            };

            $scope.deletePhysicians = function (physician) {
                $scope.deletedPhysician.push(physician)
            };

            $scope.save = function () {

                for (var i = 0; i < $scope.choosenPhysicians.length; ++i) {
                    DiagnosisParticipants.save({
                        physician_id: $scope.choosenPhysicians[i].id,
                        patient_id: patient_id

                    })
                }
                $modalInstance.close();
            };

            $scope.back = function () {
                $modalInstance.close();
                window.location.reload();
            };

            $scope.filterChoosenPhysician = function (physician) {
                console.log($scope.choosenDiagnosisParticipants)
                //console.log($.inArray(physician, $scope.choosenDiagnosisParticipants));
                for (var i = 0; i < $scope.choosenDiagnosisParticipants.length; i++) {
                    if ($scope.choosenDiagnosisParticipants[i].id === physician.id) {
                        return false;
                    }
                }
                for (var i = 0; i < $scope.choosenPhysicians.length; i++) {
                    if ($scope.choosenPhysicians[i].id === physician.id) {
                        return false;
                    }
                }
                return true;

            };


        };

        return function showDiagnosisParticipantsDialog(patient_id) {
            $modal.open({
                controller: DiagnosisParticipantsCtrl,
                templateUrl: '/components/formmanagement/patients/diagnosis-participants.html',
                keyboard: false,
                backdrop: "static",
                resolve: {
                    patient_id: function () {
                        return patient_id
                    }
                }
            });
        };

    }]);


patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/patients/new', {
        templateUrl: '/components/formmanagement/patients/selectionmethod/patients-new.html'
    });
}]);

patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/patients/today', {
        templateUrl: '/components/formmanagement/patients/selectionmethod/patients-today.html'
    });
}]);

patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/patients/all', {
        templateUrl: '/components/formmanagement/patients/selectionmethod/patients-all.html'
    });
}]);

patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/patients/assign', {
        templateUrl: '/components/formmanagement/patients/selectionmethod/patients-assign.html'
    });
}]);