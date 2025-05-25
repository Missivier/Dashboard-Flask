from peewee import *
import os

# Configuration de la base de données SQLite
db = SqliteDatabase(None)

def init_database(database_path):
    """Initialise la connexion à la base de données"""
    db.init(database_path)
    
    # Créer le répertoire si nécessaire
    os.makedirs(os.path.dirname(database_path), exist_ok=True)
    
    # Importer tous les modèles
    from app.models.user import User, Role
    from app.models.house import House
    from app.models.task import Task, ListTask, Status
    from app.models.budget import Budget
    from app.models.event import Event, Calendar
    from app.models.pet import Pet
    
    # Connecter et créer les tables
    db.connect()
    db.create_tables([
        Role, User, House, Status, Task, ListTask, Budget, 
        Calendar, Event, Pet
    ], safe=True)
    db.close()

class BaseModel(Model):
    """Modèle de base pour tous les modèles"""
    class Meta:
        database = db