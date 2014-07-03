"use strict";

/**
 * Formmanagement API Module
 * Contains all client-side models and manages *all* communication with the backend.
 **/

var api = angular.module("formmanagement.api", [
    "ngResource"
]);

api.factory("Patient", ["$resource", function ($resource) {
    console.log("test")
    return $resource("/api/patients/:id", {id: "@id" });
}]);


