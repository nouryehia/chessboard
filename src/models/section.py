from app import db

# TODO: Need method in EnrolledCourse that looks like this:
# def find_students_in_section(self, given_id: int):
#   records = EnrolledCourse.query.filter_by(section_id=given_id).all()
#   for rec in records:
#       user_ids.add(rec.user_id)
#
#   for id in user_ids:
#       student = User.find_student_by_id(id)
#       students.add(student.first_name + " " + student.last_name)
#
#   return students

# TODO: Need method in User that looks like this:
# def find_student_by_id(self, given_id: int):
#   return Users.query.filter_by(id=given_id).first()


class Section(db.Model):
    """
    Represents a section in the DB with relevant functions for
    creating a section, adding users to it, sorting the members in a
    section so that their grades can be released, and finding a section
    by its id.\n
    IMPORTANT NOTE: Everytime a section is used if it was not just
    constructed, update_section must be called. Also you must make sure a
    course exists before you try to create a section.\n

    Fields:
    id --> Section ID within table. Unique, primary key.\n
    section_name --> Section name.\n
    section_id --> Section id (webreg id - may not be unique).\n
    course_id --> Course id to the course that the section is in.
    Foreign key to courses table.\n
    @author: sccontre\n
    """

    __tablename__ = 'Section'
    id = db.Column(db.bigint(20), primary_key=True, nullable=False)
    section_name = db.Column(db.String(255), nullable=False)
    section_id = db.Column(db.bigint(20), nullable=False)
    course_id = db.Column(db.bigint(20), db.ForeignKey('Course.id'),
                          nullable=False)

    def __init__(self, **kwargs):
        '''
        Constructs the section object by delegating to Model. Also creates
        a class variable that holds the names of all of the students within
        the course so that the students can be listed\n
        Params: None.\n
        Returns: None.\n
        '''

        # Initialize the object
        super(Section, self).__init__(**kwargs)

        # Find all the students in the section using a database query
        # that returns a set of strings in the format of "First Last"
        self.students_in_section =\
            EnrolledCourse.find_students_in_section(self.id)

    def update_section(self):
        '''
        Updates the object's instance field students_in_section so that any
        added or dropped students are filled into the set. Important because
        python does not allow these instance fields to be kept after an object
        goes out of scope.\n
        Params: None.\n
        Returns: Self.\n
        '''

        # Find all the students in the section by delegating to EnrolledCourse
        updated_students_in_section =\
            EnrolledCourse.find_students_in_section(self.id)

        # Clear old set of students in section
        self.students_in_section.clear()

        # Update set of students
        for student in updated_students_in_section:
            self.students_in_section.add(student)

        return self

    def __repr__(self):
        '''
        Returns the name of the section.\n
        Params: None.\n
        Returns: Name of the section.\n
        '''

        return self.section_name

    def sort_students(self, set_of_students: set):
        '''
        Sorts a set of students alphabetically so that they can be printed out
        whenever we want a list of students.\n
        This list of students does not have to be all the students in the
        section hence the parameter that can be passed as a different list.\n
        If you want to get a list of all of the students in the section, simply
        call this function with param Section.students_in_section.\n
        Params: A set of student names (strings) that needs to be sorted and
        passed back.\n
        Returns: Ordered list of students.\n
        '''

        # Create a list out of the set
        to_be_sorted = list(set_of_students)

        # Sort list alphabetically because it is simply a set of strings and
        # return the result
        to_be_sorted.sort()
        return to_be_sorted

    def find_by_id(self, section_id: int, course_id: int):
        '''
        Performs a database query by the course and section id.\n
        Params: None.\n
        Returns: The section if it is found, none otherwise.\n
        '''

        # Filter by section id and course id because section_id is not unique
        # on its own - return the first (and only) occurrence in table
        section = Section.query.\
            filter_by(section_id=section_id, course_id=course_id).first()

        return section
