from peewee import *
from datetime import datetime
from app.models.bdd import BaseModel

class Status(BaseModel):
    """Modèle pour les statuts des tâches"""
    id_status = AutoField(primary_key=True)
    name_status = CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name_status

class ListTask(BaseModel):
    """Modèle pour les listes de tâches"""
    id_list_task = AutoField(primary_key=True)
    name_list_task = CharField(max_length=100)
    
    def __str__(self):
        return self.name_list_task

class Task(BaseModel):
    """Modèle pour les tâches"""
    id_task = AutoField(primary_key=True)
    name_task = CharField(max_length=200)
    date_creation_task = DateTimeField(default=datetime.now)
    description_task = TextField(null=True)
    
    # Relations
    status = ForeignKeyField(Status, backref='tasks', on_delete='SET NULL', null=True)
    list_task = ForeignKeyField(ListTask, backref='tasks', on_delete='SET NULL', null=True)
    
    def __str__(self):
        return self.name_task
    
    @property
    def is_completed(self):
        """Vérifie si la tâche est terminée"""
        return self.status and self.status.name_status.lower() in ['terminé', 'completed', 'done']