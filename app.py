from app import create_app
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Démarrage de l'application Flask...")
app = create_app()

if __name__ == '__main__':
    logger.info("Lancement du serveur Flask sur http://127.0.0.1:5000")
    app.run(debug=True)
