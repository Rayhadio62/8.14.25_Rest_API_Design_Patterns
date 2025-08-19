from flask import Blueprint

mechanics_bp = Blueprint('customers_bp', __name__)

from . import routes
