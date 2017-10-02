from flask import Blueprint

market = Blueprint('market', __name__)

from . import routes