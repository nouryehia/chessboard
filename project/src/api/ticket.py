from flask_cors import CORS
from flask_login import login_required
from flask import Blueprint, request, jsonify

from ..models.ticket import Ticket
from ..models.user import User


ticket_api_bp = Blueprint('ticket_api', __name__)
CORS(ticket_api_bp, supports_credentials=True)


@ticket_api_bp.route('/is_question', methods=['GET'])
@login_required
def is_question():
    '''
    Route used to determine if a ticket is a question.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])

    return (jsonify({'reason': 'ticket is a question'}), 200
            if ticket.is_question() else
            jsonify({'reason': 'ticket is not a question'}), 400)


@ticket_api_bp.route('/is_checkoff', methods=['GET'])
# @login_required
def is_checkoff():
    '''
    Route used to determine if a ticket is a checkoff.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])

    return (jsonify({'reason': 'ticket is a checkoff'}), 200
            if ticket.is_checkoff() else
            jsonify({'reason': 'ticket is not a checkoff'}), 400)


@ticket_api_bp.route('/is_pending', methods=['GET'])
# @login_required
def is_pending():
    '''
    Route used to determine if a ticket is pending.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])

    return (jsonify({'reason': 'ticket is pending'}), 200
            if ticket.is_pending() else
            jsonify({'reason': 'ticket is not pending'}), 400)


@ticket_api_bp.route('/is_accepted', methods=['GET'])
# @login_required
def is_accepted():
    '''
    Route used to determine if a ticket is accepted.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])

    return (jsonify({'reason': 'ticket is pending'}), 200
            if ticket.is_accepted() else
            jsonify({'reason': 'ticket is not pending'}), 400)


@ticket_api_bp.route('/is_resolved', methods=['GET'])
# @login_required
def is_resolved():
    '''
    Route used to determine if a ticket is resolved.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])

    return (jsonify({'reason': 'ticket is resolved'}), 200
            if ticket.is_resolved() else
            jsonify({'reason': 'ticket is not resolved'}), 400)


@ticket_api_bp.route('/is_canceled', methods=['GET'])
# @login_required
def is_canceled():
    '''
    Route used to determine if a ticket is canceled.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])

    return (jsonify({'reason': 'ticket is canceled'}), 200
            if ticket.is_canceled() else
            jsonify({'reason': 'ticket is not canceled'}), 400)


@ticket_api_bp.route('/is_non_cse', methods=['GET'])
# @login_required
def is_non_cse():
    '''
    Route used to determine if a ticket is not in the CSE building.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])

    return (jsonify({'reason': 'ticket is not in CSE'}), 200
            if ticket.is_non_cse() else
            jsonify({'reason': 'ticket is in CSE'}), 400)


@ticket_api_bp.route('/is_hallway', methods=['GET'])
# @login_required
def is_hallway():
    '''
    Route used to determine if a ticket is in the hallway.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])

    return (jsonify({'reason': 'ticket is in hallway'}), 200
            if ticket.is_hallway() else
            jsonify({'reason': 'ticket is not in hallway'}), 400)


@ticket_api_bp.route('/get_tags_list', methods=['GET'])
# @login_required
def get_tags_list():
    '''
    Route used to get the tags on a ticket.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    return jsonify(ticket.get_tags_list())


@ticket_api_bp.route('/get_help_time_in_second', methods=['GET'])
# @login_required
def get_help_time_in_second():
    '''
    Route used to get the help time of a ticket (in seconds).\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    return jsonify(ticket.get_help_time_in_second())


@ticket_api_bp.route('/get_title', methods=['GET'])
# @login_required
def get_title():
    '''
    Route used to get the get the title of a ticket.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    return jsonify(ticket.get_title())


@ticket_api_bp.route('/get_description', methods=['GET'])
# @login_required
def get_description():
    '''
    Route used to get the description of a ticket.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    return jsonify(ticket.get_description())


@ticket_api_bp.route('/get_room', methods=['GET'])
# @login_required
def get_room():
    '''
    Route used to get the room of a ticket.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    return jsonify(ticket.get_room())


@ticket_api_bp.route('/get_workstation', methods=['GET'])
# @login_required
def get_workstation():
    '''
    Route used to get the workstation of a ticket.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    return jsonify(ticket.get_workstation())


@ticket_api_bp.route('/get_position', methods=['GET'])
# @login_required
def get_position():
    '''
    Route used to get the position of a ticket in the current queue.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    return jsonify(ticket.get_position())


@ticket_api_bp.route('/get_latest_feedback', methods=['GET'])
# @login_required
def get_latest_feedback():
    '''
    Route used to get the latest feedback on a ticket.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    return jsonify(ticket.get_latest_feedback())


