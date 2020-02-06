from DBConn import connection


def insert_class(class_name, teacher_id):
    c, conn = connection()
    c.execute("INSERT INTO class_db(class_name, teacher_id) VALUES (%s, %s)", (class_name, teacher_id))
    conn.commit()
    print('CLASS SUCCESSFULLY INSERTED INTO THE DATABASE')
    c.close()
    conn.close()


def insert_session(session_name):
    c, conn = connection()
    c.execute("INSERT INTO sessions (session_name) VALUES (%s)", session_name)
    conn.commit()
    print('SESSION SUCCESSFULLY INSERTED INTO THE DATABASE')
    c.close()
    conn.close()


def insert_teacher(teacher_name, username, password, admin):
    c, conn = connection()
    c.execute("INSERT INTO teachers (teacher_name, username, password, admin) VALUES (%s, %s, %s, %s)",
              (teacher_name, username, password, admin))
    print('TEACHER SUCCESS FULLY ADDED TO THE DATABASE')
    conn.commit()
    c.close()
    conn.close()


def insert_subject(subject_name, teacher_id):
    c, conn = connection()
    c.execute("INSERT INTO subjects (subject_name, teacher_id) VALUES (%s, %s)", (subject_name, teacher_id))
    print('SUBJECT SUCCESS FULLY ADDED TO THE DATABASE')
    conn.commit()
    c.close()
    conn.close()


def insert_student(student_name, session_admitted):
    c, conn = connection()
    c.execute("INSERT INTO student (student_name, session_admitted) VALUES (%s, %s)", (student_name, session_admitted))
    print('STUDENT SUCCESS FULLY ADDED TO THE DATABASE')
    conn.commit()
    c.close()
    conn.close()


def insert_student_instance_into_scores(student_id, session_name, subject_id, session_admitted, term):
    global scores
    try:
        c, conn = connection()
        c.execute("SELECT student_id FROM scores WHERE student_id = %s AND session_name = %s AND subject_id = %s "
                  "AND session_admitted = %s", (student_id, session_name, subject_id, session_admitted))
        data = c.fetchall()
        if len(data) == 0:
            c.execute("INSERT INTO scores (student_id, session_name, subject_id, session_admitted) VALUES "
                      "(%s, %s, %s, %s)", (student_id, session_name, subject_id, session_admitted))
            conn.commit()
            return 'success in inserting'
        else:
            print('Else here')
            if term == '1':
                c.execute("SELECT class_name, 1st_test_1, 1st_test_2, 1st_test_3, 1st_exam FROM scores WHERE "
                          "student_id = %s AND subject_id = %s AND session_admitted = %s AND session_name = %s",
                          (student_id, subject_id, session_admitted, session_name))
                data = c.fetchall()
                scores = {'class_name': data[0][0], 'first_test': data[0][1], 'second_test': data[0][2],
                          'third_test': data[0][3], 'exam': data[0][4]}
                print(scores)
            if term == '2':
                c.execute("SELECT class_name, 2nd_test_1, 2nd_test_2, 2nd_test_3, 2nd_exam FROM scores WHERE "
                          "student_id = %s AND subject_id = %s AND session_admitted = %s AND session_name = %s",
                          (student_id, subject_id, session_admitted, session_name))
                data = c.fetchall()
                scores = {'class_name': data[0][0], 'first_test': data[0][1], 'second_test': data[0][2],
                          'third_test': data[0][3], 'exam': data[0][4]}
            if term == '3':
                c.execute("SELECT class_name, 3rd_test_1, 3rd_test_2, 3rd_test_3, 3rd_exam FROM scores WHERE "
                          "student_id = %s AND subject_id = %s AND session_admitted = %s AND session_name = %s",
                          (student_id, subject_id, session_admitted, session_name))
                data = c.fetchall()
                scores = {'class_name': data[0][0], 'first_test': data[0][1], 'second_test': data[0][2],
                          'third_test': data[0][3], 'exam': data[0][4]}
    except Exception as e:
        return e
    return scores


def insert_score(student_id, subject_id, Test_1, Test_2, Test_3, Exam, class_name, term_name, cum, session_name,
                 session_admitted):
    if term_name == '1':
        c, conn = connection()
        c.execute("UPDATE scores SET session_admitted = %s, class_name = %s, 1st_test_1 = %s, 1st_test_2 = %s, "
                  "1st_test_3 = %s, 1st_exam = %s, 1st_cumm = %s WHERE student_id = %s AND session_name = %s AND "
                  "subject_id = %s", (session_admitted, class_name, Test_1, Test_2, Test_3, Exam, cum, student_id,
                                      session_name, subject_id))
        print('SCORE SUCCESSFULLY ADDED TO THE DATABASE')
        conn.commit()
        c.close()
        conn.close()

    if term_name == '2':
        c, conn = connection()
        c.execute("UPDATE scores SET 2nd_test_1 = %s, 2nd_test_2 = %s, 2nd_test_3 = %s, 2nd_exam = %s, 2nd_cumm = %s "
                  "WHERE student_id = %s AND session_name = %s AND subject_id = %s",
                  (Test_1, Test_2, Test_3, Exam, cum, student_id, session_name, subject_id))
        print('SCORE SUCCESS FULLY ADDED TO THE DATABASE')
        conn.commit()
        c.close()
        conn.close()

    if term_name == '3':
        c, conn = connection()
        c.execute("UPDATE scores SET 3rd_test_1 = %s, 3rd_test_2 = %s, 3rd_test_3 = %s, 3rd_exam = %s, 3rd_cumm = %s "
                  "WHERE student_id = %s AND session_name = %s AND class_name = %s AND subject_id = %s",
                  (Test_1, Test_2, Test_3, Exam, cum, student_id, session_name, class_name, subject_id))
        print('SCORE SUCCESS FULLY ADDED TO THE DATABASE')
        conn.commit()
        c.close()
        conn.close()
