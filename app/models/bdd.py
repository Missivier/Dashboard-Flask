"""
Database management module using Peewee ORM.
Handles database connection, initialization, and test database setup for the application.
"""

from peewee import *
import os
from dotenv import load_dotenv
import time
import psycopg2
from psycopg2 import OperationalError
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()
logger.info("Environment variables loaded")

# Database configuration from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5433')
DB_NAME = os.getenv('DB_NAME', 'mydb')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

logger.info(f"DB Config: {DB_HOST}:{DB_PORT}, DB: {DB_NAME}, User: {DB_USER}")

def wait_for_postgres(host, port, user, password, dbname, timeout=30):
    """
    Waits for the PostgreSQL server to be ready before connecting.
    Retries until the timeout is reached.
    """
    start = time.time()
    while True:
        try:
            logger.info(f"Trying to connect to PostgreSQL...")
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            conn.close()
            logger.info("✅ PostgreSQL is ready.")
            break
        except OperationalError as e:
            if time.time() - start > timeout:
                logger.error(f"⛔ Timeout: PostgreSQL is not ready. Error: {str(e)}")
                raise Exception("⛔ Timeout: PostgreSQL is not ready.") from e
            logger.info(f"⏳ Waiting for PostgreSQL... Error: {str(e)}")
            time.sleep(1)

# PostgreSQL database instance
# Used by all Peewee models
#
db = PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

def init_database():
    """
    Initializes the main PostgreSQL database and creates all tables.
    Imports all models and ensures tables are created.
    """
    logger.info("Starting database initialization")
    
    try:
        # Wait for PostgreSQL to be ready
        wait_for_postgres(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        
        # Import all models
        logger.info("Importing models...")
        from app.models.user import User, Role
        from app.models.house import House
        from app.models.task import Task, ListTask, Status
        from app.models.budget import Budget
        from app.models.pet import Pet
        
        # Connect and create tables
        logger.info("Connecting to database...")
        db.connect()
        logger.info("Creating tables...")
        db.create_tables([
            Role, User, House, Status, Task, ListTask, Budget, 
            Pet
        ], safe=True)
        logger.info("Tables created successfully")
        db.close()
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Error during database initialization: {str(e)}")
        raise

class BaseModel(Model):
    """
    Base model for all Peewee models in the application.
    Sets the database to use for all subclasses.
    """
    class Meta:
        database = db

def get_test_db():
    """
    Returns a SQLite in-memory database instance for testing purposes.
    """
    return SqliteDatabase(':memory:')

def init_test_database():
    """
    Initializes a SQLite in-memory database for running tests.
    Imports test models and creates their tables.
    """
    test_db = get_test_db()
    
    # Import models for testing
    from app.models.user import User
    from app.models.task import Task, Status, ListTask
    from app.models.budget import Budget
    
    # Create tables for tests
    test_db.create_tables([
        User,
        Status,
        ListTask,
        Task,
        Budget
    ])
    
    return test_db