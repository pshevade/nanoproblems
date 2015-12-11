(function(){
  var app = angular.module('createProject', []);

  app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  }]);

  app.controller('FormController', ['$scope', '$http', '$window', function($scope, $http, $window){
		// Set defaults where necessary
		$scope.difficulty = 'EASY';

    $scope.tags = []
    var projectData = JSON.parse(sessionStorage.getItem('projects'));
    projectData.forEach(getData);
    function getData(allData) {
      allData.fields.tags.forEach(getTags);
      function getTags(tag) {
        if ($scope.tags.indexOf(tag) == -1) {
          $scope.tags.push(tag);
        }
      }
    }

    $scope.searchText = '';
    $scope.suggestions = [];
		$scope.selectedTags = [];
		$scope.selectedIndex = 0;

    $scope.search = function() {
			if ($scope.searchText) {
				searchText = $scope.searchText.toLowerCase();
			} else {
				searchText = $scope.searchText;
			}

      $scope.suggestions.length = 0;
			$scope.tags.forEach(suggest);
			function suggest(value) {
				var value = value.toLowerCase();
				if (value.indexOf($scope.searchText) === 0 && $scope.searchText.length > 0 && $scope.suggestions.indexOf(value) === -1) {
					$scope.suggestions.push(value);
				}
			}
			$scope.selectedIndex = 0;
		}

    $scope.checkKeyDown = function(event) {
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
        if ($scope.searchText.length > 0) {
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
      $scope.selectedTags.push(tag);
    }

    $scope.removeTag = function(index) {
			$scope.selectedTags.splice(index, 1);
		}

    // Add articles
		$scope.article = '';
		$scope.articles = [];
		$scope.maxArticlesText = '';
		$scope.maxArticles = 5;

		$scope.addArticle = function(event) {
			if ($scope.article) {
				if (event.keyCode === 13 || event.keyCode === 9 || event.type == "blur") { //Enter or Tab pressed
					// To-do: validate for URL instead of >0
					if ($scope.article.length > 0 && $scope.articles.indexOf($scope.article) == -1) {
						event.preventDefault();
						if ($scope.articles.length < $scope.maxArticles) {
							$scope.articles.push($scope.article);
							$scope.article = '';
						}
						if ($scope.articles.length == $scope.maxArticles) {
							$scope.maxArticlesText = 'Maximum number of articles reached';
						}
					}
				}
			}
		}

		$scope.removeArticle = function(index) {
			$scope.articles.splice(index, 1);
			$scope.maxArticlesText = '';
		}

    // Submit function
		$scope.submit = function() {
			// Define required fields
			var required = [$scope.title, $scope.difficulty, $scope.description, $scope.selectedTags, $scope.articles];
			// Set counter to check each required field actually contains data
			var allDataPresent = '0';
      required.forEach(checkData);
			// Check that all the required fields contain data
			function checkData(value) {
				if (value && value.length > 0) {
					allDataPresent++;
				}
			}
			// If all required fields contain data, then submit

			if (allDataPresent == required.length) {
        document.getElementById('id_tags').required = false;
        document.getElementById('id_articles').required = false;

        var tagString = arrayToCSV($scope.selectedTags);
        var articleString = arrayToCSV($scope.articles);

        function arrayToCSV(array) {
          var temp = '';
          array.forEach(toCSV);
          function toCSV(value, index) {
            if (index == 0) {
              temp = value;
            } else {
              temp = temp + ',' + value;
            }
          }
          return temp;
        }

				// Payload for POST request
				//$scope.description = encodeURIComponent($scope.description)
				$scope.description_escaped = $scope.description.replace(/\\n/g, "\\n")
                                      						   .replace(/\\'/g, "\\'")
						                                       .replace(/\\"/g, '\\"')
						                                       .replace(/\\&/g, "\\&")
						                                       .replace(/\\r/g, "\\r")
						                                       .replace(/\\t/g, "\\t")
						                                       .replace(/\\b/g, "\\b")
						                                       .replace(/\\f/g, "\\f");
				var payload = {
					'title': $scope.title,
					'collaborators': 1,
					'difficulty': $scope.difficulty,
					'description': $scope.description_escaped,
					'tags_list': tagString,
					'articles': articleString
				};

        // POST request to submit data
				$http.post('/projects/create_project/', payload, {"Content-Type": "application/json; charset=utf-8"}).
					then (function(response) {
            $http.get('/projects/projects_JSON/').then(function(projectResponse){
              sessionStorage.removeItem('projects');
        			var data = JSON.parse(JSON.parse(projectResponse.data));
        			sessionStorage.setItem('projects', JSON.stringify(data));
              // console.log(JSON.stringify(data.data, null, 2));
              $window.location.href = '/projects/' + response.data;
            });
          });
      }
    }
  }]);
})();
