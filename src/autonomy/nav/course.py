class Course:
    def __init__(self):
        self.marks = []

    def __iter__(self):
        return CourseIterator(self)

    def add_mark(self, mark):
        """Adds a mark to the course"""
        if len(self.marks) == 0:
            self.marks.append(mark)
            self.marks.append(mark)
        else:
            last_mark = self.marks.pop()
            self.marks.append(mark)
            self.marks.append(last_mark)

    def clear(self):
        self.marks = []

class Path:
    def __init__(self):
        self.marks = []

    def __iter__(self):
        return CourseIterator(self)

    def prepend_mark(self, mark):
        """Prepends mark to the course"""
        self.marks = [mark,] + self.marks[:]

    def add_mark(self, mark):
        """Adds a mark to the path"""
        self.marks.append(mark)

    def next_mark(self):
        """Returns next mark in path"""
        if len(self.marks) > 0:
            return self.marks[0]
        else:
            return None

    def clear(self):
        self.marks = []

class CourseIterator:
    def __init__(self, course):
        self.index = 0
        self.course = course

    def __next__(self):
        return self.next_mark()

    def current_mark(self):
        """Gets the current mark"""
        return self.course.marks[self.index]

    def next_mark(self):
        """Gets the next mark"""
        self.index += 1
        self.index %= len(self.course.marks)
        return self.course.marks[self.index]
