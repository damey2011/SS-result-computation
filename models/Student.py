class Student:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name

    def toJSON(self):
        return {'id': self.id, 'name': self.name}
