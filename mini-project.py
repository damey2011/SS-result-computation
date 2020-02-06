import json
from flask import Flask, render_template, request, url_for, session, jsonify, redirect
from DBConn import connection
from GetTeachers import getAll
from logic.DataBaseInsertOperations import insert_class, insert_session, insert_teacher, insert_subject, insert_score, \
    insert_student_instance_into_scores, insert_student
from logic.DatabaseRetrieveOperations import retrieve_sessions, retrieve_classes, get_teacher_id_using_name, \
    retrieve_teacher_particular_subjects, retrieve_selected_students, retrieve_term_scores, get_student_session_admitted
from models import Student

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secretblabla!'


@app.route('/')
def login():
    if session.get('logged_in') and session.get('admin'):
        return render_template('dashboard.html', username=session['username'])
    if session.get('logged_in') and not session.get('admin'):
        return render_template('index.html', username=session['username'])
    if not session.get('logged_in'):
        return render_template('login.html', error_bar='hide')


@app.route('/logon', methods=['POST', 'GET'])
def logon():
    if request.method == 'POST':
        c, conn = connection()
        username = request.form['username']
        password = request.form['password']
        c.execute("SELECT password, admin FROM teachers WHERE username = %s", username)
        data = c.fetchall()
        password_db = data[0][0]
        admin_db = data[0][1]
        if password == password_db and admin_db == '1':
            session['admin'] = True
            session['logged_in'] = True
            session['username'] = username
            return render_template('dashboard.html', username=username)
        elif password == password_db and admin_db == '0':
            session['admin'] = False
            session['logged_in'] = True
            session['username'] = username
            return render_template('index.html', username=username)
        elif password != password_db:
            error = 'Sorry, Could not verify your details'
            return render_template('login.html', error=error, error_bar='')


@app.route('/logout')
def logout():
    if session.get('logged_in'):
        session.clear()
        error = 'You have been logged out'
        return render_template('login.html', error=error, error_bar='')
    elif not session.get('logged_in'):
        error = 'You are not logged in'
        return render_template('login.html', error=error, error_bar='')


@app.route('/addClass')
def add_class():
    if session.get('logged_in') and session.get('admin'):
        return render_template('addClass.html', username=session.get('username'), teachers=getAll(), hide='hide')


@app.route('/post_class', methods=['GET', 'POST'])
def post_class():
    if request.method == 'POST':
        class_name = request.form['class_name']
        teacher_id = request.form['teacher_id']
        insert_class(class_name, teacher_id)
        return render_template('addClass.html', username=session.get('username'), info='Class Inserted Successfully',
                               hide='', teachers=getAll())


@app.route('/addSession')
def add_session():
    if session.get('logged_in') and session.get('admin'):
        return render_template('addSession.html', username=session.get('username'), hide='hide')


@app.route('/post_session', methods=['GET', 'POST'])
def post_session():
    if request.method == 'POST':
        session_name = request.form['session']
        insert_session(session_name)
    return render_template('addSession.html', username=session.get('username'), info='Session Inserted Successfully',
                           hide='')


@app.route('/addTeacher')
def add_teacher():
    if session.get('logged_in') and session.get('admin'):
        return render_template('addTeacher.html', username=session.get('username'), hide='hide')


@app.route('/post_teacher', methods=['GET', 'POST'])
def post_teacher():
    if request.method == 'POST':
        teacher_name = request.form['teacher_name']
        username = request.form['username']
        password = request.form['password']
        admin = request.form['admin']
        insert_teacher(teacher_name, username, password, admin)
    return render_template('addTeacher.html', username=session.get('username'), info='Session Inserted Successfully',
                           hide='')


@app.route('/addSubject')
def add_subject():
    if session.get('logged_in') and session.get('admin'):
        return render_template('addSubject.html', username=session.get('username'), hide='hide', teachers=getAll())


@app.route('/post_subject', methods=['POST'])
def post_subject():
    if request.method == 'POST':
        subject_name = request.form['subject_name']
        teacher_id = request.form['teacher_id']
        insert_subject(subject_name, teacher_id)
    return render_template('addSubject.html', username=session.get('username'), info='Subject Inserted Successfully',
                           hide='', teachers=getAll())


@app.route('/addStudent')
def add_student():
    if session.get('logged_in') and session.get('admin'):
        return render_template('addStudent.html', username=session.get('username'), hide='hide',
                               sessions=retrieve_sessions())


@app.route('/post_student', methods=['POST'])
def post_student():
    if request.method == 'POST':
        student_name = request.form['name']
        session_admitted = request.form['session_admitted']
        insert_student(student_name, session_admitted)
    return render_template('addStudent.html', username=session.get('username'), info='Student Inserted Successfully',
                           hide='', sessions=retrieve_sessions())


@app.route('/loadSessions', methods=['GET'])
def load_sessions():
    return json.dumps(retrieve_sessions())


@app.route('/loadClasses', methods=['GET'])
def load_classes():
    return json.dumps(retrieve_classes())


@app.route('/loadSubjects', methods=['GET'])
def load_subjects():
    return json.dumps(retrieve_teacher_particular_subjects(get_teacher_id_using_name(session.get('username'))))


@app.route('/studentSelected', methods=['POST', 'GET'])
def load_selected_students():
    classe = request.get_json()
    session_admitted = str(classe['session_admitted'])
    print(session_admitted)
    return retrieve_selected_students(session_admitted)


@app.route('/startStudentScoreRecord', methods=['POST', 'GET'])
def start_student_score_record():
    try:
        student_details = request.get_json()
        student_id = str(student_details['student_id'])
        session_name = str(student_details['session_name'])
        subject_id = str(student_details['subject_id'])
        session_admitted = str(student_details['session_admitted'])
        term = str(student_details['term'])
        return jsonify(insert_student_instance_into_scores(student_id, session_name, subject_id, session_admitted, term))
    except Exception as e:
        print(e)


@app.route('/submitScore', methods=['POST', 'GET'])
def submit_score():
    score_details = request.get_json()
    student_id = str(score_details['student_id'])
    subject_name = str(score_details['subject_name'])
    test_1 = str(score_details['test_1'])
    test_2 = str(score_details['test_2'])
    test_3 = str(score_details['test_3'])
    exam = str(score_details['exam'])
    class_name = str(score_details['class_name'])
    term_name = str(score_details['term_name'])
    cumulative = str(score_details['cumulative'])
    session_name = str(score_details['session_nam'])
    session_admitted = get_student_session_admitted(student_id)
    insert_score(student_id, subject_name, test_1, test_2, test_3, exam, class_name, term_name, cumulative,
                 session_name, session_admitted)
    return 'success'


@app.route('/getSubjectResult', methods=['POST', 'GET'])
def get_subject_result():
    try:
        result_query_details = request.get_json()
        student_id = str(result_query_details['student_id'])
        term = str(result_query_details['term'])
        session_name = str(result_query_details['session_nam'])
        session_admitted = str(result_query_details['session_admitted'])
        term_scores = jsonify(retrieve_term_scores(student_id, term, session_name, session_admitted))
        return term_scores
    except Exception as e:
        print(e.with_traceback())
    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
