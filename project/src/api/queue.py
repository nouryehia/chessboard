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

# from ..models.queue import Queue

queue_api_bp = Blueprint('queue_api', __name__)
CORS(queue_api_bp, supports_credentials=True)


@queue_api_bp.route('/find_queue', methods=['GET'])
def find_queue():
    """
    Return the queue object corresponding to an id.\n
    """
    queue_id = request.json["queue_id"] if "queue_id" in request.json else None
    if not queue_id:
        return jsonify({'reason': 'queue_id invalid'}), 400

    # queue = Queue.get_queue_by_id(queue_id)
    queue = None

    if not queue:
        return jsonify({'reason': 'queue not found'}), 400

    ret = {'reason': 'request ok', 'result': queue.to_json()}
    return jsonify(ret), 200
