var ResultApp = angular.module('ResultApp', []);

ResultApp.controller('MasterController', function ($scope, $http) {


    ///////VARIABLES FROM THE PRE-INPUT PAGE... I CANT EVEN UNDERSTAND WHAT I'M DOING MY SELF AGAIN GANNNN///////
    $scope.session_nam = '';
    $scope.term_name = '';
    $scope.subject_name = '';
    ///////END OF THOSE VARIABLE, YOU SHOULD UNDERSTAND SER, IS IT EVERYTHING, YOU HAVE TO DO COMMENT FOR///////

    ////////VIEW VARIABLES///////////////////////////
    $scope.side_bar_view = 'side-bar.html';
    $scope.input_tab_view = 'pre_input.html';
    ///////END VIEW VARIABLES////////////////////////

    ///////LISTS/////////////////////////////////////
    $scope.sessions = [];
    $scope.classes = [];
    $scope.subjects = [];
    $scope.selected_students = [];
    $scope.results = [];
    //////END LISTS//////////////////////////////////

    /////SCORE///////////////////////////////////////
    $scope.log = '';
    $scope.student_id = '';
    $scope.student_name = '';
    $scope.class_name = '';
    $scope.session_admitted = '';
    $scope.test_1 = '';
    $scope.test_2 = '';
    $scope.test_3 = '';
    $scope.exam = '';
    $scope.class_position = '';
    /////SCORE//////////////////////////////////////

    loadSessions();
    loadClasses();
    loadSubjects();


    $scope.set_pre_values = function () {
        console.log('Class Name: '+ $scope.class_name);
        var data = {session_admitted: $scope.session_admitted};
        $http({
            url: '/studentSelected',
            method: 'POST',
            headers:{'Content-Type':'application/json'},
            data: JSON.stringify(data)
        }).success(function(r){
            console.log(r);
            for(var i=0; i< r.length; i++){
                $scope.selected_students.push(r[i]);
            }
            $scope.input_tab_view = 'input_score.html';
        }).error(function(resp){
            console.log('Error Performing the operation: '+resp.data)
        });
    };


    $scope.load_students_based_on_class = function () {
        var data = {session_admitted: $scope.session_admitted};
        $http({
            url: '/studentSelected',
            method: 'POST',
            headers:{'Content-Type':'application/json'},
            data: JSON.stringify(data)
        }).success(function(r){
            console.log(r);
            $scope.selected_students = [];
            //for(var j=0; j< $scope.selected_students.length; j++){
            //    $scope.selected_students.pop();
            //}  //for(var j=0; j< $scope.selected_students.length; j++){
            //    $scope.selected_students.pop();
            //}
            for(var i=0; i< r.length; i++){
                $scope.selected_students.push(r[i]);
            }
        }).error(function(resp){
            console.log('Error Performing the operation: '+resp.data)
        });
    };



    $scope.select_student_on_table = function (student) {
        console.log(student);
        $scope.student_name = student.name;
        $scope.student_id = student.id;
        $http({
           url: '/startStudentScoreRecord',
            method: 'POST',
            header: 'Content-Type: application/json',
            data: JSON.stringify({student_id: $scope.student_id, session_name: $scope.session_nam, subject_id: $scope.subject_name
            , session_admitted: $scope.session_admitted, term: $scope.term_name})
        }).success(function(resp){
            console.log(resp);
            $scope.class_name = resp.class_name;
            $scope.test_1 = resp.first_test;
            $scope.test_2 = resp.second_test;
            $scope.test_3 = resp.third_test;
            $scope.exam = resp.exam;
            console.log(resp);
        }).error(function(){
            console.log('Error in creating student instance in the scores database')
        });

        $('#test_1').removeAttr('disabled');
        $('#test_2').removeAttr('disabled');
        $('#test_3').removeAttr('disabled');
        $('#exam').removeAttr('disabled');
        $('#submit').removeAttr('disabled');

    };



    $scope.submit_score_entry = function () {
        console.log($scope.student_name);
        var cum = parseInt($scope.test_1)+parseInt($scope.test_2)+parseInt($scope.test_3)+parseInt($scope.exam);
        console.log('Test Cummulative: ' +(parseInt($scope.test_1)+parseInt($scope.test_2)+parseInt($scope.test_3)));
        console.log($scope.session_nam);
        var score_entry = {student_id:$scope.student_id, subject_name:$scope.subject_name, class_name: $scope.class_name,
            test_1:$scope.test_1, test_2:$scope.test_2, test_3:$scope.test_3, exam:$scope.exam,
            term_name:$scope.term_name, cumulative:cum, session_nam:$scope.session_nam, session_admitted:$scope.session_admitted};
        $http({
           url:'/submitScore',
            method:'post',
            header: {'Content-Type':'application/json'},
            data: JSON.stringify(score_entry)
        }).success(function(response){
            $scope.test_1 = '';
            $scope.test_2 = '';
            $scope.test_3 = '';
            $scope.exam = '';
            $scope.log = 'Successfully Inserted the Darn Score';
        }).error(function(resp, status){
            console.log(resp + '\n' + status);
            $scope.log = 'Failed to Insert the darn score, \nError '+resp;

        });
    };

    $scope.check_result = function(){
        $scope.results = [];
        $http({
            url: '/getSubjectResult',
            method: 'POST',
            header : 'Content-Type: application/json',
            data: JSON.stringify({student_id:$scope.student_id, term: $scope.term_name,
                session_nam: ($scope.session_nam).toString(), session_admitted: $scope.session_admitted})
        }).success(function(data){
            for (var i=0; i<data.length; i++){
                $scope.results.push(data[i]);
            };
            console.log(data);
            $scope.input_tab_view = 'display_result.html';
        }).error(function (response, status) {
            alert('Check the values and make sure the student is in the class selected')
        })
    };


    $scope.changeView = function(page){
        switch (page) {
            case 4:
                $scope.input_tab_view = 'check_result.html';
                break;
        }
    };


    ////////////////////FUNTIONS TO LOAD THE OPTION BOXES HERE//////////////////////////////
    function loadSessions(){
        $http.get('/loadSessions').then(function(r){
            $scope.sessions = r.data;
        })
    }

    function loadClasses(){
        $http.get('/loadClasses').then(function(r){
            $scope.classes = r.data;
        })
    }

    function loadSubjects(){
        $http.get('/loadSubjects').then(function(r){
            $scope.subjects = r.data;
        })
    }


});