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

def search_and_add_videos_with_api(youtube, playlist_id, keywords, max_results=50):
    """
    Recherche et ajoute avec clé API (pour production/Render)
    """
    try:
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
            
            # Filtrer par durée
            try:
                video_details = youtube.videos().list(
                    id=video_id,
                    part='contentDetails'
                ).execute()
                
                if not video_details.get('items'):
                    error_count += 1
                    continue
                
                duration_str = video_details['items'][0]['contentDetails']['duration']
                total_seconds = parse_duration(duration_str)
                
                if total_seconds < 120:
                    too_short_count += 1
                    continue
                
            except Exception as e:
                print(f"DEBUG: Erreur durée: {str(e)}")
                error_count += 1
                continue
            
            snippet = item.get('snippet', {})
            title = snippet.get('title', 'Sans titre')
            channel = snippet.get('channelTitle', 'Inconnu')
            
            try:
                youtube.playlistItems().insert(
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
                ).execute()
                
                added_videos.append({
                    'id': video_id,
                    'title': title,
                    'channel': channel,
                    'timestamp': datetime.now().isoformat()
                })
                added_count += 1
                
            except Exception as e:
                if 'duplicate' in str(e).lower():
                    skipped_count += 1
                else:
                    error_count += 1
        
        return {
            'added': added_count,
            'skipped': skipped_count,
            'errors': error_count,
            'videos': added_videos
        }
    
    except Exception as e:
        raise Exception(f"Erreur: {str(e)}")