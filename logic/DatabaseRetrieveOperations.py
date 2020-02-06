from flask import json, jsonify
from DBConn import connection
from models.Student import Student
from models.Student_Score import Student_Score
from models.Subject_Result import Subject_Result


def retrieve_sessions():
    c, conn = connection()
    c.execute("SELECT * FROM sessions")
    data = c.fetchall()
    sessions = []
    for session in data:
        id_ = session[0]
        name = session[1]
        sessions.append({'id': id_, 'name': name})
    c.close()
    conn.close()
    return sessions


def retrieve_classes():
    c, conn = connection()
    c.execute("SELECT * FROM class_db")
    data = c.fetchall()
    classes = []
    for classe in data:
        id_ = classe[0]
        name = classe[1]
        classes.append({'id': id_, 'name': name})
    c.close()
    conn.close()
    return classes


def retrieve_teacher_particular_subjects(teacher_id):
    c, conn = connection()
    c.execute("SELECT * FROM subjects WHERE teacher_id = %s", teacher_id)
    data = c.fetchall()
    subjects = []
    for subject in data:
        id_ = subject[0]
        name = subject[1]
        subjects.append({'id': id_, 'name': name})
    c.close()
    conn.close()
    return subjects


def get_teacher_id_using_name(username):
    c, conn = connection()
    c.execute("SELECT id FROM teachers WHERE username = %s", username)
    data = c.fetchone()
    id_ = data
    return id_


def retrieve_selected_students(session_admitted):
    c, conn = connection()
    c.execute("SELECT DISTINCT id, student_name FROM student WHERE session_admitted = %s",
              session_admitted)
    data = c.fetchall()
    selected_students = []
    for student in data:
        new_student = Student(student[0], student[1])
        selected_students.append(new_student.toJSON())
    conn.close()
    c.close()
    print(selected_students)
    return json.dumps(selected_students)


def get_student_session_admitted(student_id):
    c, conn = connection()
    c.execute("SELECT session_admitted FROM student WHERE id = %s", student_id)
    data = c.fetchone()
    c.close()
    conn.close()
    return data[0]


def retrieve_student_id_using_name(student_name):
    c, conn = connection()
    c.execute("SELECT id FROM student WHERE student_name = %s", student_name)
    data = c.fetchone()
    c.close()
    conn.close()
    return data[0]


def retrieve_student_name_with_id(id_):
    c, conn = connection()
    c.execute("SELECT student_name FROM student WHERE id = %s", id_)
    data = c.fetchone()
    c.close()
    conn.close()
    return data[0]


def retrieve_class_name(student_id, session_name):
    c, conn = connection()
    c.execute("SELECT class_name FROM scores WHERE student_id = %s AND session_name = %s", (student_id, session_name))
    data = c.fetchone()
    c.close()
    conn.close()
    print(data[0])
    return str(data[0])


