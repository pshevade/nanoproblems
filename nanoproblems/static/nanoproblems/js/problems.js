(function(){
	var app = angular.module('problems', []);

	app.config(['$httpProvider', function($httpProvider) {
    	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    	$httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  	  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }]);

	app.config(['$interpolateProvider', function($interpolateProvider){
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    }])

  app.controller("CommentsController", function($scope, CommentsService, $sce){
        $scope.comments=[]
        $scope.problem_id = 0;
        $scope.solution_id = 0;
        $scope.comment = {}

        $scope.renderHtml = function (htmlCode){
          return $sce.trustAsHtml(htmlCode);
        };

        $scope.can_delete_comment = function(email, comment, is_admin){
          console.log("Here is the is_admin flag: ", is_admin)
          if (is_admin) {
            return true
          }
          if (comment.fields.user[0] == email){
            return true
          }
          else{
            return false
          }
        }

        $scope.getComments = function() {
            console.log("Inside getComments, and the problem_id is: ", $scope.problem_id)
            CommentsService.getComments($scope.problem_id, $scope.solution_id).then(function(dataResponse){
                console.log("Raw fetch data: ", JSON.parse(dataResponse.data))
                $scope.comments = JSON.parse(dataResponse.data)
                console.log("The comments var is: ", $scope.comments)
                // $scope.likes = dataResponse.data.Item.likes;
                // $scope.dislikes = dataResponse.data.Item.dislikes;
            });
        };

        $scope.postComment = function() {
            // $scope.comment.problem_id = problem_id
            // $scope.comment.user_email = user_email
            console.log("inside postComment: ", $scope.comment)

            CommentsService.postComment($scope.problem_id, $scope.solution_id, $scope.comment).then(function(dataResponse){
                console.log("We posted!")
                console.log("here is the response: ", dataResponse.data)
                $scope.getComments()
                $scope.comment = {}
            })
        };

        $scope.deleteComment = function(comment_id){
          console.log("inside deleteComment: ", comment_id)
          CommentsService.deleteComment($scope.problem_id, $scope.solution_id, comment_id).then(function(dataResponse){
                console.log("We deleted!")
                // console.log("here is the response: ", dataResponse.data)
                $scope.getComments()
                $scope.comment = {}
            })
        }

        $scope.initComments = function(problem_id, solution_id) {
          console.log("init comments! the problem id is: ", problem_id)

          console.log("inside if statement.")
          if (problem_id > 0){
            $scope.problem_id = problem_id
          }
          if (solution_id > 0){
            $scope.solution_id = solution_id
          }
          if ($scope.problem_id > 0 | $scope.solution_id > 0){
            $scope.getComments()
            return true;
          }
          else{
            return false;
          }
        };

    });

	app.controller("VoteController", function($scope, VoteService){
        $scope.likes = 0;
        $scope.dislikes = 0;
        $scope.solution_likes = 0;
        $scope.solution_dislikes = 0;
        $scope.problem_id = -1;
        $scope.solution_id = -1;


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

        $scope.getSolutionVote = function() {
            console.log("Inside getSolutionVote, and the solution_id is: ", $scope.solution_id)
            VoteService.getSolutionVotes($scope.solution_id).then(function(dataResponse){
                $scope.solution_likes = JSON.parse(dataResponse.data)[0].fields.likes
                $scope.solution_dislikes = JSON.parse(dataResponse.data)[0].fields.dislikes
                // $scope.likes = dataResponse.data.Item.likes;
                // $scope.dislikes = dataResponse.data.Item.dislikes;
            });
        };

        $scope.postVote = function(vote) {
            console.log("inside postvote")
            VoteService.postProblemVote($scope.problem_id, vote).then(function(dataResponse){
                console.log("We posted!")
                console.log("here is the response: ", dataResponse.data)
            	$scope.likes = JSON.parse(dataResponse.data)[0].fields.likes
                $scope.dislikes = JSON.parse(dataResponse.data)[0].fields.dislikes
            })
        };

        $scope.postSolutionVote = function(vote) {
            console.log("inside postsolutionvote")
            VoteService.postSolutionVote($scope.problem_id, $scope.solution_id, vote).then(function(dataResponse){
                console.log("We posted!")
                console.log("here is the response: ", dataResponse.data)
            	$scope.solution_likes = JSON.parse(dataResponse.data)[0].fields.likes
                $scope.solution_dislikes = JSON.parse(dataResponse.data)[0].fields.dislikes
            })
        };

        $scope.initVote = function(problem_id) {
        	console.log("init Vote! the problem id is: ", problem_id)
            if ($scope.problem_id == -1) {
                $scope.problem_id = problem_id
                $scope.getVote()
            };
            return true;

        };

        $scope.initSolutionVote = function(problem_id, solution_id){
        	console.log("init solution vote! the problem id is: ", solution_id)
        	console.log("init solution vote! the solution id is: ", problem_id)
            if ($scope.solution_id == -1) {
                $scope.solution_id = solution_id
                $scope.getSolutionVote()
            };
            if ($scope.problem_id == -1) {
                $scope.problem_id = problem_id
            };
            return true;
        };
    });

    app.controller('FilterController', ['$scope', '$sce', '$http', '$window', 'TagsService', 'FilterService', function($scope, $sce, $http, $window, TagsService, FilterService){
        // Set defaults where necessary
        $scope.tags = []
        $scope.searchText = '';
        $scope.suggestions = [];
        $scope.selectedTags = [];
        $scope.selectedIndex = 0;
        $scope.problems = []

        $scope.is_data = function(){
          if ($scope.problems.length > 0){
            return true
          }
          else {
            return false
          }
        }

        $scope.renderHtml = function (htmlCode){
          return $sce.trustAsHtml(htmlCode);
        };

        $scope.init_filter = function() {
          console.log ("init_filter")
          $scope.difficulty = 'ALL'
          $scope.category = 'ALL'
          $scope.problems = []
          $scope.tags = []
          $scope.getTags()
          // $scope.postFilter(true)
        }

        $scope.postFilter = function(all) {
          console.log("making a filter query")
          FilterService.postFilter($scope.category, $scope.difficulty, $scope.selectedTags, all).then(function(dataResponse){
            $scope.problems = JSON.parse(dataResponse.data)
            console.log("Raw fetch data: ", $scope.problems)
          })
        }

        $scope.getTags = function() {
            console.log("Inside getTags")
            TagsService.getTags().then(function(dataResponse){
                var data = JSON.parse(dataResponse.data)
                console.log("Raw fetch data: ", data)

                for (var tag in data){
                   console.log(data[tag])
                   $scope.tags.push(data[tag].fields['tag_name'])
                }
                console.log("The tags var is: ", $scope.tags)
                // $scope.likes = dataResponse.data.Item.likes;
                // $scope.dislikes = dataResponse.data.Item.dislikes;
            });
        };




        $scope.search = function() {
            console.log("Inside search")
            if ($scope.searchText) {
              searchText = $scope.searchText.toLowerCase();
            }
            else {
              searchText = $scope.searchText;
            }

            $scope.suggestions.length = 0;
            $scope.tags.forEach(suggest);
            function suggest(value) {
              console.log("Insie search.suggest, value is: ", value)
                var value = value.toLowerCase();
                console.log('Checking out conditions to push to suggestions, here is value: ', value)
                console.log("Search text: ", $scope.searchText)
                console.log("Value at index of search txt (should be ==0): ", value.indexOf($scope.searchText))
                console.log("Search text length: (should be > 0): ", $scope.searchText.length )
                console.log("last one: (should be -1): ", $scope.suggestions.indexOf(value) )
                  if (value.indexOf($scope.searchText) === 0 && $scope.searchText.length > 0 && $scope.suggestions.indexOf(value) === -1) {
                    console.log("Pushing to suggestsion: ", value)
                    $scope.suggestions.push(value);
                  }
            }
            $scope.selectedIndex = 0;
        }

        $scope.checkKeyDown = function(event) {
          console.log("inside checkKeyDown")
          if (event.keyCode === 40) { //down key, increment selectedIndex
            event.preventDefault();
            if ($scope.selectedIndex+1 !== $scope.suggestions.length) {
              $scope.selectedIndex++;
            }
          }
          else if (event.keyCode === 38) { //up key, decrement selectedIndex
            event.preventDefault();
            if ($scope.selectedIndex-1 !== -1) {
              $scope.selectedIndex--;
            }
          }
          else if (event.keyCode === 9) { //Tab (9) pressed
            if ($scope.searchText.length > 0) {
              event.preventDefault();
              $scope.addToSelectedTags($scope.selectedIndex);
              $scope.searchText = '';
              $scope.search();
            }
          }
          else if (event.keyCode === 13 || event.type == "blur") { // Enter (13) pressed
            if ($scope.searchText && $scope.searchText.length > 0) {
              event.preventDefault();
              $scope.pushToSelectedTags($scope.searchText); // Force add raw data, not suggestion
              $scope.searchText = '';
              $scope.search();
            }
          }
        }

        $scope.addToSelectedTags = function(index) {
          if ($scope.suggestions.length > 0) {
            if ($scope.selectedTags.indexOf($scope.suggestions[index]) == -1) {
              $scope.selectedTags.push($scope.suggestions[index]);
            }
          }
          else {
            if ($scope.selectedTags.indexOf($scope.searchText) == -1 && $scope.searchText !== '') {
              $scope.selectedTags.push($scope.searchText);
            }
          }
        }
        $scope.pushToSelectedTags = function(tag) {
          if ($scope.selectedTags.length < 5){
            console.log("this is the tag to be pushed: ", tag)
            $scope.selectedTags.push(tag);
          }
        }

        $scope.removeTag = function(index) {
          $scope.selectedTags.splice(index, 1);
        }
  }]);


  app.service("FilterService", function($http){
        console.log("FilterService on")
        //this.review = {};

        this.postFilter = function(category, difficulty, tags, all) {
            if (all){
              return $http({
                method   : 'GET',
                url      : '/problems/json/all/',
                headers  : {'Content-Type': 'application/json'},
              });
            }
            else {
              filter_url = '/problems/filter/';
              console.log("The url is: ", filter_url)
               return $http({
                   method  : 'POST',
                   url     : filter_url,
                   data    : {
                              "filters": [{
                                "type": "filter",
                                "property": "category",
                                "value": category
                              }, {
                                "type": "filter",
                                "property": "difficulty",
                                "value": difficulty
                              }, {
                                "type": "filter",
                                "property": "tags__tag_name__in",
                                "value": tags
                              }]
                            },
                   headers : {'Content-Type': 'application/json'},
              });
            }
        }
  });


  app.service("TagsService", function($http){
        console.log("TagsService on")
        //this.review = {};

        this.getTags = function() {
            tags_url = '/problems/tags_json/';
            console.log("The url is: ", tags_url)
             return $http({
                 method  : 'GET',
                 url     : tags_url,
                 headers : {'Content-Type': 'application/json'},
            });
        }
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

       	this.getSolutionVotes = function(solution_id){
       		solution_votes_url = '/problems/solutions_json/' + solution_id;
       		return $http({
       			method	: 'GET',
       			url 	: solution_votes_url,
       			headers : {'Content-Type': 'application/json'},
       		})

       	}

        this.postProblemVote = function(problem_id, vote) {
            problem_votes_url = '/problems/' + problem_id +'/vote/'+vote;
            console.log("Sending HTTP req to ", problem_votes_url);
            return $http({
                method  : 'POST',
                url     : problem_votes_url,
                data    : vote,
                headers : {'Content-Type': 'application/json; charset=utf-8'},
            });
        };

        this.postSolutionVote = function(problem_id, solution_id, vote) {
            solution_votes_url = '/problems/' + problem_id +'/show_solution/'+ solution_id + '/vote/' + vote;
            console.log("Sending HTTP req to ", solution_votes_url);
            return $http({
                method  : 'POST',
                url     : solution_votes_url,
                data    : vote,
                headers : {'Content-Type': 'application/json; charset=utf-8'},
            });
        };
    });

  /* CommentsService -
        Service to get the reviews and send new comments to the database
    */
  app.service("CommentsService", function($http){
      console.log("CommentsService on")
      //this.review = {};


      this.getComments = function(problem_id, solution_id) {
          if (!solution_id){
            comments_url = '/problems/' + problem_id + '/comments/all/';

          }
          else {
            comments_url = '/problems/' + problem_id + '/show_solution/' + solution_id + '/comments/all/'
          }
          return $http({
              method  : 'GET',
              url     : comments_url,
              headers : {'Content-Type': 'application/json'},
          });
      }


      this.postComment = function(problem_id, solution_id, comment_obj) {
          if (!solution_id){
            comments_url = '/problems/' + problem_id + '/comments/new/';

          }
          else {
            comments_url = '/problems/' + problem_id + '/show_solution/' + solution_id + '/comments/new/'
          }
          console.log("Sending HTTP req to ", comments_url);
          console.log("Comment obj, ", comment_obj)
          return $http({
              method  : 'POST',
              url     : comments_url,
              data    : comment_obj,
              headers : {'Content-Type': 'application/json'},
          });
      };

      this.deleteComment = function(problem_id, solution_id, comment_id) {
          console.log("inside deleteComment: ", problem_id, solution_id, comment_id)
          if (!solution_id){
            comments_url = '/problems/' + problem_id + '/comments/' + comment_id +'/delete/';

          }
          else {
            comments_url = '/problems/' + problem_id + '/show_solution/' + solution_id + '/comments/' + comment_id +'/delete/'
          }
          console.log("Sending HTTP req to ", comments_url);
          return $http({
              method  : 'POST',
              url     : comments_url,
              headers : {'Content-Type': 'application/json'},
          });
      };
  });


// app.controller('FormController', ['$scope', '$http', '$window', 'TagsService', function($scope, $http, $window){
// 		// Set defaults where necessary
// 		$scope.difficulty = 'EASY';

//     $scope.tags = []
//     $scope.getTags = function() {
//         console.log("Inside getTags")
//         TagsService.getTags().then(function(dataResponse){
//             var data = JSON.parse(dataResponse.data)
//             console.log("Raw fetch data: ", data)

//             for (var tag in data){
//                console.log(data[tag])
//                $scope.tags.push(data[tag].fields['tag_name'])
//             }
//             console.log("The tags var is: ", $scope.tags)
//             // $scope.likes = dataResponse.data.Item.likes;
//             // $scope.dislikes = dataResponse.data.Item.dislikes;
//         });
//     };

//     $scope.searchText = '';
//     $scope.suggestions = [];
// 		$scope.selectedTags = [];
// 		$scope.selectedIndex = 0;

//     $scope.search = function() {
// 			if ($scope.searchText) {
// 				searchText = $scope.searchText.toLowerCase();
// 			} else {
// 				searchText = $scope.searchText;
// 			}

//       $scope.suggestions.length = 0;
// 			$scope.tags.forEach(suggest);
// 			function suggest(value) {
// 				var value = value.toLowerCase();
// 				if (value.indexOf($scope.searchText) === 0 && $scope.searchText.length > 0 && $scope.suggestions.indexOf(value) === -1) {
// 					$scope.suggestions.push(value);
// 				}
// 			}
// 			$scope.selectedIndex = 0;
// 		}

//     $scope.checkKeyDown = function(event) {
// 			if (event.keyCode === 40) { //down key, increment selectedIndex
// 				event.preventDefault();
// 				if ($scope.selectedIndex+1 !== $scope.suggestions.length) {
// 					$scope.selectedIndex++;
// 				}
// 			}
// 			else if (event.keyCode === 38) { //up key, decrement selectedIndex
// 				event.preventDefault();
// 				if ($scope.selectedIndex-1 !== -1) {
// 					$scope.selectedIndex--;
// 				}
// 			}
// 			else if (event.keyCode === 9) { //Tab (9) pressed
// 				if ($scope.searchText.length > 0) {
// 					event.preventDefault();
// 					$scope.addToSelectedTags($scope.selectedIndex);
// 					$scope.searchText = '';
// 					$scope.search();
// 				}
// 			}
//       else if (event.keyCode === 13 || event.type == "blur") { // Enter (13) pressed
//         if ($scope.searchText.length > 0) {
// 					event.preventDefault();
//           $scope.pushToSelectedTags($scope.searchText); // Force add raw data, not suggestion
//           $scope.searchText = '';
// 					$scope.search();
//         }
//       }
// 		}

//     $scope.addToSelectedTags = function(index) {
// 			if ($scope.suggestions.length > 0) {
// 				if ($scope.selectedTags.indexOf($scope.suggestions[index]) == -1) {
// 					$scope.selectedTags.push($scope.suggestions[index]);
// 				}
// 			}
// 			else {
// 				if ($scope.selectedTags.indexOf($scope.searchText) == -1 && $scope.searchText !== '') {
// 					$scope.selectedTags.push($scope.searchText);
// 				}
// 			}
// 		}
//     $scope.pushToSelectedTags = function(tag) {
//       $scope.selectedTags.push(tag);
//     }

//     $scope.removeTag = function(index) {
// 			$scope.selectedTags.splice(index, 1);
// 		}

//     // Submit function
// 		$scope.submit = function() {
// 			// Define required fields
// 			var required = [$scope.title, $scope.difficulty, $scope.description, $scope.selectedTags];
// 			// Set counter to check each required field actually contains data
// 			var allDataPresent = '0';
//       required.forEach(checkData);
// 			// Check that all the required fields contain data
// 			function checkData(value) {
// 				if (value && value.length > 0) {
// 					allDataPresent++;
// 				}
// 			}
// 			// If all required fields contain data, then submit

// 			if (allDataPresent == required.length) {
//         document.getElementById('id_tags').required = false;
//         document.getElementById('id_articles').required = false;

//         var tagString = arrayToCSV($scope.selectedTags);
//         var articleString = arrayToCSV($scope.articles);

//         function arrayToCSV(array) {
//           var temp = '';
//           array.forEach(toCSV);
//           function toCSV(value, index) {
//             if (index == 0) {
//               temp = value;
//             } else {
//               temp = temp + ',' + value;
//             }
//           }
//           return temp;
//         }

// 				// Payload for POST request
// 				//$scope.description = encodeURIComponent($scope.description)
// 				$scope.description_escaped = $scope.description.replace(/\\n/g, "\\n")
//                                       						   .replace(/\\'/g, "\\'")
// 						                                       .replace(/\\"/g, '\\"')
// 						                                       .replace(/\\&/g, "\\&")
// 						                                       .replace(/\\r/g, "\\r")
// 						                                       .replace(/\\t/g, "\\t")
// 						                                       .replace(/\\b/g, "\\b")
// 						                                       .replace(/\\f/g, "\\f");
// 				var payload = {
// 					'title': $scope.title,
// 					'difficulty': $scope.difficulty,
// 					'description': $scope.description_escaped,
// 					'tags_list': tagString,
// 				};

//         // POST request to submit data
// 				$http.post('/problems/create_problem/', payload, {"Content-Type": "application/json; charset=utf-8"}).
// 					then (function(response) {
//             $http.get('/problems/problems_JSON/').then(function(problemResponse){
//               sessionStorage.removeItem('problems');
//         			var data = JSON.parse(JSON.parse(problemResponse.data));
//         			sessionStorage.setItem('problems', JSON.stringify(data));
//               // console.log(JSON.stringify(data.data, null, 2));
//               $window.location.href = '/problems/' + response.data;
//             });
//           });
//       }
//     }
//   }]);

//   app.controller('ProblemsController', ['$scope', '$http', '$window', function($scope, $http, $window) {
//     //
//   }]);

//   app.filter('problemsFilter', function() {
//     return function(items, scope) {
//       var filtered = [];
//       var checksum = [];
//       angular.forEach(items, function(item) {

//         itemTags = [];
//         item.fields.tags.forEach(lowerCase);
//         function lowerCase(value) {
//           if (typeof(value) == 'string') {
//             itemTags.push(value.toLowerCase());
//           } else {
//             itemTags.push(value);
//           }
//         }

//         if (scope.selectedTags.length == 0) {
//           filtered.push(item);
//         } else {
//           scope.selectedTags.forEach(checkTags);
//           function checkTags(value) {
//             if (itemTags.indexOf(value) == -1) {
//               checksum.push(0);
//             } else {
//               checksum.push(1);
//             }
//           }
//           if (checksum.indexOf(0) == -1) {
//             filtered.push(item);
//           }
//         }
//         checksum = [];
//       });
//       return filtered;
//     }
//   });


})();
