"""
Event and Calendar models for the application.
Defines calendar and event management, including duration and status logic, using Peewee ORM.
"""

from peewee import *
from datetime import datetime
from app.models.bdd import BaseModel
from app import db

class Calendar(BaseModel):
    """
    Model representing a calendar entity.
    Stores the name of the calendar.
    """
    id_calendar = AutoField(primary_key=True)
    name_calendar = CharField(max_length=100)
    
    def __str__(self):
        return self.name_calendar

class Event(Model):
    """
    Model representing an event in a calendar.
    Stores event details, timing, and provides utility methods for event status.
    """
    id = AutoField(primary_key=True)
    title = CharField(max_length=200)
    description = TextField(null=True)
    start_date = DateTimeField()
    end_date = DateTimeField(null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    user_id = IntegerField()
    
    # Relationships
    calendar = ForeignKeyField(Calendar, backref='events', on_delete='CASCADE', null=True)
    
    def __str__(self):
        return self.title
    
    @property
    def duration(self):
        """
        Returns the duration of the event as a timedelta, or None if not applicable.
        """
        if self.end_date:
            return self.end_date - self.start_date
        return None
    
    def is_all_day(self):
        """
        Returns True if the event lasts all day or more.
        """
        if self.end_date:
            return (self.end_date - self.start_date).days >= 1
        return False
    
    def is_ongoing(self):
        """
        Returns True if the event is currently ongoing.
        """
        now = datetime.now()
        if self.end_date:
            return self.start_date <= now <= self.end_date
        return self.start_date <= now
    
    def is_upcoming(self):
        """
        Returns True if the event is in the future.
        """
        return self.start_date > datetime.now()
    
    def is_past(self):
        """
        Returns True if the event has ended.
        """
        end_time = self.end_date or self.start_date
        return end_time < datetime.now()

    def save(self, *args, **kwargs):
        """
        Updates the 'updated_at' timestamp on every save.
        """
        self.updated_at = datetime.now()
        return super(Event, self).save(*args, **kwargs)

    class Meta:
        database = db
        table_name = 'events'