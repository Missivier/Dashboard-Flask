from peewee import *
from app.models.bdd import BaseModel

class House(BaseModel):
    """Modèle pour les maisons"""
    id_house = AutoField(primary_key=True)
    name_house = CharField(max_length=100)
    adress = CharField(max_length=255)  # Note: "adress" comme dans le diagramme
    description_house = TextField(null=True)
    photo_house = CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name_house
    
    @property
    def address(self):
        """Alias pour une meilleure lisibilité"""
        return self.adress