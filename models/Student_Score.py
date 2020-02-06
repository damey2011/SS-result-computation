class Student_Score:
    def __init__(self, student_id, score):
        self.student_id = student_id
        self.score = score

    def __repr__(self):
        return '{}: {} {}'.format(self.__class__.__name__, self.student_id, self.score)

    def getkey(self):
        return self.score
