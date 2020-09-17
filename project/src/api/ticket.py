from flask_cors import CORS
from flask_login import login_required, current_user
from flask import Blueprint, request, jsonify

from ..models.ticket import Ticket, HelpType, TicketTag
from ..models.events.ticket_event import TicketEvent, EventType
from ..models.enrolled_course import EnrolledCourse as EC
from ..models.enrolled_course import Role
from ..models.course import Course
from ..models.user import User
from ..utils.time import TimeUtil


ticket_api_bp = Blueprint('ticket_api', __name__)
CORS(ticket_api_bp, supports_credentials=True)


@ticket_api_bp.route('/add_ticket', methods=['POST'])
@login_required
def add_ticket():
    """
    Add a ticket to the queue.\n
    For the is_private field, pass in 0 or 1 to indicate true of false.\n
    For the tag_list, pass in semi-colon seperated list of numbers in string.\n
    @author YixuanZhou
    """
    queue_id = int(request.json['queue_id'])
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

    # create a ticket
    ticket = Ticket.add_ticket(queue_id=queue_id, student_id=student_id,
                               title=title, description=description, room=room,
                               workstation=workstation, is_private=is_private,
                               help_type=help_type, tag_list=tag_list)

    # submit a ticket event
    TicketEvent.create_event(event_type=EventType.CREATED,
                             ticket_id=ticket.id,
                             message=description,
                             is_private=is_private,
                             user_id=student_id)

    return (jsonify({'reason': 'ticket added to queue',
                     'result': ticket.to_json(user_id=current_user.id)}), 200)


@ticket_api_bp.route('/get_info', methods=['GET'])
@login_required
def get_info():
    '''
    Route used to get a ticket's info.\n
    @author nouryehia
    '''
    user_id = request.args.get('user_id', type=int)
    ticket = Ticket.get_ticket_by_id(request.args.get('ticket_id', type=int))

    return jsonify(ticket.to_json(user_id=user_id)), 200


@ticket_api_bp.route('/get_user_permissions', methods=['GET'])
@login_required
def get_user_permissions():
    '''
    Route used to determine if a user can view or edit a ticket.\n
    @author nouryehia
    '''
    user_id = request.args.get('user_id', type=int)
    ticket = Ticket.get_ticket_by_id(request.args.get('ticket_id', type=int))

    return jsonify({'can_view': ticket.can_view_by(user_id),
                    'can_edit': ticket.can_edit_by(user_id)}), 200


@ticket_api_bp.route('/student_update', methods=['POST'])
@login_required
def student_update():
    '''
    Route used to update a ticket. Only the fields being updated need to be
    passed in. This is specifically used for student updates.
    @author nouryehia
    @author YixuanZhou (updates)
    '''
    req = request.json

    ticket = Ticket.get_ticket_by_id(int(req['ticket_id']))

    title = req['title'] if 'title' in req else ticket.title
    desc = req['description'] if 'description' in req else ticket.description
    room = req['room'] if 'room' in req else ticket.room
    ws = req['workstation'] if 'workstation' in req else ticket.workstation
    help_type = (HelpType(int(request.json['help_type'])) if 'help_type' in req
                 else ticket.help_type)
    if 'is_private' in req:
        private = True if req['is_private'] == 1 else False
    else:
        private = ticket.is_private

    if not ticket.can_edit_by(current_user.id):
        return jsonify({'reason': 'Permission denied'}), 400

    TicketEvent.create_event(event_type=EventType.UPDATED, ticket_id=ticket.id,
                             message=desc, is_private=private,
                             user_id=ticket.student_id)

    if 'tag_list' in request.json:
        raw_tags = request.json['tag_list'].split(';')
        tags = []
        for tag in raw_tags:
            tags.append(TicketTag(int(tag)).value)
    else:
        tags = ticket.get_tags_list()

    if ticket.student_update(title, desc, room, ws, private, help_type, tags):
        return jsonify({'reason': 'ticket updated'}), 200

    return jsonify({'reason': 'ticket could not be updated'}), 400


@ticket_api_bp.route('/grader_update', methods=['POST'])
@login_required
def grader_update():
    """
    The api function used for graders to perfrom actions to ticket.\n
    Expect status for only accepted, defered, canceled, resolved.
    @author YixuanZhou
    @author nouryehia (updates)
    """
    ticket = Ticket.get_ticket_by_id(int(request.json['ticket_id']))
    status = request.json['status']

    course_id = Course.get_course_by_queue_id(ticket.queue_id)

    user = EC.find_user_in_course(user_id=current_user.user_id,
                                  course_id=course_id)

    if user.get_role() == Role.STUDENT.value and \
       current_user.user_id != ticket.student_id:
        return jsonify({'reason': "User does not have permissions"}), 400

    actions = {'resolved': ticket.mark_resolved,
               'canceled': ticket.mark_canceled,
               'defered': ticket.mark_pending}

    event_types = {'accepted': EventType.ACCEPTED,
                   'resolved': EventType.RESOLVED,
                   'canceled': EventType.CANCELED,
                   'defered': EventType.DEFERRED}

    grader = User.get_user_by_id(current_user.user_id)

    if status == 'accepted':
        ticket.mark_accepted_by(grader)
    else:
        actions[status]()

    TicketEvent.create_event(event_type=event_types[status],
                             ticket_id=ticket.id,
                             message=status,
                             is_private=ticket.is_private,
                             user_id=current_user.user_id,
                             timestamp=TimeUtil.get_current_time())

    return jsonify({'status': status,
                    'grader_name': grader.first_name + ' ' + grader.last_name,
                    'grader_pid': grader.pid}), 200


