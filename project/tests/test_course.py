from project.src.models.course import Course

# Courses
test_course_ninety = {'description':'this is a cool course', 'name':'CSE 9090', 'quarter':1, 
                    'short_name':'9090', 'url': 'https://acmucsd.com/', 'year':2022,
                    'active':True, 'queue_enabled':True,'cse':True,'queue_id':1,'instructor_id':1}
test_course_math = {'description':'m4th', 'name':'math is cool', 'quarter':1, 
                    'short_name':'20C', 'url': 'https://acmucsd.com/', 'year':2022,
                    'active':True, 'queue_enabled':True,'cse':False,'queue_id':1,'instructor_id':1}

# Tests
## Methods used in the controller
def test_create_course():
    course = Course.create_course('this is a cool course','CSE 9090',1,'9090','https://acmucsd.com/',2022,True,True,True,1,1)
    course_math = Course.create_course('m4th', 'math is cool', 1, '20C', 'https://acmucsd.com/', 2022,True, True,False,1,1)

    # test had just run so this course exists already (so it is equal to None)
    if(course != None):
        assert course.year == test_course_ninety['year'] and course.url == test_course_ninety['url']
        # test quarter params
        qtr = course.quarter_year()
        assert qtr == 'WI2022'
        course.is_deleted = False
    else:
        a = Course.exists_course(test_course_ninety['quarter'], test_course_ninety['short_name'], test_course_ninety['year'])
        a.is_deleted = False

    if(course_math != None):
        assert course_math.year == test_course_math['year'] and course_math.url == test_course_math['url']
        course_math.is_deleted = False
    else:
        a = Course.exists_course(test_course_math['quarter'], test_course_math['short_name'], test_course_math['year'])
        a.is_deleted = False

def test_exists_course():
    course = Course.exists_course(1,'9090',2022)
    assert course.description == 'this is a cool course'

def test_get_all_courses():
    all_courses = Course.get_all_courses()
    a = Course.exists_course(test_course_ninety['quarter'], test_course_ninety['short_name'], test_course_ninety['year'])
    b = Course.exists_course(test_course_math['quarter'], test_course_math['short_name'], test_course_math['year'])
    print(a)
    assert all_courses.index(a)
    assert all_courses.index(b)

def test_delete_course():
    course = Course.create_course('this is a cool course','CSE 9090',1,'9090','https://acmucsd.com/',2022,True,True,True,1,1)
    # if the course was previously created
    if(course == None):
        Course.delete_course(quarter=test_course_ninety['quarter'], short_name=test_course_ninety['short_name'], year=test_course_ninety['year'])
        all_courses = Course.get_all_courses()
        a = Course.exists_course(test_course_ninety['quarter'], test_course_ninety['short_name'], test_course_ninety['year'])
        assert a.is_deleted