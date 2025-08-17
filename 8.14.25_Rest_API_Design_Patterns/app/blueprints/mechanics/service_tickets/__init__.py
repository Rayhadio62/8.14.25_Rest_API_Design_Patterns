from flask import Blueprint

users_bp = Blueprint('service_tickets_bp', __name__)

from . import routes