@ticket_api_bp.route('/get_ticket_events', methods=['GET'])
# @login_required
def get_ticket_events():
    '''
    Route used to get a ticket's events.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    return jsonify(ticket.get_ticket_events())


@ticket_api_bp.route('/can_view_by', methods=['GET'])
# @login_required
def can_view_by():
    '''
    Route used to determine if a user can see a ticket.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    user = User.find_by_pid_email_fallback(None, request.json['email'])

    return (jsonify({'reason': 'ticket can be viewed by user'}), 200
            if ticket.can_view_by(user) else
            jsonify({'reason': 'ticket cannot be viewed by user'}), 400)


@ticket_api_bp.route('/can_edit_by', methods=['GET'])
# @login_required
def can_edit_by():
    '''
    Route used to determine if a user can edit a ticket.\n
    @author Nour
    '''
    ticket = Ticket.get_ticket_by_id(request.json['ticket_id'])
    user = User.find_by_pid_email_fallback(None, request.json['email'])

    return (jsonify({'reason': 'ticket can be edited by user'}), 200
            if ticket.can_edit_by(user) else
            jsonify({'reason': 'ticket cannot be edited by user'}), 400)


@ticket_api_bp.route('/student_update', methods=['POST'])
# @login_required
def student_update():
    '''
    Route used to update a ticket. Only the fields being updated need to be
    passed in.\n
    @author Nour
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


@ticket_api_bp.route('/find_all_tickets', methods=['GET'])
# @login_required
def find_all_tickets():
    '''
    Route used to get all the tickets currently on a queue.\n
    @author Nour
    '''
    queue = Ticket.get_ticket_by_id(request.json['queue_id'])
    status = (request.json['status'] if 'status' in request.json
              else None)

    return jsonify(Ticket.find_all_tickets(queue, status))


@ticket_api_bp.route('/find_all_tickets_for_grader', methods=['GET'])
# @login_required
def find_all_tickets_for_grader():
    '''
    Route used to get all tickets handled by a grader.\n
    @author Nour
    '''
    queue = Ticket.get_ticket_by_id(request.json['queue_id'])
    grader = User.find_by_pid_email_fallback(None, request.json['email'])

    return jsonify(Ticket.find_all_tickets_for_grader(queue, grader))


@ticket_api_bp.route('/find_tickets_in_range', methods=['GET'])
# @login_required
def find_tickets_in_range():
    '''
    Route used to find all the tickets on a queue created between two dates.\n
    @author Nour
    '''
    queue = Ticket.get_ticket_by_id(request.json['queue_id'])
    start = request.json['start']
    end = request.json['end']
    grader = (User.find_by_pid_email_fallback(None, request.json['email'])
              if 'email' in request.json
              else None)

    return jsonify(Ticket.find_tickets_in_range(queue, start, end, grader))


@ticket_api_bp.route('/find_ticket_accepted_by_grader', methods=['GET'])
# @login_required
def find_ticket_accepted_by_grader():
    '''
    Route used to find the last ticket accepted by a grader.\n
    @author Nour
    '''
    grader = User.find_by_pid_email_fallback(None, request.json['email'])
    return jsonify(Ticket.find_ticket_accepted_by_grader(grader))


@ticket_api_bp.route('/find_resolved_tickets_in', methods=['GET'])
# @login_required
def find_resolved_tickets_in():
    '''
    Route used to find all resolved tickets in queue. Can query for the last
    hour, the last day, or a specific time interval.\n
    @author Nour
    '''
    queue = Ticket.get_ticket_by_id(request.json['queue_id'])
    recent_hour = (request.json['recent_hour'] if 'recent_hour' in request.json
                   else False)
    day = (request.json['day'] if 'day' in request.json
           else False)
    start = (request.json['start'] if 'start' in request.json
             else None)
    end = (request.json['end'] if 'end' in request.json
           else None)

    return (jsonify(Ticket.find_resolved_tickets_in(queue, recent_hour, day,
                                                    start, end)))


@ticket_api_bp.route('/average_resolved_time', methods=['GET'])
# @login_required
def average_resolved_time():
    '''
    Route used to find the average time it took to resolve a list of tickets
    (in seconds).\n
    @author Nour
    '''
    tickets = Ticket.get_ticket_by_id(request.json['tickets'])
    return jsonify(Ticket.average_resolved_time(tickets))


@ticket_api_bp.route('/defer_accepted_ticket_for_grader', methods=['POST'])
# @login_required
def defer_accepted_ticket_for_grader():
    '''
    Route used to return tickets accepted by a grader to the queue. \n
    @author Nour
    '''
    grader = User.find_by_pid_email_fallback(None, request.json['email'])

    return (jsonify({'reason': 'ticket updated'}), 200
            if Ticket.defer_accepted_ticket_for_grader(grader)
            else jsonify({'reason': 'ticket could not be updated'}), 400)
