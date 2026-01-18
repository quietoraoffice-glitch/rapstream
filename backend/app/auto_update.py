import os
import json
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv('config/.env')

PLAYLIST_ID = os.getenv('PLAYLIST_ID')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
LOG_FILE = 'logs/auto_update.log'

# Créer le dossier logs s'il n'existe pas
os.makedirs('logs', exist_ok=True)

# Keywords optimisés pour RAP GASY avec codes de ville
KEYWORDS_LIST = [
    # Base
    "rap malagasy",
    "rap gasy",
    "hip hop malagasy",
    "hip hop gasy",
    "rap madagascar",
    
    # Locale / scène
    "rap tanà",
    "rap tana",
    "hira rap",
    "hira vaovao",
    "vaovao rap",
    
    # Paroles
    "tononkira",
    "paroles rap gasy",
    "lyrics rap malagasy",
    "lyric video gasy",
    
    # Formats
    "rap gasy clip officiel",
    "official video rap malagasy",
    "official audio rap gasy",
    "freestyle rap malagasy",
    "live rap gasy",
    
    # Collabs & dynamique
    "rap gasy feat",
    "rap malagasy featuring",
    "remix rap gasy",
    "cypher rap malagasy",
    "rap gasy diss",
    
    # Sous-genres
    "trap malagasy",
    "drill malagasy",
    "boom bap malagasy",
    "old school rap malagasy",
    "underground rap malagasy",
    
    # Codes de ville
    "rap 501",  # Tamatave
    "rap 502",  # Antalaha
    "rap 503",  # Sambava
    "rap 504",  # Soanierana Ivongo
    "rap 505",  # Vohémar
    "rap 506",  # Antsiranana
    "rap 601",  # Mahajanga
    "rap 602",  # Soalala
    "rap 603",  # Mitsinjo
    "rap 701",  # Toliary
    "rap 702",  # Betioky
    "rap 703",  # Ampanihi
    "rap 801",  # Fianarantsoa
    "rap 901",  # Antananarivo
    
    # Artistes/Groupes connus
    "cyphaka",
    "zaza rap taiza",
    "kolotsaina mainty",
]

def log_update(message):
    """Sauvegarde les logs des mises à jour"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

def automatic_update():
    """
    Effectue une mise à jour automatique de la playlist
    Recherche les nouvelles vidéos RAP Gasy et les ajoute
    - 50 résultats par requête
    - Anti-doublons global
    - Durée minimale: 2 minutes
    - Toutes les chaînes
    """
    log_update("=" * 70)
    log_update("🔄 DÉBUT DE LA MISE À JOUR AUTOMATIQUE")
    log_update(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_update(f"🔍 Total mots-clés à traiter: {len(KEYWORDS_LIST)}")
    log_update("=" * 70)
    
    try:
        # Importer la fonction de recherche
        from .search_api import search_and_add_videos_with_api
        from googleapiclient.discovery import build
        
        # Construire le service YouTube avec clé API
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        total_added = 0
        total_skipped = 0
        total_errors = 0
        skipped_details = []
        
        for idx, keywords in enumerate(KEYWORDS_LIST, 1):
            log_update(f"\n[{idx}/{len(KEYWORDS_LIST)}] 🔍 Recherche: '{keywords}'")
            
            try:
                result = search_and_add_videos_with_api(
                    youtube,
                    PLAYLIST_ID,
                    keywords,
                    max_results=50  # 50 résultats par requête
                )
                
                if result:
                    added = result.get('added', 0)
                    skipped = result.get('skipped', 0)
                    errors = result.get('errors', 0)
                    
                    total_added += added
                    total_skipped += skipped
                    total_errors += errors
                    
                    status = "✅" if added > 0 else "⏭️"
                    log_update(f"  {status} Ajoutées: {added} | ⏭️ Doublons: {skipped} | ❌ Erreurs: {errors}")
                    
                    if skipped > 0:
                        skipped_details.append(f"  • {keywords}: {skipped} doublons")
                else:
                    log_update(f"  ⚠️ Erreur lors de la recherche")
                    total_errors += 1
                
                # Petit délai pour ne pas surcharger l'API
                time.sleep(1)
                
            except Exception as e:
                log_update(f"  ❌ Erreur critique: {str(e)}")
                total_errors += 1
        
        # Résumé final
        log_update("\n" + "=" * 70)
        log_update("📊 RÉSUMÉ DE LA MISE À JOUR")
        log_update("=" * 70)
        log_update(f"✅ Total vidéos ajoutées: {total_added}")
        log_update(f"⏭️ Total doublons détectés: {total_skipped}")
        if skipped_details:
            log_update(f"\n📌 Détails des doublons:")
            for detail in skipped_details[:10]:  # Afficher les 10 premiers
                log_update(detail)
            if len(skipped_details) > 10:
                log_update(f"  ... et {len(skipped_details) - 10} autres")
        
        log_update(f"❌ Total erreurs: {total_errors}")
        log_update(f"✨ Mise à jour terminée à {datetime.now().strftime('%H:%M:%S')}")
        log_update("=" * 70 + "\n")
        
        # Retourner les stats
        return {
            'added': total_added,
            'skipped': total_skipped,
            'errors': total_errors,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        log_update(f"❌ ERREUR CRITIQUE DANS LA MISE À JOUR: {str(e)}")
        import traceback
        log_update(traceback.format_exc())
        return None

def start_scheduler():
    """
    Démarre le scheduler qui exécute les mises à jour toutes les 3 heures
    Utilisé EN LOCAL uniquement
    """
    log_update("🚀 Scheduler démarré - Mises à jour toutes les 3 heures")
    
    # Programmer la mise à jour toutes les 3 heures
    schedule.every(3).hours.do(automatic_update)
    
    # Exécuter une fois au démarrage
    automatic_update()
    
    # Boucle infinie du scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)  # Vérifier toutes les minutes

def start_scheduler_background():
    """
    Lance le scheduler en arrière-plan (pour déploiement local)
    Utilisé EN LOCAL uniquement
    """
    import threading
    
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    
    log_update("🔄 Scheduler lancé en arrière-plan (mise à jour toutes les 3 heures)")