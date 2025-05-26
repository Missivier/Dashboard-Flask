"""
Models package initializer for the application.
Imports and exposes main models and database utilities for use throughout the app.
"""

from app.models.bdd import db, init_database
from app.models.user import User

# Export main models and utilities
__all__ = ['db', 'init_database', 'User']