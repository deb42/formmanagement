var common = angular.module("formmanagement.common", [
    "ngRoute",
    "formmanagement.api"
]);

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

