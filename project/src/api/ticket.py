from flask_cors import CORS
from flask_login import login_required
from flask import Blueprint, request, jsonify

from ..models.ticket import Ticket
from ..models.user import User


ticket_api_bp = Blueprint('ticket_api', __name__)
CORS(ticket_api_bp, supports_credentials=True)


@ticket_api_bp.route('/get_info', methods=['GET'])
@login_required
def get_info():
    '''
    Route used to get a ticket's info.\n
    @author nouryehia
    '''
    ticket = Ticket.get_ticket_by_id(int(request.json['ticket_id']))
    return jsonify(ticket.to_json()), 200


@ticket_api_bp.route('/get_user_permissions', methods=['GET'])
@login_required
def get_user_permissions():
    '''
    Route used to determine if a user can view or edit a ticket.\n
    @author nouryehia
    '''
    ticket = Ticket.get_ticket_by_id(int(request.json['ticket_id']))
    email = request.json['email'] if 'email' in request.json else None
    pid = request.json['pid'] if 'pid' in request.json else None

    user = User.find_by_pid_email_fallback(pid, email)

    return jsonify({'can_view': ticket.can_view_by(user),
                    'can_edit': ticket.can_edit_by(user)}), 200


@ticket_api_bp.route('/student_update', methods=['POST'])
@login_required
def student_update():
    '''
    Route used to update a ticket. Only the fields being updated need to be\n
    passed in.
    @author nouryehia
    '''
    req = request.json

    ticket = Ticket.get_ticket_by_id(int(req['ticket_id']))

    title = req['title'] if 'title' in req else ticket.title
    desc = req['description'] if 'description' in req else ticket.title
    room = req['room'] if 'room' in req else ticket.room
    ws = req['workstation'] if 'workstation' in req else ticket.workstation
    help_type = req['help_type'] if 'help_type' in req else ticket.help_type
    tags = request.json['tags'] if 'tags' in request.json else ticket.tags

    if 'is_private' in req:
        private = (True if (req['is_private'] == 'true' or
                            req['is_private'] == 'True')
                   else False)
    else:
        private = ticket.is_private

    if ticket.student_update(title, desc, room, ws, private, help_type, tags):
        return jsonify({'reason': 'ticket updated'}), 200

    return jsonify({'reason': 'ticket could not be updated'}), 400


@ticket_api_bp.route('/find_ticket_accepted_by_grader', methods=['GET'])
@login_required
def find_ticket_accepted_by_grader():
    '''
    Route used to find the last ticket accepted by a grader.\n
    @author nouryehia
    '''
    email = request.json['email'] if 'email' in request.json else None
    pid = request.json['pid'] if 'pid' in request.json else None
    grader = User.find_by_pid_email_fallback(pid, email)

    ticket = Ticket.find_ticket_accepted_by_grader(grader)

    if ticket is None:
        return jsonify({'reason': 'Grader did not accept any tickets'}), 400

    return jsonify(ticket.to_json()), 200


@ticket_api_bp.route('/defer_accepted_ticket_for_grader', methods=['POST'])
@login_required
def defer_accepted_ticket_for_grader():
    '''
    Route used to return tickets accepted by a grader to the queue.\n
    @author nouryehia
    '''
    email = request.json['email'] if 'email' in request.json else None
    pid = request.json['pid'] if 'pid' in request.json else None
    grader = User.find_by_pid_email_fallback(pid, email)

    if Ticket.defer_accepted_ticket_for_grader(grader):
        return jsonify({'reason': 'tickets deferred'}), 200

    return jsonify({'reason': 'tickets could not be deffered'}), 400


@ticket_api_bp.route('/find_all_tickets', methods=['GET'])
@login_required
def find_all_tickets():
    '''
    Route used to find tickets on the queue (can be catgorized as pending or\n
    accepted).\n
    @author nouryehia
    '''
    status = []
    pending = True if ('pending' in request.json and
                       (request.json['pending'] == 'true' or
                        request.json['pending'] == 'True')) else False
    accepted = True if ('accepted' in request.json and
                        (request.json['accepted'] == 'true' or
                         request.json['accepted'] == 'True')) else False
    if pending:
        status.append(0)
    if accepted:
        status.append(1)

    tickets = Ticket.find_all_tickets(int(request.json['queue_id']), status)

    ticket_infos = []
    for ticket in tickets:
        ticket_infos.append(ticket.to_json())

    return jsonify({'result': ticket_infos}), 200


@ticket_api_bp.route('/find_tickets_in_range', methods=['GET'])
@login_required
def find_tickets_in_range():
    '''
    Route used to find tickets in a specific range of time. A grader can be\n
    passed in to only get tickets for that grader.\n
    @author nouryehia
    '''
    queue_id = int(request.json['queue_id'])
    start = request.json['start']
    end = request.json['end']
    grader_id = (int(request.json['grader_id']) if 'grader_id' in request.json
                 else None)

    tickets = Ticket.find_tickets_in_range(queue_id, start, end, grader_id)

    ticket_infos = []
    for ticket in tickets:
        ticket_infos.append(ticket.to_json())

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
    pending = True if ('pending' in request.json and
                       (request.json['pending'] == 'true' or
                        request.json['pending'] == 'True')) else False
    accepted = True if ('accepted' in request.json and
                        (request.json['accepted'] == 'true' or
                         request.json['accepted'] == 'True')) else False
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
    tickets = Ticket.find_all_tickets(int(request.json['queue_id']),
                                      int(request.json['grader_id']))

    ticket_infos = []
    for ticket in tickets:
        ticket_infos.append(ticket.to_json())

    return jsonify({'result': ticket_infos}), 200


@ticket_api_bp.route('/find_resolved_tickets_in', methods=['GET'])
@login_required
def find_resolved_tickets_in():
    '''
    Route used to resolved tickets on a queue.\n
    @author nouryehia
    '''
    queue_id = int(request.json['queue_id'])
    recent_hour = True if ('recent_hour' in request.json and
                           (request.json['recent_hour'] == 'true' or
                            request.json['recent_hour'] == 'True')) else False
    day = True if ('day' in request.json and
                   (request.json['day'] == 'true' or
                    request.json['day'] == 'True')) else False
    start = request.json['start'] if 'start' in request.json else None
    end = request.json['end'] if 'end' in request.json else None

    tickets = Ticket.find_resolved_tickets_in(queue_id, recent_hour, day,
                                              start, end)

    ticket_infos = []
    for ticket in tickets:
        ticket_infos.append(ticket.to_json())

    return jsonify({'result': ticket_infos}), 200
