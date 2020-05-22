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

    return jsonify(ticket.to_json())


@ticket_api_bp.route('/get_latest_feedback', methods=['GET'])
@login_required
def get_latest_feedback():
    '''
    Route used to get the latest feedback on a ticket.\n
    @author nouryehia
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    return jsonify(ticket.get_latest_feedback())


@ticket_api_bp.route('/get_ticket_events', methods=['GET'])
@login_required
def get_ticket_events():
    '''
    Route used to get a ticket's events.\n
    @author nouryehia
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    return jsonify(ticket.get_ticket_events())


@ticket_api_bp.route('/get_user_permissions', methods=['GET'])
@login_required
def get_user_permissions():
    '''
    Route used to determine if a user can view or edit a ticket.\n
    @author nouryehia
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    email = request.json['email'] if 'email' in request.json else None
    pid = request.json['pid'] if 'pid' in request.json else None

    user = User.find_by_pid_email_fallback(pid, email)

    return jsonify({'can_view': ticket.can_view_by(user),
                    'can_edit': ticket.can_edit_by(user)})


@ticket_api_bp.route('/student_update', methods=['POST'])
@login_required
def student_update():
    '''
    Route used to update a ticket. Only the fields being updated need to be
    passed in.\n
    @author nouryehia
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])

    title = (request.json['title'] if 'title' in request.json
             else ticket.title)
    description = (request.json['description'] if 'description' in request.json
                   else ticket.title)
    room = (request.json['room'] if 'room' in request.json
            else ticket.room)
    workstation = (request.json['workstation'] if 'workstation' in request.json
                   else ticket.workstation)
    is_private = (request.json['is_private'] if 'is_private' in request.json
                  else ticket.is_private)
    help_type = (request.json['help_type'] if 'help_type' in request.json
                 else ticket.help_type)
    tags = (request.json['tags'] if 'tags' in request.json
            else ticket.tags)

    return (jsonify({'reason': 'ticket updated'}), 200
            if ticket.student_update(title, description, room, workstation,
                                     is_private, help_type, tags) else
            jsonify({'reason': 'ticket could not be updated'}), 400)


# @ticket_api_bp.route('/find_all_tickets', methods=['GET'])
# @login_required
# def find_all_tickets():
#     '''
#     Route used to get all the tickets currently on a queue.\n
#     @author nouryehia
#     '''
#     queue = Ticket.get_ticket_by_id(request.json['queue_id'])
#     status = (request.json['status'] if 'status' in request.json
#               else None)

#     return jsonify(Ticket.find_all_tickets(queue, status))


# @ticket_api_bp.route('/find_all_tickets_for_grader', methods=['GET'])
# @login_required
# def find_all_tickets_for_grader():
#     '''
#     Route used to get all tickets handled by a grader.\n
#     @author nouryehia
#     '''
#     queue = Ticket.get_ticket_by_id(request.json['queue_id'])
#     grader = User.find_by_pid_email_fallback(None, request.json['email'])

#     return jsonify(Ticket.find_all_tickets_for_grader(queue, grader))


# @ticket_api_bp.route('/find_tickets_in_range', methods=['GET'])
# @login_required
# def find_tickets_in_range():
#     '''
#     Route used to find all the tickets on a queue created between two dates.
#     @author nouryehia
#     '''
#     queue = Ticket.get_ticket_by_id(request.json['queue_id'])
#     start = request.json['start']
#     end = request.json['end']
#     grader = (User.find_by_pid_email_fallback(None, request.json['email'])
#               if 'email' in request.json
#               else None)

#     return jsonify(Ticket.find_tickets_in_range(queue, start, end, grader))


# @ticket_api_bp.route('/find_ticket_accepted_by_grader', methods=['GET'])
# @login_required
# def find_ticket_accepted_by_grader():
#     '''
#     Route used to find the last ticket accepted by a grader.\n
#     @author nouryehia
#     '''
#     grader = User.find_by_pid_email_fallback(None, request.json['email'])
#     return jsonify(Ticket.find_ticket_accepted_by_grader(grader))


# @ticket_api_bp.route('/find_resolved_tickets_in', methods=['GET'])
# @login_required
# def find_resolved_tickets_in():
#     '''
#     Route used to find all resolved tickets in queue. Can query for the last
#     hour, the last day, or a specific time interval.\n
#     @author nouryehia
#     '''
#     queue = Ticket.get_ticket_by_id(request.json['queue_id'])
#   recent_hour = (request.json['recent_hour'] if 'recent_hour' in request.json
#                    else False)
#     day = (request.json['day'] if 'day' in request.json
#            else False)
#     start = (request.json['start'] if 'start' in request.json
#              else None)
#     end = (request.json['end'] if 'end' in request.json
#            else None)

#     return (jsonify(Ticket.find_resolved_tickets_in(queue, recent_hour, day,
#                                                     start, end)))


# @ticket_api_bp.route('/average_resolved_time', methods=['GET'])
# @login_required
# def average_resolved_time():
#     '''
#     Route used to find the average time it took to resolve a list of tickets
#     (in seconds).\n
#     @author nouryehia
#     '''
#     tickets = Ticket.get_ticket_by_id(request.json['tickets'])
#     return jsonify(Ticket.average_resolved_time(tickets))


# @ticket_api_bp.route('/defer_accepted_ticket_for_grader', methods=['POST'])
# @login_required
# def defer_accepted_ticket_for_grader():
#     '''
#     Route used to return tickets accepted by a grader to the queue. \n
#     @author nouryehia
#     '''
#     grader = User.find_by_pid_email_fallback(None, request.json['email'])

#     return (jsonify({'reason': 'ticket updated'}), 200
#             if Ticket.defer_accepted_ticket_for_grader(grader)
#             else jsonify({'reason': 'ticket could not be updated'}), 400)
