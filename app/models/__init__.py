"""
Module des modèles de données avec Peewee ORM
"""

from app.models.bdd import db, init_database
from app.models.user import User

# Export des modèles principaux
__all__ = ['db', 'init_database', 'User']