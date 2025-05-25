from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.models.event import Event, Calendar
from datetime import datetime
from flask_login import login_required, current_user

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/calendar')
@login_required
def calendar():
    return render_template('calendar/index.html')

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