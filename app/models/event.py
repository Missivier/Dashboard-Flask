from peewee import *
from datetime import datetime
from app.models.bdd import BaseModel
from app import db

class Calendar(BaseModel):
    """Modèle pour les calendriers"""
    id_calendar = AutoField(primary_key=True)
    name_calendar = CharField(max_length=100)
    
    def __str__(self):
        return self.name_calendar

class Event(Model):
    """Modèle pour les événements"""
    id = AutoField(primary_key=True)
    title = CharField(max_length=200)
    description = TextField(null=True)
    start_date = DateTimeField()
    end_date = DateTimeField(null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    user_id = IntegerField()
    
    # Relations
    calendar = ForeignKeyField(Calendar, backref='events', on_delete='CASCADE', null=True)
    
    def __str__(self):
        return self.title
    
    @property
    def duration(self):
        """Calcule la durée de l'événement"""
        if self.end_date:
            return self.end_date - self.start_date
        return None
    
    def is_all_day(self):
        """Vérifie si l'événement dure toute la journée"""
        if self.end_date:
            return (self.end_date - self.start_date).days >= 1
        return False
    
    def is_ongoing(self):
        """Vérifie si l'événement est en cours"""
        now = datetime.now()
        if self.end_date:
            return self.start_date <= now <= self.end_date
        return self.start_date <= now
    
    def is_upcoming(self):
        """Vérifie si l'événement est à venir"""
        return self.start_date > datetime.now()
    
    def is_past(self):
        """Vérifie si l'événement est passé"""
        end_time = self.end_date or self.start_date
        return end_time < datetime.now()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(Event, self).save(*args, **kwargs)

    class Meta:
        database = db
        table_name = 'events'