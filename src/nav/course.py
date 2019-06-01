class Course:
    def __init__(self):
        self.legs = []

    def __iter__(self):
        return CourseIterator(self)

    def add_mark(self, mark):
        """Adds a mark to the course"""
        first_mark = mark
        next_to_last_mark = mark
        if len(self.legs) > 0:
            first_mark = self.legs[0][0]
            next_to_last_mark = self.legs[len(self.legs) - 1][1]
            self.legs.pop()  # Remove previous link leg
        last_mark = mark

        self.legs.append((next_to_last_mark, last_mark))
        self.legs.append((last_mark, first_mark))

    def clear(self):
        self.legs = []


class Path:
    def __init__(self):
        self.legs = []

    def __iter__(self):
        return CourseIterator(self)

    def add_mark(self, mark):
        """Adds a mark to the path"""
        next_to_last_mark = mark
        if len(self.legs) > 0:
            next_to_last_mark = self.legs[len(self.legs) - 1][1]
        last_mark = mark

        self.legs.append((next_to_last_mark, last_mark))


class CourseIterator:
    def __init__(self, course):
        self.index = 0
        self.course = course

    def __next__(self):
        return self.next_leg()

    def current_leg(self):
        """Gets the next leg"""
        return self.course.legs[self.index]

    def next_leg(self):
        """Gets the next leg"""
        self.index += 1
        self.index %= len(self.course.legs)
        return self.course.legs[self.index]
