import os
import json
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime
import sys

# Charger les variables d'environnement
load_dotenv('config/.env')

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
PLAYLIST_ID = os.getenv('PLAYLIST_ID')

def search_and_add_videos(keywords, max_results=50):
    """
    Recherche des vidéos YouTube et les ajoute à la playlist
    
    Args:
        keywords (str): Mots-clés de recherche
        max_results (int): Nombre max de résultats
    """
    
    if not YOUTUBE_API_KEY or not PLAYLIST_ID:
        print("❌ Erreur: Variables d'environnement manquantes!")
        print("   Vérifiez config/.env")
        return None
    
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        print(f"\n{'='*60}")
        print(f"🔍 Recherche: '{keywords}'")
        print(f"{'='*60}\n")
        
        # Rechercher les vidéos
        request = youtube.search().list(
            q=keywords,
            part='snippet',
            type='video',
            maxResults=max_results,
            relevanceLanguage='fr',
            order='relevance'
        )
        response = request.execute()
        
        added_count = 0
        skipped_count = 0
        error_count = 0
        added_videos = []
        
        for item in response.get('items', []):
            # Vérifier que c'est bien une vidéo
            if 'videoId' not in item['snippet'].get('resourceId', {}):
                continue
            
            video_id = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            channel = item['snippet']['channelTitle']
            
            try:
                # Ajouter la vidéo à la playlist
                add_request = youtube.playlistItems().insert(
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
                add_request.execute()
                
                added_videos.append({
                    'id': video_id,
                    'title': title,
                    'channel': channel,
                    'timestamp': datetime.now().isoformat()
                })
                added_count += 1
                print(f"  ✅ {title[:60]}...")
                
            except Exception as e:
                error_msg = str(e).lower()
                if 'duplicate' in error_msg or 'already exists' in error_msg:
                    skipped_count += 1
                    print(f"  ⏭️  [DOUBLON] {title[:60]}...")
                else:
                    error_count += 1
                    print(f"  ❌ [ERREUR] {title[:60]}...")
        
        # Sauvegarder les résultats
        results = {
            'search_query': keywords,
            'timestamp': datetime.now().isoformat(),
            'added': added_count,
            'skipped': skipped_count,
            'errors': error_count,
            'videos': added_videos
        }
        
        with open('scripts/search_results.json', 'a', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            f.write('\n---\n')
        
        print(f"\n{'='*60}")
        print(f"📊 RÉSUMÉ DE LA RECHERCHE")
        print(f"{'='*60}")
        print(f"  ✅ Vidéos ajoutées: {added_count}")
        print(f"  ⏭️  Vidéos en doublon: {skipped_count}")
        print(f"  ❌ Erreurs: {error_count}")
        print(f"  📺 Total trouvé: {added_count + skipped_count + error_count}")
        print(f"{'='*60}\n")
        
        return {
            'added': added_count,
            'skipped': skipped_count,
            'errors': error_count,
            'videos': added_videos
        }
    
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {str(e)}\n")
        return None

def interactive_search():
    """Mode interactif pour rechercher et ajouter des vidéos"""
    print("\n" + "="*60)
    print("🎤 RAP GASY STREAMING - RECHERCHE ET AJOUT DE VIDÉOS")
    print("="*60 + "\n")
    
    while True:
        keywords = input("Entrez les mots-clés de recherche (ou 'quitter' pour exit): ").strip()
        
        if keywords.lower() in ['quitter', 'exit', 'q']:
            print("\n👋 Bye!\n")
            break
        
        if not keywords:
            print("⚠️  Veuillez entrer au moins un mot-clé\n")
            continue
        
        max_results_input = input("Nombre max de résultats (défaut 50): ").strip()
        max_results = 50
        
        if max_results_input.isdigit():
            max_results = int(max_results_input)
        
        result = search_and_add_videos(keywords, max_results)
        
        if result:
            input("\nAppuyez sur Entrée pour continuer...")
        else:
            print("\n⚠️  La recherche a échoué. Vérifiez vos identifiants.\n")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Mode ligne de commande
        keywords = ' '.join(sys.argv[1:])
        search_and_add_videos(keywords)
    else:
        # Mode interactif
        interactive_search()