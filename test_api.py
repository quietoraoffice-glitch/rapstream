from googleapiclient.discovery import build

API_KEY = "AIzaSyDDyYAO9WO32NVBetYxNiuDerH17Rl7i8I"

try:
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    # Test simple : chercher une vidéo
    request = youtube.search().list(
        q="rap gasy",
        part="snippet",
        type="video",
        maxResults=1
    )
    response = request.execute()
    
    if response.get('items'):
        print("✅ API fonctionnelle !")
        print(f"Première vidéo trouvée: {response['items'][0]['snippet']['title']}")
    else:
        print("❌ Aucune vidéo trouvée")
        
except Exception as e:
    print(f"❌ Erreur: {str(e)}")