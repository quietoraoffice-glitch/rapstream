from googleapiclient.discovery import build
from datetime import datetime
import re

def parse_duration(duration_str):
    """Parse une durée YouTube au format ISO 8601"""
    try:
        match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration_str)
        if not match:
            return 0
        
        hours = int(match.group(1)[:-1]) if match.group(1) else 0
        minutes = int(match.group(2)[:-1]) if match.group(2) else 0
        seconds = int(match.group(3)[:-1]) if match.group(3) else 0
        
        return hours * 3600 + minutes * 60 + seconds
    except:
        return 0

def get_existing_video_ids(youtube, playlist_id):
    """
    Récupère la liste de TOUS les video IDs déjà dans la playlist
    """
    existing_ids = set()
    next_page_token = None
    
    try:
        while True:
            request = youtube.playlistItems().list(
                playlistId=playlist_id,
                part='snippet',
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response.get('items', []):
                video_id = item['snippet']['resourceId']['videoId']
                existing_ids.add(video_id)
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
    
    except Exception as e:
        print(f"DEBUG: Erreur récupération playlist: {str(e)}")
    
    print(f"DEBUG: {len(existing_ids)} vidéos déjà dans la playlist")
    return existing_ids

def search_and_add_videos_with_api(youtube, playlist_id, keywords, max_results=50):
    """
    Recherche et ajoute avec clé API (pour production/Render)
    - Anti-doublons GLOBAL (vérifie avant d'ajouter)
    - Filtre par durée (2min+)
    - Toutes les chaînes
    """
    try:
        # Récupérer les vidéos existantes UNE FOIS
        existing_video_ids = get_existing_video_ids(youtube, playlist_id)
        
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
        too_short_count = 0
        added_videos = []
        
        items = response.get('items', [])
        print(f"DEBUG: Trouvé {len(items)} items pour '{keywords}'")
        
        for item in items:
            item_id = item.get('id', {})
            video_id = item_id.get('videoId')
            
            if not video_id:
                continue
            
            # ===== VÉRIFIER SI DÉJÀ DANS LA PLAYLIST =====
            if video_id in existing_video_ids:
                skipped_count += 1
                print(f"DEBUG: ⏭️ Déjà dans playlist: {video_id}")
                continue
            
            # ===== FILTRER PAR DURÉE (minimum 2 minutes) =====
            try:
                video_details = youtube.videos().list(
                    id=video_id,
                    part='contentDetails'
                ).execute()
                
                if not video_details.get('items'):
                    print(f"DEBUG: Vidéo {video_id} - pas de détails")
                    error_count += 1
                    continue
                
                duration_str = video_details['items'][0]['contentDetails']['duration']
                total_seconds = parse_duration(duration_str)
                
                # Rejeter si < 120 secondes (2 minutes)
                if total_seconds < 120:
                    too_short_count += 1
                    print(f"DEBUG: ⏭️ Vidéo trop courte ({total_seconds}s): {video_id}")
                    continue
                
                print(f"DEBUG: ✅ Durée OK ({total_seconds}s): {video_id}")
                
            except Exception as e:
                print(f"DEBUG: ❌ Erreur vérification durée: {str(e)}")
                error_count += 1
                continue
            
            # ===== RÉCUPÉRER LES INFOS =====
            snippet = item.get('snippet', {})
            title = snippet.get('title', 'Sans titre')
            channel = snippet.get('channelTitle', 'Inconnu')
            
            print(f"DEBUG: Traitement vidéo {video_id}: {title}")
            
            try:
                # Ajouter la vidéo à la playlist
                add_request = youtube.playlistItems().insert(
                    part='snippet',
                    body={
                        'snippet': {
                            'playlistId': playlist_id,
                            'resourceId': {
                                'kind': 'youtube#video',
                                'videoId': video_id
                            }
                        }
                    }
                )
                add_request.execute()
                
                # Ajouter à la liste locale pour éviter les doublons dans cette recherche
                existing_video_ids.add(video_id)
                
                added_videos.append({
                    'id': video_id,
                    'title': title,
                    'channel': channel,
                    'timestamp': datetime.now().isoformat()
                })
                added_count += 1
                print(f"DEBUG: ✅ Ajoutée")
                
            except Exception as e:
                error_msg = str(e).lower()
                if 'duplicate' in error_msg or 'already exists' in error_msg:
                    skipped_count += 1
                    print(f"DEBUG: ⏭️ Doublon détecté")
                else:
                    error_count += 1
                    print(f"DEBUG: ❌ Erreur: {str(e)}")
        
        print(f"DEBUG: Résumé '{keywords}' - Ajoutées: {added_count}, Doublons: {skipped_count}, Erreurs: {error_count}, Trop courtes: {too_short_count}")
        
        return {
            'added': added_count,
            'skipped': skipped_count,
            'errors': error_count,
            'too_short': too_short_count,
            'videos': added_videos
        }
    
    except Exception as e:
        print(f"DEBUG: Erreur critique: {str(e)}")
        raise Exception(f"Erreur lors de la recherche: {str(e)}")