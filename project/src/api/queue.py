from flask_cors import CORS
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from ..models.ticket import HelpType, TicketTag
from ..models.queue import Queue, Status
from ..models.enrolled_course import EnrolledCourse, Role
from ..models.course import Course
from ..models.ticket import Status as t_Status
from ..models.queue_calendar import QueueCalendar

queue_api_bp = Blueprint('queue_api', __name__)
CORS(queue_api_bp, supports_credentials=True)


def user_in_course(queue_id: int, course_id: int) -> bool:
    """
    Checking whether the user is enrolled in the course.
    """
    course = Course.get_course_by_queue_id(queue_id)
    c_u_id = current_user.id
    if EnrolledCourse.find_user_in_course(user_id=c_u_id,
                                          course_id=course.id):
        return True
    else:
        return False


def user_own_queue(queue_id: int, course_id: int) -> bool:
    """
    Checkin gwhetehr the user is the instructor of the course
    that has this queue.
    """
    course = Course.get_course_by_queue_id(queue_id)
    c_u_id = current_user.id
    ec_entry = EnrolledCourse.find_user_in_course(user_id=c_u_id,
                                                  course_id=course.id)
    if ec_entry:
        if ec_entry.role == Role.INSTRUCTOR.value:
            return True
    return False


@queue_api_bp.route('/find_queue', methods=['GET'])
@login_required
def find_queue():
    """
    Return the queue object corresponding to an id.\n
    @authoer: YixuanZhou
    """
    queue_id = (int(request.json['queue_id']) if 'queue_id' in request.json
                else None)
    if not queue_id:
        return jsonify({'reason': 'queue_id invalid'}), 400

    if not user_in_course:
        return jsonify({'reason': 'user not enrolled'}), 400

    queue = Queue.get_queue_by_id(queue_id)

    if not queue:
        return jsonify({'reason': 'queue not found'}), 400

    ret = {'reason': 'success', 'result': queue.to_json()}
    return jsonify(ret), 200


@queue_api_bp.route('/create_queue', methods=['POST'])
@login_required
# @role_required(role=URole.ADMIN.value)
def create_queue():
    """
    Create a queue for a course.\n
    """
    hce = bool(request.json['high_capacity_enabled']) if \
        'high_capacity_enabled' in request.json else None
    hct = int(request.json['high_capacity_threshold']) if \
        'high_capacity_threshold' in request.json else None
    hcm = request.json['high_capacity_message'] if \
        'high_capacity_message' in request.json else None
    hcw = request.json['high_capacity_warning'] if \
        'high_capacity_warning' in request.json else None
    tc = int(request.json['ticket_cooldown']) if \
        'ticket_cooldown' in request.json else None
    q = Queue(status=Status.CLOSED.value,
              high_capacity_enable=hce,
              high_capacity_threshold=hct,
              high_capacity_message=hcm,
              high_capacity_warning=hcw,
              ticket_cool_down=tc)
    Queue.add_to_db(q)
    return jsonify({'reason': 'queue created'}), 200


@queue_api_bp.route('/add_ticket', methods=['POST'])
@login_required
def add_ticket():
    """
    Add a ticket to the queue.\n
    For the is_private field, pass in 0 or 1 to indicate true of false.\n
    For the tag_list, pass in comma seperated list of numbers in string.\n
    """
    queue = Queue.get_queue_by_id(int(request.json['queue_id']))
    student_id = int(request.json['student_id'])
    title = request.json['title']
    description = request.json['description']
    room = request.json['room']
    workstation = request.json['workstation']
    is_private = int(request.json['is_private'])  # pass in 1 or 0
    help_type = HelpType(int(request.json['help_type']))
    tag_list_raw = request.json['tag_list'].split(';')  # Pass in ; sep ints.
    tag_list = []
    for tag in tag_list_raw:
        tag_list.append(TicketTag(int(tag)).value)

    ticket = (queue.add_ticket(student_id, title, description, room,
                               workstation, is_private, help_type, tag_list))

    return (jsonify({'reason': 'ticket added to queue',
                     'result': ticket.to_json()}), 200)


@queue_api_bp.route('/login_grader', methods=['POST'])
@login_required
def login_grader():
    """
    Login a certain grader.
    """
    q_id = request.json['queue_id']
    g_id = request.json['grader_id']
    a_c = request.json['action_type']
    result = Queue.grader_login(queue_id=q_id,
                                grader_id=g_id,
                                action_type=a_c)
    if result[0]:
        return jsonify({'reason': 'grader login'}), 200
    else:
        return jsonify({'reason': result[1]}), 400


@queue_api_bp.route('/logout_grader', methods=['POST'])
@login_required
def logout_grader():
    """
    Logout a certain grader
    """
    q_id = request.json['queue_id']
    g_id = request.json['grader_id']
    a_c = request.json['action_type']
    status, result = Queue.grader_logout(queue_id=q_id,
                                         grader_id=g_id,
                                         action_type=a_c)
    if status:
        return jsonify({'reason': 'grader login'}), 200
    else:
        return jsonify({'reason': result}), 400


