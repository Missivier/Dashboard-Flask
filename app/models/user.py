from peewee import *
from datetime import datetime
from app.models.bdd import BaseModel
from flask_login import UserMixin
from app.models.house import House

class Role(BaseModel):
    """Modèle pour les rôles utilisateur"""
    id_role = AutoField(primary_key=True)
    name_role = CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name_role

class User(BaseModel, UserMixin):
    """Modèle pour les utilisateurs"""
    id_user = AutoField(primary_key=True)
    name_user = CharField(max_length=100)
    first_name_user = CharField(max_length=100)
    username_user = CharField(max_length=50, unique=True)
    phone_user = CharField(max_length=20, null=True)
    age_user = IntegerField(null=True)
    date_birthday_user = DateField(null=True)
    email_user = CharField(max_length=150, unique=True)
    date_inscription = DateTimeField(default=datetime.now)
    description_user = TextField(null=True)
    photo_user = CharField(max_length=255, null=True)
    password = CharField()
    is_active = BooleanField(default=True)
    
    # Relations
    role = ForeignKeyField(Role, backref='users', on_delete='SET NULL', null=True)
    house = ForeignKeyField(House, backref='users', on_delete='SET NULL', null=True)
    is_admin_house = BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name_user} {self.name_user}"
    
    @property
    def full_name(self):
        return f"{self.first_name_user} {self.name_user}"
    
    def get_age_from_birthday(self):
        """Calcule l'âge à partir de la date de naissance"""
        if self.date_birthday_user:
            today = datetime.now().date()
            return today.year - self.date_birthday_user.year - (
                (today.month, today.day) < (self.date_birthday_user.month, self.date_birthday_user.day)
            )
        return self.age_user

    def __repr__(self):
        return f'<User {self.email_user}>'