from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import usersDB
from .models import Event
from datetime import datetime

events = Blueprint('edit_event', __name__)


@events.route('/create_event')
@login_required
def createevent():
    return render_template('create_event.html', today=datetime.today())


@events.route('/create_event', methods=['POST'])
def createevent_post():
    email = current_user.email
    name = current_user.name
    category = request.form.get('category')
    place = request.form.get('place')
    address = request.form.get('address')
    startDate = request.form.get('startDate')
    endDate = request.form.get('endDate')
    isVirtual = True if request.form.get('isVirtual') else False

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_event = Event(email=email,
                      name=name,
                      category=category,
                      place=place,
                      address=address,
                      startDate=datetime.strptime(startDate, '%Y-%m-%d'),
                      endDate=datetime.strptime(endDate, '%Y-%m-%d'),
                      isVirtual=isVirtual)
    print(new_event)
    # add the new user to the database
    if endDate >= startDate:
        usersDB.session.add(new_event)
        usersDB.session.commit()
        flash('Evento creado.', 'created')
    else:
        flash('Fechas no válidas. Intente crear el evento de nuevo.', 'error')

    return redirect(url_for('main.profile'))


@events.route('/event_description')
@login_required
def description():
    return redirect(url_for('main.profile'))


@events.route('/event_description', methods=['POST', 'DELETE', 'PUT'])
@login_required
def description_post():
    if request.form.get('_method') is None:
        see_id = request.form.get('id_edit')
        print(see_id)
        print("POST" + request.method)
        see_event = Event.query.filter_by(id=see_id).first()

        return render_template('event_description.html', event_id=see_id, event=see_event)

    if request.form.get('_method') == "DELETE" or request.method == "DELETE":
        delete_id = request.form.get('delete_id')
        print(delete_id)
        print("DELETE" + request.method)
        see_event = Event.query.filter_by(id=delete_id).first()
        # delete the event to the database
        usersDB.session.delete(see_event)
        usersDB.session.commit()
        flash('Evento borrado.', 'deleted')
        return redirect(url_for('main.profile'))

    if request.form.get('_method') == "PUT" or request.method == "PUT":
        edit_id = request.form.get('edit_id')
        edit_event = Event.query.filter_by(id=edit_id).first()
        edit_event.category = request.form.get('category')
        edit_event.place = request.form.get('place')
        edit_event.address = request.form.get('address')
        edit_event.startDate = datetime.strptime(request.form.get('startDate'), '%Y-%m-%d')
        edit_event.endDate = datetime.strptime(request.form.get('endDate'), '%Y-%m-%d')
        edit_event.isVirtual = True if request.form.get('isVirtual') else False
        print(edit_id)
        print("PUT" + request.method)
        # delete the event to the database
        if request.form.get('endDate') >= request.form.get('startDate'):
            usersDB.session.commit()
            flash('Evento actualizado.', 'edited')
        else:
            flash('Fechas no válidas. Intente editar el evento de nuevo.', 'error')
        return redirect(url_for('main.profile'))

