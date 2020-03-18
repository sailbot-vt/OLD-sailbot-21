import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from src.autonomy.nav.course import Course

class CourseTests(unittest.TestCase):
    """Tests the methods in Course"""
    def setUp(self):
        self.course = Course()

    def test_add_mark(self):
        """Tests add mark method of Course"""
        # check that list is empty
        self.assertEqual(0, len(self.course.marks))
        
        # generate list of objects
        rng_list = [50, 70, 70, 50]
        bearing_list = [5, 50, 140, 175]

        mark_list = [(r, bearing) for r, bearing in zip(rng_list, bearing_list)]

        # add objects to course (one by one) and check that course updates correctly
        # add first object
        self.course.add_mark(mark_list[0])
        self.assertEqual(2, len(self.course.marks))      # list length should be two
        self.assertEqual(mark_list[0], self.course.marks[0])
        self.assertEqual(mark_list[0], self.course.marks[1])

        # add 2nd object
        self.course.add_mark(mark_list[1])
        self.assertEqual(3, len(self.course.marks))      # list length should be three 
        self.assertEqual(mark_list[0], self.course.marks[0])
        self.assertEqual(mark_list[1], self.course.marks[1])
        self.assertEqual(mark_list[0], self.course.marks[2])

        # add 3rd object
        self.course.add_mark(mark_list[2])
        self.assertEqual(4, len(self.course.marks))      # list length should be four 
        self.assertEqual(mark_list[0], self.course.marks[0])
        self.assertEqual(mark_list[1], self.course.marks[1])
        self.assertEqual(mark_list[2], self.course.marks[2])
        self.assertEqual(mark_list[0], self.course.marks[3])

        # add 4th object
        self.course.add_mark(mark_list[3])
        self.assertEqual(5, len(self.course.marks))      # list length should be five 
        self.assertEqual(mark_list[0], self.course.marks[0])
        self.assertEqual(mark_list[1], self.course.marks[1])
        self.assertEqual(mark_list[2], self.course.marks[2])
        self.assertEqual(mark_list[3], self.course.marks[3])
        self.assertEqual(mark_list[0], self.course.marks[4])

    def test_clear(self):
        """Tests clear method of Object Course"""

        # add elements to objs in Object Course
        self.course.marks = [x for x in range(5)]

        self.assertEqual(5, len(self.course.marks))      # list length should be five 

        # clear list
        self.course.clear()

        self.assertEqual(0, len(self.course.marks))      # list length should be zero 
