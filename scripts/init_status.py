import os
import sys

# Ajoute le chemin du projet pour les imports relatifs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.task import Status
from app.models.bdd import db

status_list = ["En cours", "Terminé", "En attente"]

if db.is_closed():
    db.connect()

for status_name in status_list:
    status, created = Status.get_or_create(name_status=status_name)
    if created:
        print(f"Statut '{status_name}' créé.")
    else:
        print(f"Statut '{status_name}' existe déjà.")

db.close() 