# Dashboard Flask

Application de tableau de bord développée avec Flask.

## Description

Dashboard Flask est une application web moderne qui permet aux utilisateurs de visualiser et gérer leurs données de manière interactive. L'application offre :

- **Tableau de bord personnalisable** : Visualisation de données en temps réel avec des graphiques interactifs et des widgets configurables
- **Gestion des utilisateurs** : Système d'authentification complet avec différents niveaux d'accès (admin, utilisateur standard)
- **Interface intuitive** : Design responsive s'adaptant à tous les appareils (desktop, tablette, mobile)
- **Fonctionnalités avancées** :
  - Export de données en différents formats (CSV, PDF, Excel)
  - Filtres et recherche avancée
  - Notifications en temps réel
  - Historique des actions
  - Sauvegarde automatique des configurations

L'application est construite avec les technologies suivantes :

- **Backend** : Flask (Python)
- **Base de données** : PostgreSQL
- **Frontend** : HTML5, CSS3, JavaScript
- **Sécurité** : Protection CSRF, authentification sécurisée, sessions chiffrées

## Prérequis

- Python 3.11 ou supérieur
- PostgreSQL
- pip (gestionnaire de paquets Python)

## Installation

1. Cloner le repository :

```bash
git clone [URL_DU_REPO]
cd Dashboard-Flask
```

2. Créer et activer l'environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate  # Sur Unix/macOS
# ou
.\venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Configuration de l'environnement :
   - Créer un fichier `.env` à la racine du projet
   - Copier le contenu suivant et ajuster les valeurs selon votre environnement :

```env
# Configuration de l'application
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=votre_cle_secrete_ici
WTF_CSRF_SECRET_KEY=votre_cle_csrf_ici

# Configuration de la base de données
DB_NAME=mydb
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Configuration de sécurité
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=3600
MAX_CONTENT_LENGTH=16777216
```

5. Initialiser la base de données :

```bash
flask db init
flask db migrate
flask db upgrade
```

## Fonctionnalités

- Authentification des utilisateurs
- Gestion des profils
- Tableau de bord personnalisé
- Gestion des données
- Interface responsive

## Sécurité

L'application implémente plusieurs mesures de sécurité :

- Protection CSRF
- Gestion sécurisée des sessions
- Validation des mots de passe
- Protection contre les attaques par force brute
- Limitation de la taille des fichiers uploadés
- Cookies sécurisés

## Développement

Pour lancer l'application en mode développement :

```bash
flask run
```

L'application sera accessible à l'adresse : http://localhost:5000

## Production

Pour déployer en production :

1. Configurer les variables d'environnement appropriées
2. Utiliser un serveur WSGI (Gunicorn, uWSGI)
3. Configurer un serveur web (Nginx, Apache)
4. Activer HTTPS

## Tests

Pour exécuter les tests :

```bash
python -m pytest
```

## Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
