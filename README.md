# RAP Gasy Streaming 🎤🎵

Une application web moderne pour découvrir et gérer une playlist YouTube dédiée au RAP Gasy.

## Structure du projet

\\\
rapstream/
├── backend/               # API FastAPI
│   ├── app/
│   │   └── main.py       # Application FastAPI
│   └── requirements.txt   # Dépendances Python
├── frontend/             # Application React
│   ├── src/
│   └── package.json
├── scripts/              # Scripts utilitaires
│   └── search_and_add.py # Script de recherche YouTube
├── config/               # Configuration
│   └── .env.example
└── docs/                 # Documentation
\\\

## Installation

### Backend

\\\ash
# 1. Créer un environnement virtuel Python
python -m venv venv

# 2. Activer l'environnement
# Windows
.\venv\Scripts\activate

# 3. Installer les dépendances
pip install -r backend/requirements.txt

# 4. Configurer les variables d'environnement
cp config/.env.example config/.env
# Éditer config/.env avec vos clés API
\\\

### Frontend

\\\ash
# 1. Installer les dépendances
npm install

# 2. Lancer le serveur de développement
npm run dev
\\\

## Configuration

1. Créez un compte Google Cloud
2. Activez YouTube Data API v3
3. Créez une clé API
4. Créez une playlist YouTube et notez son ID
5. Remplissez le fichier \config/.env\

## Utilisation

### Lancer le backend
\\\ash
python backend/app/main.py
\\\

### Rechercher et ajouter des vidéos
\\\ash
python scripts/search_and_add.py
\\\

### Lancer le frontend
\\\ash
npm run dev
\\\

## Fonctionnalités

✅ Affichage de la playlist YouTube  
✅ Lecture directe sur YouTube  
✅ Recherche automatique et ajout de vidéos  
✅ Interface moderne et responsive  

## License

MIT
