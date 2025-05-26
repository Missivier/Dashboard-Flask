"""
Pet model for the application.
Represents pets owned by users, including species, breed, and other details using Peewee ORM.
"""

from app.models.bdd import db
from app.models.user import User
from peewee import *
from datetime import datetime

class Pet(db.Model):
    """
    Model representing a pet owned by a user.
    Stores pet details such as name, species, breed, birth date, and weight.
    """
    id = AutoField(primary_key=True)
    name = CharField(max_length=100, null=False)
    species = CharField(max_length=50, null=False)
    breed = CharField(max_length=50, null=True)
    birth_date = DateField(null=True)
    weight = FloatField(null=True)
    owner = ForeignKeyField(User, backref='pets', null=False)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'pets'

    def save(self, *args, **kwargs):
        """
        Updates the 'updated_at' timestamp on every save.
        """
        self.updated_at = datetime.now()
        return super(Pet, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.species})"

    def to_dict(self):
        """
        Returns a dictionary representation of the pet instance.
        """
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
            'breed': self.breed,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'weight': self.weight,
            'owner_id': self.owner.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 