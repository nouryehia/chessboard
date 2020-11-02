from flask_cors import CORS
from flask_login import login_required, current_user
from flask import Blueprint, request, jsonify

from ..utils.time import TimeUtil
from ..utils.tutor_stats import TutoringSession
from ..models.ticket import Ticket
from ..models.ticket_feedback import TicketFeedback, Rating


tutor_stats_api_bp = Blueprint('tutor_stats_api', __name__)
CORS(tutor_stats_api_bp, supports_credentials=True)


# @tutor_stats_api_bp.route('get_on_duty_time')
