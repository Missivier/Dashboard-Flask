from peewee import *
import os
from dotenv import load_dotenv
import time
import psycopg2
from psycopg2 import OperationalError
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement du fichier .env
load_dotenv()
logger.info("Variables d'environnement chargées")

# Configuration par défaut pour Docker
DB_NAME = os.getenv('DB_NAME', 'mydb')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'db')  # Forcer l'utilisation de localhost
DB_PORT = int(os.getenv('DB_PORT', 5432))

logger.info(f"Configuration DB: {DB_HOST}:{DB_PORT}, DB: {DB_NAME}, User: {DB_USER}")

def wait_for_postgres(host, port, user, password, dbname, timeout=30):
    start = time.time()
    while True:
        try:
            logger.info(f"Tentative de connexion à PostgreSQL...")
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            conn.close()
            logger.info("✅ PostgreSQL est prêt.")
            break
        except OperationalError as e:
            if time.time() - start > timeout:
                logger.error(f"⛔ Timeout: PostgreSQL n'est pas prêt. Erreur: {str(e)}")
                raise Exception("⛔ Timeout: PostgreSQL n'est pas prêt.") from e
            logger.info(f"⏳ En attente de PostgreSQL... Erreur: {str(e)}")
            time.sleep(1)

# Configuration de la base de données PostgreSQL
db = PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

def init_database():
    """Initialise la connexion à la base de données"""
    logger.info("Début de l'initialisation de la base de données")
    
    try:
        # Attendre que PostgreSQL soit prêt
        wait_for_postgres(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        
        # Importer tous les modèles
        logger.info("Importation des modèles...")
        from app.models.user import User, Role
        from app.models.house import House
        from app.models.task import Task, ListTask, Status
        from app.models.budget import Budget
        from app.models.event import Event, Calendar
        from app.models.pet import Pet
        
        # Connecter et créer les tables
        logger.info("Connexion à la base de données...")
        db.connect()
        logger.info("Création des tables...")
        db.create_tables([
            Role, User, House, Status, Task, ListTask, Budget, 
            Calendar, Event, Pet
        ], safe=True)
        logger.info("Tables créées avec succès")
        db.close()
        logger.info("Initialisation de la base de données terminée")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de la base de données: {str(e)}")
        raise

class BaseModel(Model):
    """Modèle de base pour tous les modèles"""
    class Meta:
        database = db