from flask import Blueprint

users_bp = Blueprint('mechanics_bp', __name__)

from . import routes
