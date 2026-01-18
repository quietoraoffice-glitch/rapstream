import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Fichier où stocker le token
TOKEN_FILE = 'config/token.pickle'
CREDENTIALS_FILE = 'config/credentials.json'

# Scopes nécessaires pour accéder à YouTube
SCOPES = ['https://www.googleapis.com/auth/youtube']

def get_authenticated_service():
    """
    Retourne un service YouTube authentifié avec OAuth2
    """
    creds = None
    
    # Charger le token existant s'il existe
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # Si pas de credentials valides, faire l'authentification
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Créer un nouveau flux d'authentification
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8888)
        
        # Sauvegarder le token pour la prochaine fois
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    # Construire le service YouTube
    from googleapiclient.discovery import build
    youtube = build('youtube', 'v3', credentials=creds)
    
    return youtube

def refresh_token():
    """
    Rafraîchit le token OAuth2
    """
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
        
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
            
            return True
    
    return False