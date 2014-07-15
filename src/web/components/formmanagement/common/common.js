var common = angular.module("formmanagement.common", [
    "ngRoute",
    "formmanagement.api"
]);


common.factory('isPatient', ['UserType', function (UserType) {
    return function (user) {
        /* jshint bitwise: false */
        return (user && (user.type & UserType.Patient));
    };
}]);

common.factory('isPhysician', ['UserType', function (UserType) {
    return function (user) {
        /* jshint bitwise: false */
        return (user && (user.type & UserType.Physician));
    };
}]);

common.factory('showSingUpDialog', ['$modal', '$timeout', 'Session',
    function ($modal, $timeout, Session) {

        var NewPatientCtrl = function ($scope, $modalInstance, $location) {
            $scope.patient = {surname: "", forename: "", gender: "", birthday: "", username: "", password: ""};

            $scope.save = function () {
                $scope.forename = $scope.surname = $scope.gender = $scope.birthday = $scope.username = $scope.usernameExists = $scope.password = $scope.passwordUnequal = false;
                if (!$scope.patient.forename) {
                    $scope.forename = true;
                } else if (!$scope.patient.surname) {
                    $scope.surname = true;
                } else if (!$scope.patient.birthday) {
                    $scope.birthday = true;
                } else if (!$scope.patient.gender) {
                    $scope.gender = true;
                } else if (!$scope.patient.username) {
                    $scope.username = true;
                } else if (!$scope.patient.password) {
                    $scope.password = true;
                } else if ($scope.patient.comparePassword !== $scope.patient.password) {
                    $scope.passwordUnequal = true;
                } else {

                    var newPatient = new Patient({
                        username: $scope.patient.username,
                        pw_hash: $scope.patient.password,
                        name: $scope.patient.forename + " " + $scope.patient.surname,
                        physician_id: 0
                    });

                    var path = 'api/users/' + $scope.patient.username;
                    $http.get(path)
                        .error(function () {
                            Session.signup(newPatient).success(function () {
                                $modalInstance.close();
                                $location.path('/questionnaire');
                            });
                        })
                        .success(function () {
                            $scope.usernameExists = true;
                        });
                }
            };

            $scope.back = function () {
                $modalInstance.close();
                window.location.reload();
            };


        };

        return function showSingUpDialog() {
            $modal.open({
                controller: NewPatientCtrl,
                templateUrl: '/components/formmanagement/login/new-patient.html',
                keyboard: false,
                backdrop: "static"
            });
        };

    }]);


common.directive('questionnaireForm', [function () {
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

        }
    };
}]);

common.directive('chart', function () {
    var baseWidth = 800;
    var baseHeight = 600;

    return {
        restrict: 'E',
        template: '<canvas></canvas>',
        scope: {
            chartObject: "=value"
        },
        link: function (scope, element, attrs) {
            var canvas = element.find('canvas')[0],
                context = canvas.getContext('2d'),
                chart;

            var options = {
                type: attrs.type || "Line",
                width: attrs.width || baseWidth,
                height: attrs.height || baseHeight
            };
            canvas.width = options.width;
            canvas.height = options.height;
            chart = new Chart(context);

            scope.$watch(function () {
                return element.attr('type');
            }, function (value) {
                if (!value) return;
                options.type = value;
                var chartType = options.type;
                chart[chartType](scope.chartObject.data, scope.chartObject.options);
            });

            //Update when charts data changes
            scope.$watch(function () {
                return scope.chartObject;
            }, function (value) {
                if (!value) return;
                var chartType = options.type;
                chart[chartType](scope.chartObject.data, scope.chartObject.options);
            });
        }

    }
});

