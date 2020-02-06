from DBConn import connection


def getAll():
    c, conn = connection()
    teachers = []
    c.execute("SELECT id, teacher_name FROM teachers")
    data = c.fetchall()
    for data_item in data:
        teachers.append({'teacher_id': data_item[0], 'teacher_name': data_item[1]})
    conn.close()
    c.close()
    return teachers
