"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var patients = angular.module("formmanagement.patients", [
    "ngRoute",
    "formmanagement.api"
]);

patients.controller("patientsCtrl", ["$scope", "Session", "Patient", "Physician", "Reply",
    function ($scope, Session, Patient, Physician, Reply) {

        $scope.session = Session.get();
        $scope.patients = Patient.query();
        $scope.physicains = Physician.query();
        $scope.replies = Reply.query({type: 9, id: 9})
        console.log($scope.session);


        $scope.updateData = function (replies) {
            var chart = document.getElementById("myCoolChart").getAttribute("type");
            switch (chart) {
                case 'PolarArea':
                    $scope.generatePieData();
                    break;
                case 'Pie':
                    $scope.generatePieData();
                    break;
                case 'Doughnut':
                    $scope.generatePieData();
                    break;
                default:
                    $scope.generateData(replies);
            }
        };

        $scope.generateData = function (replies) {

            console.log(replies)
            console.log(replies[0])


            var sevenRandNumbers = function () {
                var numberArray = [];
                for (var i = 0; i < replies.length; i++) {
                    numberArray.push(replies[0]["anxiety_scale"]);
                }
                return numberArray;
            };
            var data = {
                labels: ["January", "February", "March", "April", "May"],
                datasets: [
                    {
                        fillColor: "rgba(220,220,220,0.5)",
                        strokeColor: "rgba(220,220,220,1)",
                        pointColor: "rgba(220,220,220,1)",
                        pointStrokeColor: "#fff",
                        data: [1,2,0,4,5]
                    },
                    {
                        fillColor: "rgba(151,187,205,0.5)",
                        strokeColor: "rgba(151,187,205,1)",
                        pointColor: "rgba(151,187,205,1)",
                        pointStrokeColor: "#fff",
                        data: sevenRandNumbers()
                    }
                ]
            };
            $scope.myChart = {"data": data, "options": {} };
        };

        $scope.generatePieData = function () {
            var data = [
                {
                    value: Math.floor((Math.random() * 100) + 1),
                    color: "#F38630"
                },
                {
                    value: Math.floor((Math.random() * 100) + 1),
                    color: "#E0E4CC"
                },
                {
                    value: Math.floor((Math.random() * 100) + 1),
                    color: "#69D2E7"
                }
            ]
            $scope.myChart = {"data": data, "options": {} };
        };

        $scope.line = function () {
            document.getElementById('myCoolChart').setAttribute('type', 'Line');
            $scope.updateData();
        };

        $scope.bar = function () {
            document.getElementById('myCoolChart').setAttribute('type', 'Bar');
            $scope.updateData();
        };

        $scope.radar = function () {
            document.getElementById('myCoolChart').setAttribute('type', 'Radar');
            $scope.updateData();
        };

        $scope.polarArea = function () {
            document.getElementById('myCoolChart').setAttribute('type', 'PolarArea');
            $scope.updateData();
        };

        $scope.pie = function () {
            document.getElementById('myCoolChart').setAttribute('type', 'Pie');
            $scope.updateData();
        };

        $scope.doughnut = function () {
            document.getElementById('myCoolChart').setAttribute('type', 'Doughnut');
            $scope.updateData();
        };

        //$scope.generateData();


    }])
;

patients.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/patients', {
        templateUrl: '/components/formmanagement/patients/patients.html'
    });
}]);

