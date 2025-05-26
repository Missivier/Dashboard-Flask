"""
Task, Status, and ListTask models for the application.
Defines the structure and relationships for task management using Peewee ORM.
"""

from peewee import *
from datetime import datetime
from app.models.bdd import BaseModel

class Status(BaseModel):
    """
    Model representing the status of a task (e.g., To Do, Done).
    """
    id_status = AutoField(primary_key=True)
    name_status = CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name_status

class ListTask(BaseModel):
    """
    Model representing a list of tasks (e.g., a project or category).
    """
    id_list_task = AutoField(primary_key=True)
    name_list_task = CharField(max_length=100)
    
    def __str__(self):
        return self.name_list_task

class Task(BaseModel):
    """
    Model representing an individual task.
    Includes relationships to status and list, and completion logic.
    """
    id_task = AutoField(primary_key=True)
    name_task = CharField(max_length=200)
    date_creation_task = DateTimeField(default=datetime.now)
    description_task = TextField(null=True)
    
    # Relationships
    status = ForeignKeyField(Status, backref='tasks', on_delete='SET NULL', null=True)
    list_task = ForeignKeyField(ListTask, backref='tasks', on_delete='SET NULL', null=True)
    
    def __str__(self):
        return self.name_task
    
    @property
    def is_completed(self):
        """
        Returns True if the task is marked as completed.
        """
        return self.status and self.status.name_status.lower() in ['terminé', 'completed', 'done']