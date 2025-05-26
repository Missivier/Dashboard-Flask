"""
Calendar management routes for the application.
Handles CRUD operations for events and calendar views.
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.models.event import Event, Calendar
from datetime import datetime, timedelta
from flask_login import login_required, current_user

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/calendar')
@login_required
def index():
    """
    Displays the calendar view with all events.
    """
    events = Event.select().where(Event.user_id == current_user.id)
    return render_template('calendar/index.html', events=events)

@calendar_bp.route('/api/events')
@login_required
def get_events():
    events = Event.select().where(Event.user_id == current_user.id)
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'start': event.start_date.isoformat(),
        'end': event.end_date.isoformat() if event.end_date else None
    } for event in events])

@calendar_bp.route('/api/events', methods=['POST'])
@login_required
def create_event():
    data = request.json
    try:
        event = Event.create(
            title=data['title'],
            description=data.get('description'),
            start_date=datetime.fromisoformat(data['start']),
            end_date=datetime.fromisoformat(data['end']) if data.get('end') else None,
            user_id=current_user.id
        )
        return jsonify({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat() if event.end_date else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@calendar_bp.route('/api/events/<int:event_id>', methods=['PUT'])
@login_required
def update_event(event_id):
    event = Event.get_or_none(Event.id == event_id, Event.user_id == current_user.id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    try:
        data = request.json
        event.title = data.get('title', event.title)
        event.description = data.get('description', event.description)
        event.start_date = datetime.fromisoformat(data['start'])
        event.end_date = datetime.fromisoformat(data['end']) if data.get('end') else None
        event.save()
        
        return jsonify({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat() if event.end_date else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@calendar_bp.route('/api/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    event = Event.get_or_none(Event.id == event_id, Event.user_id == current_user.id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    try:
        event.delete_instance()
        return jsonify({'message': 'Event deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@calendar_bp.route('/calendar/new', methods=['GET', 'POST'])
@login_required
def new():
    """
    Creates a new calendar event.
    """
    # Implementation of the new route
    pass

@calendar_bp.route('/calendar/<int:id_event>/edit', methods=['GET', 'POST'])
@login_required
def edit(id_event):
    """
    Edits an existing calendar event.
    """
    # Implementation of the edit route
    pass

@calendar_bp.route('/calendar/<int:id_event>/delete', methods=['POST'])
@login_required
def delete(id_event):
    """
    Deletes a calendar event.
    """
    # Implementation of the delete route
    pass

@calendar_bp.route('/calendar/upcoming')
@login_required
def upcoming():
    """
    Displays upcoming events for the next 7 days.
    """
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    
    events = Event.select().where(
        (Event.user_id == current_user.id) &
        (Event.start_date >= today) &
        (Event.start_date <= next_week)
    ).order_by(Event.start_date)
    
    return render_template('calendar/upcoming.html', events=events)

@calendar_bp.route('/calendar/today')
@login_required
def today():
    """
    Displays events scheduled for today.
    """
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    events = Event.select().where(
        (Event.user_id == current_user.id) &
        (Event.start_date >= today) &
        (Event.start_date < tomorrow)
    ).order_by(Event.start_date)
    
    return render_template('calendar/today.html', events=events) 