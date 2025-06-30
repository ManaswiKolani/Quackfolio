from flask import Blueprint, render_template
from app.constants import get_background_url

start_bp = Blueprint('start', __name__)

@start_bp.route('/')
def start():
    background = get_background_url('start')
    return render_template('start.html', background=background)
