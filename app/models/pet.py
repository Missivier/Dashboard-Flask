from app.models.bdd import db
from app.models.user import User
from peewee import *
from datetime import date

class Pet(db.Model):
    id_pet = AutoField(primary_key=True)
    name_pet = CharField(max_length=100, null=False)
    species_pet = CharField(max_length=50, null=False)
    birth_date_pet = DateField(null=True)
    user = ForeignKeyField(User, backref='pets', null=False)

    class Meta:
        table_name = 'pets'

    @property
    def age(self):
        if self.birth_date_pet:
            today = date.today()
            age = today.year - self.birth_date_pet.year
            if (today.month, today.day) < (self.birth_date_pet.month, self.birth_date_pet.day):
                age -= 1
            return age
        return None

    def __str__(self):
        return f"{self.name_pet} ({self.species_pet})" 