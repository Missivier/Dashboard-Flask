"""
Module des modèles de données avec Peewee ORM
"""

from app.models.bdd import db, BaseModel, init_database
from app.models.user import User, Role
from app.models.house import House
from app.models.task import Task, ListTask, Status
from app.models.budget import Budget
from app.models.event import Event, Calendar
from app.models.pet import Pet

# Export des modèles principaux
__all__ = [
    'db', 'BaseModel', 'init_database',
    'User', 'Role', 'House', 'Task', 'ListTask', 'Status',
    'Budget', 'Event', 'Calendar', 'Pet'
]