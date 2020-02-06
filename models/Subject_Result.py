
def calculate_grade(cumm):
    if int(cumm) > 74:
        return 'A'
    elif 64 < int(cumm) < 75:
        return 'B'
    elif 54 < int(cumm) < 65:
        return 'C'
    elif 44 < int(cumm) < 55:
        return 'D'
    elif 40 < int(cumm) < 45:
        return 'E'
    elif int(cumm) < 40:
        return 'F'
    return ''


class Subject_Result:
    def __init__(self, student_id, subject, test_1, test_2, test_3, exam, cum, av_cum, last_cum, term, total_aver,
                 final_position):
        self.student_id = student_id
        self.subject = subject
        self.test_1 = test_1
        self.test_2 = test_2
        self.test_3 = test_3
        self.exam = exam
        self.cum = cum
        self.av_cum = av_cum
        self.last_cum = last_cum
        self.term = term
        self.total_aver = total_aver
        self.final_position = final_position

    def toJSON(self, class_name, session_name):
        from logic.DatabaseRetrieveOperations import retrieve_teacher_using_subject
        from logic.DatabaseRetrieveOperations import retrieve_class_average_for_each_subject
        from logic.DatabaseRetrieveOperations import retrieve_term_position_for_each_student_in_every_subject
        from logic.DatabaseRetrieveOperations import retrieve_student_name_with_id
        from logic.DatabaseRetrieveOperations import retrieve_no_of_students_in_class

        return {'student_id': self.student_id, 'student_name': retrieve_student_name_with_id(self.student_id),
                'no_of_students_in_class': retrieve_no_of_students_in_class(class_name),
                'subject': self.subject, 'test_1': self.test_1, 'test_2': self.test_2,
                'test_3': self.test_3, 'exam': self.exam, 'cum': self.cum, 'av_cum': self.av_cum,
                'last_cum': self.last_cum, 'grade': calculate_grade(self.cum),
                'teacher_name': retrieve_teacher_using_subject(self.subject),
                'class_av': int(retrieve_class_average_for_each_subject(session_name, class_name, self.subject,
                                                                        self.term)),
                'position': retrieve_term_position_for_each_student_in_every_subject(self.student_id, class_name,
                                                                                     self.subject, session_name,
                                                                                     self.term),
                'class_name': class_name,
                'session_name': session_name,
                'total_aver': self.total_aver,
                'final_position': self.final_position}