def retrieve_term_scores(student_id, term, session_name, session_admitted):
    c, conn = connection()
    if term == '1':
        c.execute("SELECT student_id, subject_id, 1st_test_1, 1st_test_2, 1st_test_3, 1st_exam, 1st_cumm FROM scores "
                  "WHERE student_id = %s AND session_name = %s ORDER BY subject_id",
                  (retrieve_student_id_using_name(student_id), session_name))
        data = c.fetchall()
        subject_score_list = []
        term_percent = retrieve_term_percentage(retrieve_student_id_using_name(student_id), session_name, term)
        for subject_result in data:
            subject_result_object = Subject_Result(subject_result[0], subject_result[1], subject_result[2],
                                                   subject_result[3], subject_result[4], subject_result[5],
                                                   subject_result[6], subject_result[6], '', term, term_percent,
                                                   '')
            class_name = retrieve_class_name(retrieve_student_id_using_name(student_id), session_name)
            print(class_name)
            subject_result_object_json = subject_result_object.toJSON(class_name, session_name)
            subject_score_list.append(subject_result_object_json)
        print(subject_score_list)
        return subject_score_list

    if term == '2':
        c.execute("SELECT student_id, subject_id, 2nd_test_1, 2nd_test_2, 2nd_test_3, 2nd_exam, 2nd_cumm, 1st_cumm "
                  "FROM scores WHERE student_id = %s AND session_name = %s ORDER BY subject_id",
                  (retrieve_student_id_using_name(student_id), session_name))
        data = c.fetchall()
        subject_score_list = []
        term_percent = retrieve_term_percentage(retrieve_student_id_using_name(student_id), session_name, term)
        for subject_result in data:
            subject_result_object = Subject_Result(subject_result[0], subject_result[1], subject_result[2],
                                                   subject_result[3], subject_result[4], subject_result[5],
                                                   int((int(subject_result[6]) + int(subject_result[7])) / 2),
                                                   subject_result[6], subject_result[7], term, term_percent, '')
            class_name = retrieve_class_name(retrieve_student_id_using_name(student_id), session_name)
            print(class_name)
            subject_result_object_json = subject_result_object.toJSON(class_name, session_name)
            subject_score_list.append(subject_result_object_json)
        print(subject_score_list)
        return subject_score_list

    if term == '3':
        c.execute("SELECT student_id, subject_id, 3rd_test_1, 3rd_test_2, 3rd_test_3, 3rd_exam, 3rd_cumm, 2nd_cumm, "
                  "1st_cumm FROM scores WHERE student_id = %s AND session_name = %s ORDER BY subject_id",
                  (retrieve_student_id_using_name(student_id), session_name))
        data = c.fetchall()
        subject_score_list = []
        term_percent = retrieve_term_percentage(retrieve_student_id_using_name(student_id), session_name, term)
        class_position = retrieve_class_position(str(retrieve_student_id_using_name(student_id)), session_name,
                                                 session_admitted) + 1

        if class_position == 1:
            class_position = '1st'
        if class_position == 2:
            class_position = '2nd'
        if class_position == 3:
            class_position = '3rd'
        if class_position in range(4, len(data) + 1):
            class_position = str(class_position) + 'th'

        for subject_result in data:
            subject_result_object = Subject_Result(subject_result[0], subject_result[1], subject_result[2],
                                                   subject_result[3], subject_result[4], subject_result[5],
                                                   subject_result[6],
                                                   int((int(subject_result[6]) + int(subject_result[7]) +
                                                        int(subject_result[8])) / 3),
                                                   subject_result[7],
                                                   term, term_percent, class_position)

            print(student_id, session_name, session_admitted)
            class_name = retrieve_class_name(retrieve_student_id_using_name(student_id), session_name)
            print(class_name)
            subject_result_object_json = subject_result_object.toJSON(class_name, session_name)
            subject_score_list.append(subject_result_object_json)
        print(subject_score_list)
        return subject_score_list


# retrieve_term_scores('Otolorin Olabode', '3', '2013//2014', '2013//2014')


def get_teacher_id_from_subject_table(subject_name):
    c, conn = connection()
    c.execute("SELECT teacher_id FROM subjects WHERE subject_name = %s", subject_name)
    data = c.fetchone()
    c.close()
    conn.close()
    return data


def retrieve_teacher_using_subject(subject_name):
    c, conn = connection()
    c.execute("SELECT teacher_name FROM teachers WHERE id = %s", get_teacher_id_from_subject_table(subject_name))
    data = c.fetchone()
    c.close()
    conn.close()
    return data[0]


def retrieve_class_average_for_each_subject(session_name, class_name, subject_id, term):
    c, conn = connection()
    if term == '1':
        c.execute("SELECT AVG(1st_cumm) FROM scores WHERE session_name = %s AND class_name = %s AND "
                  "subject_id = %s", (session_name, class_name, subject_id))
        data = c.fetchone()
        return data[0]
        c.close()
        conn.close()
    if term == '2':
        c.execute("SELECT AVG(2nd_cumm) FROM scores WHERE session_name = %s AND class_name = %s AND "
                  "subject_id = %s", (session_name, class_name, subject_id))
        data = c.fetchone()
        return data[0]
        c.close()
        conn.close()
    if term == '3':
        c.execute("SELECT AVG(3rd_cumm) FROM scores WHERE session_name = %s AND class_name = %s AND "
                  "subject_id = %s", (session_name, class_name, subject_id))
        data = c.fetchone()
        return data[0]
        c.close()
        conn.close()


