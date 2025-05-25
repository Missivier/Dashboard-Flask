from peewee import *
from datetime import datetime
from app.models.bdd import BaseModel

class Pet(BaseModel):
    """Modèle pour les animaux de compagnie"""
    id_pet = AutoField(primary_key=True)
    name_pet = CharField(max_length=100)
    date_birthday_pet = DateField(null=True)
    type_pet = CharField(max_length=50)  # Chat, Chien, etc.
    description_pet = TextField(null=True)
    photo_pet = CharField(max_length=255, null=True)
    
    def __str__(self):
        return f"{self.name_pet} ({self.type_pet})"
    
    @property
    def age(self):
        """Calcule l'âge de l'animal"""
        if self.date_birthday_pet:
            today = datetime.now().date()
            age_years = today.year - self.date_birthday_pet.year
            
            # Ajuster si l'anniversaire n'est pas encore passé cette année
            if (today.month, today.day) < (self.date_birthday_pet.month, self.date_birthday_pet.day):
                age_years -= 1
                
            return age_years
        return None
    
    def get_age_string(self):
        """Retourne l'âge sous forme de chaîne"""
        age = self.age
        if age is not None:
            if age == 0:
                # Calculer en mois pour les très jeunes animaux
                today = datetime.now().date()
                months = (today.year - self.date_birthday_pet.year) * 12 + (today.month - self.date_birthday_pet.month)
                return f"{months} mois" if months > 1 else "moins d'un mois"
            else:
                return f"{age} an{'s' if age > 1 else ''}"
        return "Âge inconnu"