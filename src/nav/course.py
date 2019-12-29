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

class ObjectCourse:
    def __init__(self):
        self.objs = []

    def __iter__(self):
        return ObjectCourseIterator(self)

    def add_obj(self, obj):
        """
        Adds an object to the course
        Inputs:
            obj -- object to be added to object course
        Side Effects:
            objs -- object is inserted at end of loop
        """
        first_obj = obj
        next_to_last_obj = obj
        if len(self.objs) > 0:
            first_obj =  self.objs[0][0]
            next_to_last_obj = self.objs[-1][1]
            self.objs.pop()
        last_obj = obj

        self.objs.append((next_to_last_obj, last_obj))
        self.objs.append((last_obj, first_obj))

    def clear(self):
        """
        Empties objs
        Side Effects:
            objs -- clears objs
        """
        self.objs = []

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

class ObjectCourseIterator:
    def __init__(self, obj_course):
        self.index = 0
        self.obj_course = obj_course

    def __next__(self):
        return self.next_leg()

    def next_leg(self):
        """
        Gets the next leg
        Returns:
            next_leg -- next leg (object) on course
        """
        self.index += 1
        self.index %= len(self.obj_course.objs)
        return self.course.objs[self.index]
        
