"""
This file is for the api of queue and queue related functions.
It is not finished, appearently.
However, just to note that this should be the only api for this model.
By how the models are constructed, now,
all the requests should be sent through queue.
Typically, we need to retrive a queue object from the database first,
and then use them to perform other things.
@Yixuan Zhou
"""
from flask_cors import CORS
from flask import Blueprint, request, jsonify
from flask_login import login_required

from ..models.queue import Queue, Status

queue_api_bp = Blueprint('queue_api', __name__)
CORS(queue_api_bp, supports_credentials=True)


@queue_api_bp.route('/find_queue', methods=['GET'])
@login_required
def find_queue():
    """
    Return the queue object corresponding to an id.\n
    @authoer: YixuanZhou
    """
    queue_id = request.json['queue_id'] if 'queue_id' in request.json else None
    if not queue_id:
        return jsonify({'reason': 'queue_id invalid'}), 400

    queue = Queue.get_queue_by_id(queue_id)

    if not queue:
        return jsonify({'reason': 'queue not found'}), 400

    ret = {'reason': 'request ok', 'result': queue.to_json()}
    return jsonify(ret), 200


@queue_api_bp.route('/create_queue', methods=['GET'])
@login_required
def create_queue():
    """
    Create a queue for a course.\n
    """
    hce = request.json['high_capacity_enabled'] if \
        'high_capacity_enabled' in request.json else None
    hct = request.json['high_capacity_threshold'] if \
        'high_capacity_threshold' in request.json else None
    hcm = request.json['high_capacity_message'] if \
        'high_capacity_message' in request.json else None
    hcw = request.json['high_capacity_warning'] if \
        'high_capacity_warning' in request.json else None
    tc = request.json['ticket_cooldown'] if \
        'ticket_cooldown' in request.json else None
    Queue(status=Status.CLOSED.value,
          high_capacity_enabled=hce,
          high_capacity_threshold=hct,
          high_capacity_message=hcm,
          high_capacity_warning=hcw,
          ticket_cooldown=tc)
    return jsonify({'reason': 'queue created'}), 200
