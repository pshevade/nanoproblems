(function(){
	var app = angular.module('problems', []);

	app.config(['$httpProvider', function($httpProvider) {
    	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    	$httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  	}]);

	app.config(['$interpolateProvider', function($interpolateProvider){
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    }])

	app.controller("VoteController", function($scope, VoteService){
        $scope.likes = 0;
        $scope.dislikes = 0;
        $scope.problem_id = -1;


        /* getVotes */
        $scope.getVote = function() {
            console.log("Inside getVote, and the problem_id is: ", $scope.problem_id)
            VoteService.getProblemVote($scope.problem_id).then(function(dataResponse){
                $scope.likes = JSON.parse(dataResponse.data)[0].fields.likes
                $scope.dislikes = JSON.parse(dataResponse.data)[0].fields.dislikes
                // $scope.likes = dataResponse.data.Item.likes;
                // $scope.dislikes = dataResponse.data.Item.dislikes;
            });
        };

        $scope.postVote = function(vote) {
            console.log("inside postvote")
            VoteService.postMenuItemVote($scope.problem_id, vote).then(function(dataResponse){
                console.log("We posted!")
                console.log("here is the response: ", dataResponse.data)
            	$scope.likes = JSON.parse(dataResponse.data)[0].fields.likes
                $scope.dislikes = JSON.parse(dataResponse.data)[0].fields.dislikes
            })
        };

        $scope.initVote = function(problem_id) {
        	console.log("init vote! the problem id is: ", problem_id)
            if ($scope.problem_id == -1) {
                $scope.problem_id = problem_id
                $scope.getVote()
            };
            return true;

        };


    });

	app.service("VoteService", function($http){
        console.log("VoteService on")
        //this.review = {};

        this.getProblemVote = function(problem_id) {
           	problem_votes_url = '/problems/problems_json/' + problem_id;
            console.log("The url is: ", problem_votes_url)
             return $http({
                 method  : 'GET',
                 url     : problem_votes_url,
                 headers : {'Content-Type': 'application/json'},
            });
        }


        this.postMenuItemVote = function(problem_id, vote) {
            problem_votes_url = '/problems/' + problem_id +'/vote/'+vote;
            console.log("Sending HTTP req to ", problem_votes_url);
            return $http({
                method  : 'POST',
                url     : problem_votes_url,
                data    : vote,
                headers : {'Content-Type': 'application/json; charset=utf-8'},
            });
        };
    });

})();
