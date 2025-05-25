import os
import sys

# Ajoute le chemin du projet pour les imports relatifs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.user import Role
from app.models.bdd import db

roles = ["ADMIN", "USER", "INVITE", "NO_HOUSE"]

if db.is_closed():
    db.connect()

for role_name in roles:
    role, created = Role.get_or_create(name_role=role_name)
    if created:
        print(f"Rôle '{role_name}' créé.")
    else:
        print(f"Rôle '{role_name}' existe déjà.")

db.close()