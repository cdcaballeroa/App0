from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import usersDB
from .models import Event

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        event_query = Event.query.order_by(Event.id.desc()).filter_by(email=current_user.email).all()
        return render_template('profile.html', name=current_user.name, user_events=event_query)
    else:
        return render_template('login.html')


@main.route('/profile')
@login_required
def profile():
    event_query = Event.query.order_by(Event.id.desc()).filter_by(email=current_user.email).all()
    events_number = Event.query.filter_by(email=current_user.email).count()
    return render_template('profile.html', name=current_user.name, user_events=event_query, count = events_number)