# This parameter should carry term later as we would be using just one method fot the three terms
def retrieve_term_position_for_each_student_in_every_subject(student_id, class_name, subject, session, term):
    try:
        global position
        global position_
        if term == '1':
            c, conn = connection()
            c.execute("SELECT student_id, 1st_cumm FROM scores WHERE subject_id = %s AND session_name = %s AND "
                      "class_name = %s ORDER BY 1st_cumm DESC", (subject, session, class_name))
            data = c.fetchall()
            scores = []
            for item in data:
                scores.append({'student_id': item[0], 'score': item[1]})
            i = 1
            for score in scores:
                print(score)
                if score['student_id'] == student_id:
                    position = i
                    print(position)
                i += 1

            if position == 1:
                position_ = '1st'
            if position == 2:
                position_ = '2nd'
            if position == 3:
                position_ = '3rd'
            if position in range(4, len(scores) + 1):
                position_ = str(position) + 'th'

            return position_

        if term == '2':
            c, conn = connection()
            c.execute("SELECT student_id, 2nd_cumm FROM scores WHERE subject_id = %s AND session_name = %s AND "
                      "class_name = %s ORDER BY 2nd_cumm DESC", (subject, session, class_name))
            data = c.fetchall()
            scores = []
            for item in data:
                scores.append({'student_id': item[0], 'score': item[1]})
            i = 1
            for score in scores:
                print(score)
                if score['student_id'] == student_id:
                    position = i
                    print(position)
                i += 1

            if position == 1:
                position_ = '1st'
            if position == 2:
                position_ = '2nd'
            if position == 3:
                position_ = '3rd'
            if position in range(4, len(scores) + 1):
                position_ = str(position) + 'th'

            return position_

        if term == '3':
            c, conn = connection()
            c.execute("SELECT student_id, 3rd_cumm FROM scores WHERE subject_id = %s AND session_name = %s AND "
                      "class_name = %s ORDER BY 3rd_cumm DESC", (subject, session, class_name))
            data = c.fetchall()
            scores = []
            for item in data:
                scores.append({'student_id': item[0], 'score': item[1]})
            i = 1
            for score in scores:
                print(score)
                if score['student_id'] == student_id:
                    position = i
                    print(position)
                i += 1

            if position == 1:
                position_ = '1st'
            if position == 2:
                position_ = '2nd'
            if position == 3:
                position_ = '3rd'
            if position in range(4, len(scores) + 1):
                position_ = str(position) + 'th'

            return position_

            c.close()
            conn.close()

    except Exception as e:
        return e


def retrieve_no_of_students_in_class(class_name):
    c, conn = connection()
    c.execute("SELECT COUNT(DISTINCT student_id) FROM scores WHERE class_name = %s", class_name)
    data = c.fetchone()
    c.close()
    conn.close()
    return data[0]


def retrieve_class_position(student_id_, session_name, session_admitted):

    c, conn = connection()
    c.execute("SELECT student_id, 1st_cumm, 2nd_cumm, 3rd_cumm FROM scores WHERE session_name = %s "
              "AND session_admitted = %s", (session_name, session_admitted))
    data = c.fetchall()
    c.close()
    conn.close()
    new_data_list = []
    student_list = []
    for student_ in data:
        new_data_list.append({'student_id': student_[0], 'cumm_av_each_subj': int((int(student_[1]) + int(student_[2]) +
                                                                                  int(student_[3])) / 3)})
        if student_[0] in student_list:
            pass
        else:
            student_list.append(student_[0])
    every_student_total = []
    global total_sum, student, student_id_global, student_score, student_position

    for std in student_list:
        total_sum = 0
        for student in new_data_list:
            if student['student_id'] == std:
                total_sum += int(student['cumm_av_each_subj'])
                student_id_global = student['student_id']
        student_score = Student_Score(student_id_global, total_sum)
        every_student_total.append(student_score)

    every_student_total.sort(key=Student_Score.getkey, reverse=True)

    global index, student_position
    index = 0
    student_position = 0
    for student_score_1 in every_student_total:
        if student_score_1.student_id == student_id_:
            student_position = index
            print(index)
        index += 1
    print(student_position)
    return student_position


def retrieve_term_percentage(student_id, session_name, term):
    c, conn = connection()
    c.execute("SELECT DISTINCT subject_id from scores WHERE student_id = %s AND session_name = %s", (student_id,
                                                                                                     session_name))
    data = c.fetchall()
    print('Subject Number Part')
    print(data)
    no_of_subjects = len(data)
    return get_percent_figures(session_name, student_id, term, no_of_subjects)


def get_percent_figures(session_name, student_id, term, no_of_subjects):
    c, conn = connection()

    global total_score
    total_score = 0

    if term == '1':
        c.execute("SELECT student_id, 1st_cumm FROM scores WHERE session_name = %s "
                  "AND student_id = %s", (session_name, student_id))
        data = c.fetchall()
        print('Scores PArt')
        print(data)
        c.close()
        conn.close()
        for score in data:
            total_score += int(score[1])

    if term == '2':
        c.execute("SELECT student_id, 2nd_cumm FROM scores WHERE session_name = %s "
                  "AND student_id = %s", (session_name, student_id))
        data = c.fetchall()
        print('Scores PArt')
        print(data)
        c.close()
        conn.close()
        for score in data:
            total_score += int(score[1])

    if term == '3':
        c.execute("SELECT student_id, 3rd_cumm FROM scores WHERE session_name = %s "
                  "AND student_id = %s", (session_name, student_id))
        data = c.fetchall()
        print('Scores PArt')
        print(data)
        c.close()
        conn.close()
        for score in data:
            total_score += int(score[1])

    return str(total_score/no_of_subjects) + str('%')


# retrieve_term_percentage('2', '2013//2014', 2)