@ticket_api_bp.route('/defer_accepted_tickets_for_grader', methods=['POST'])
@login_required
def defer_accepted_tickets_for_grader():
    '''
    Route used to return tickets accepted by a grader to the queue.\n
    @author nouryehia
    '''
    email = request.json['email'] if 'email' in request.json else None
    pid = request.json['pid'] if 'pid' in request.json else None
    grader = User.find_by_pid_email_fallback(pid, email)

    tickets = Ticket.defer_accepted_tickets_for_grader(grader)

    return jsonify({'reason': str(tickets) + ' tickets deferred'}), 400


@ticket_api_bp.route('/find_all_tickets', methods=['GET'])
@login_required
def find_all_tickets():
    '''
    Route used to find tickets on the queue (can be catgorized as pending or\n
    accepted).\n
    @author nouryehia
    '''
    status = []
    pending = request.args.get('pending', default=0, type=int)
    accepted = request.args.get('accepted', default=0, type=int)
    if pending:
        status.append(0)
    if accepted:
        status.append(1)

    tickets = Ticket.find_all_tickets(queue_id=int(request.json['queue_id']),
                                      status=status)

    ticket_infos = []
    for ticket in tickets:
        ticket_infos.append(ticket.to_json(user_id=current_user.id))

    return jsonify({'result': ticket_infos}), 200


@ticket_api_bp.route('/find_tickets_in_range', methods=['GET'])
@login_required
def find_tickets_in_range():
    '''
    Route used to find tickets in a specific range of time. A grader can be\n
    passed in to only get tickets for that grader.\n
    @author nouryehia
    '''
    queue_id = request.args.get('queue_id', type=int)
    start = request.args.get('start', type=str)
    end = request.args.get('end', type=str)
    grader_id = request.args.get('grader_id', type=int)
    tickets = Ticket.find_tickets_in_range(queue_id, start, end, grader_id)

    ticket_infos = []
    for ticket in tickets:
        ticket_infos.append(ticket.to_json(user_id=current_user.id))

    return jsonify({'result': ticket_infos}), 200


@ticket_api_bp.route('/find_all_tickets_by_student', methods=['GET'])
@login_required
def find_all_tickets_by_student():
    '''
    Route used to find tickets on the queue by a student (can be catgorized\n
    as pending or accepted).\n
    @author nouryehia
    '''
    status = []
    pending = request.args.get('pending', default=False, type=bool)
    accepted = pending = request.args.get('accepted', default=False, type=bool)
    if pending:
        status.append(0)
    if accepted:
        status.append(1)

    tickets = Ticket.find_all_tickets(int(request.json['queue_id']),
                                      int(request.json['student_id']), status)

    ticket_infos = []
    for ticket in tickets:
        ticket_infos.append(ticket.to_json())

    return jsonify({'result': ticket_infos}), 200


@ticket_api_bp.route('/find_all_tickets_for_grader', methods=['GET'])
@login_required
def find_all_tickets_for_grader():
    '''
    Route used to find tickets on a queue handled by a grader.\n
    @author nouryehia
    '''
    tickets = Ticket.find_all_tickets(
        queue_id=request.args.get('queue_id', type=int),
        grader_id=request.args.get('grader_id', type=int))

    ticket_infos = []
    for ticket in tickets:
        ticket_infos.append(ticket.to_json(user_id=current_user.id))

    return jsonify({'result': ticket_infos}), 200


@ticket_api_bp.route('/find_resolved_tickets_in', methods=['GET'])
@login_required
def find_resolved_tickets_in():
    '''
    Route used to resolved tickets on a queue.\n
    @author nouryehia
    '''
    queue_id = request.args.get('queue_id', type=int)
    recent_hour = request.args.get('recent_hour', default=0, type=int)
    day = request.args.get('day', default=0, type=int)
    start = request.args.get('start', default=None, type=str)
    end = request.args.get('end', default=None, type=str)

    tickets = Ticket.find_resolved_tickets_in(queue_id, recent_hour, day,
                                              start, end)

    ticket_infos = []
    for ticket in tickets:
        ticket_infos.append(ticket.to_json(user_id=current_user.id))

    return jsonify({'result': ticket_infos}), 200
