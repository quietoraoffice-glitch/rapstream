from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# Imports relatifs
from .auth import get_authenticated_service
from .models import SearchRequest
from .auto_update import start_scheduler_background

# Charger les variables d'environnement
load_dotenv('config/.env')

app = FastAPI(
    title="RAP Gasy Streaming API",
    description="API pour gérer la playlist YouTube RAP Gasy",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
PLAYLIST_ID = os.getenv('PLAYLIST_ID')

@app.on_event("startup")
async def startup_event():
    """Lance le scheduler en arrière-plan au démarrage"""
    start_scheduler_background()
    print("✅ Scheduler de mise à jour automatique lancé !")

@app.get("/")
def read_root():
    return {
        "message": "RAP Gasy Streaming API",
        "version": "1.0.0",
        "status": "✅ Running"
    }

@app.get("/api/videos")
def get_playlist_videos():
    """Récupère les vidéos de la playlist YouTube"""
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        request = youtube.playlistItems().list(
            playlistId=PLAYLIST_ID,
            part='snippet',
            maxResults=50
        )
        response = request.execute()
        
        videos = []
        for item in response.get('items', []):
            videos.append({
                'id': item['snippet']['resourceId']['videoId'],
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['default']['url'],
                'url': f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}"
            })
        
        return {'videos': videos, 'count': len(videos)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search-and-add")
def search_and_add(request: SearchRequest):
    """
    Recherche et ajoute des vidéos à la playlist
    En production (Render): utilise clé API
    En local: utilise OAuth2 avec credentials.json
    """
    try:
        # Utiliser la clé API pour les recherches et ajouts
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        # Importer la fonction de recherche
        from .search_api import search_and_add_videos_with_api
        
        result = search_and_add_videos_with_api(
            youtube,
            PLAYLIST_ID,
            request.keywords,
            request.max_results
        )
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/add-video")
def add_video_to_playlist(video_id: str):
    """Ajoute une vidéo à la playlist"""
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        request = youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': PLAYLIST_ID,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        )
        response = request.execute()
        return {'status': 'success', 'videoId': video_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)