"""
House model for the application.
Represents a house entity with address and description fields using Peewee ORM.
"""

from peewee import *
from app.models.bdd import BaseModel

class House(BaseModel):
    """
    Model representing a house entity.
    Stores house name, address, description, and photo.
    """
    id_house = AutoField(primary_key=True)
    name_house = CharField(max_length=100)
    adress = CharField(max_length=255)  # Note: 'adress' as in the original schema
    description_house = TextField(null=True)
    photo_house = CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name_house
    
    @property
    def address(self):
        """
        Alias for the 'adress' field for better readability.
        """
        return self.adress