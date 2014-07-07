"use strict";

/**
 * Bankbook Home Module
 * Author:
 **/

var questionaire = angular.module("formmanagement.questionaire", [
    "ngRoute",
    "formmanagement.api"
]);

questionaire.controller("questionaireCtrl", ["$scope", "Session", "Patient", "Physician", "Questionnaire", "Hads", function ($scope, Session, Patient, Physician, Questionnaire, Hads) {

    $scope.session = Session.get();
    $scope.hads;
    var blub = function () {
        return Hads.get({id: 1});
    }

    sessionStorage["hads"];

    var update = function (data) {
        console.log(data)
        $scope.hads = data;
    }

    console.log($scope.hads);
    //window.$scope.hads = $scope.hads;

    $scope.questionaire = Questionnaire.query();
    $scope.awnsers ={"anxiety_scale":1,"data":[],"date":"2014-07-07","depression_scale":1,"patient_id":10,"type":9};



    $scope.setData = function (question, awnser) {
        console.log("index: " + question + ", " + awnser);
        $scope.awnsers.data[question] = awnser;
        console.log($scope.awnsers.data);
    };

    $scope.save = function(){
        alert("save");
        Hads.save($scope.awnsers);
    };

}])
;

questionaire.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/questionaire', {
        templateUrl: '/components/formmanagement/questionaire/questionaire.html'
    });
}]);