@queue_api_bp.route('/find_queue_for_user', methods=['GET'])
@login_required
def find_queue_for_user():
    """
    Find all the queues that this user is in.
    """
    uid = request.json['user_id']
    status, mess, q_list = Queue.\
        find_current_queue_for_user(user_id=uid)
    if status:
        ret = {}
        i = 0
        for q in q_list:
            i += 1
            ret['queue' + str(i)] = q.to_json()
        return jsonify({'reason': 'success', 'result': ret}), 200
    else:
        return jsonify({'reason': mess}), 400


@queue_api_bp.route('/lock_queue', methods=['POST'])
@login_required
def lock_queue():
    """
    Lock the queue.
    """
    qid = request.json['queue_id']
    q = Queue.get_queue_by_id(queue_id=qid)
    if not q:
        return jsonify({'reason': 'queue not found'}), 400
    else:
        q.lock()
        return jsonify({'reason': 'success'}), 200


@queue_api_bp.route('/find_queue_for_course', methods=['GET'])
@login_required
def find_queue_for_course():
    """
    Find the queue for a given course.
    """
    c_id = request.json['course_id']
    sta, q = Queue.find_queue_for_course(course_id=c_id)
    if sta:
        return jsonify({'reason': 'success', 'result': q}), 200
    else:
        return jsonify({'reason': 'queue not found'}), 400


@queue_api_bp.route('/create_queue_calendar', methods=['POST'])
@login_required
def create_queue_calendar():
    """
    Create the queue_calendar for the queue.
    """
    url = request.json['url']
    color = request.json['color']
    enable = request.json['is_enabled']
    q_id = request.json['queue_id']

    QueueCalendar(url=url, color=color, is_enabled=enable, queue_id=q_id)
    return jsonify({'reason': 'success'}), 200


@queue_api_bp.route('/find_queue_calendar', methods=['GET'])
@login_required
def find_queue_calendar():
    """
    Find the active queue_clandars
    """
    q_id = request.json['queue_id']
    c_list = QueueCalendar.find_all_calendar_for_queue(queue_id=q_id)
    if not c_list:
        return jsonify({'reason': 'queue not found, queue \
        has no calander'}), 400
    ret = {}
    i = 0
    for c in c_list:
        i += 1
        ret['queue_calander' + str(i)] = c.to_json()
    return jsonify({'reason': 'Success', 'result': ret}), 200


@queue_api_bp.route('/find_all_tickets_for_queue', methods=['GET'])
@login_required
def find_all_ticket_for_queue():
    """
    Find all the tickest for queue.
    """
    q_id = int(request.json['queue_id'])
    s_type_list = []
    if 'status' in request.json:
        s_list = list(request.json['status'])
        for s in s_list:
            t_s = t_Status(s)
            s_type_list.append(t_s)
        status, msg, t_list = Queue.find_all_tickets(queue_id=q_id,
                                                     status=s_type_list)
    else:
        status, msg, t_list = Queue.find_all_tickets(queue_id=q_id)
    if not status:
        return jsonify({'reason': msg}), 400
    ret = {}
    i = 0
    for t in t_list:
        i += 1
        view = t.can_view_by(current_user.id)
        edit = t.can_edit_by(current_user.id)
        ret['ticket' + str(i)] = {'ticket': t.to_json(),
                                  'can_view': view,
                                  'can_edit': edit}
    return jsonify({'reason': 'Success', 'result': ret}), 200


@queue_api_bp.route('/find_all_tickets_for_student', methods=['GET'])
@login_required
def find_all_ticket_for_student():
    """
    Find all the tickest for queue.
    """
    q_id = request.json['queue_id']
    s_id = request.json['student_id']
    s_type_list = []
    s_list = list(request.json['status'])
    for s in s_list:
        t_s = t_Status(s)
        s_type_list.append(t_s)
    t_list = Queue.find_all_tickets_by_student(queue_id=q_id,
                                               student_id=s_id,
                                               status=s_type_list)
    ret = {}
    i = 0
    for t in t_list:
        i += 1
        ret['ticket' + str(i)] = t.to_json()
    return jsonify({'reason': 'Success', 'result': ret}), 200


@queue_api_bp.route('/find_all_tickets_for_grader', methods=['GET'])
@login_required
def find_all_ticket_for_grader():
    """
    Find all the tickest for queue.
    """
    q_id = request.json['queue_id']
    g_id = request.json['grader_id']
    s_type_list = []
    s_list = list(request.json['status'])
    for s in s_list:
        t_s = t_Status(s)
        s_type_list.append(t_s)
    t_list = Queue.find_all_tickets_by_student(queue_id=q_id,
                                               student_id=g_id,
                                               status=s_type_list)
    ret = {}
    i = 0
    for t in t_list:
        i += 1
        ret['ticket' + str(i)] = t.to_json()
    return jsonify({'reason': 'Success', 'result': ret}), 200


@queue_api_bp.route('/accept_ticket', methods=['POST'])
@login_required
def accept_ticket():
    """
    User accept a ticket.
    """
    q_id = request.json['queue_id']
    g_id = request.json['grader_id']
    t_id = request.json['ticket_id']
    s, r = Queue.accept_ticket(queue_id=q_id, grader_id=g_id, ticket_id=t_id)
    if s:
        return jsonify({'reason': r}), 200
    else:
        return jsonify({'reason': r}), 400
