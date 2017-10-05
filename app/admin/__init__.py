from flask import Blueprint

admin_panel = Blueprint('admin_panel', __name__)

from . import views