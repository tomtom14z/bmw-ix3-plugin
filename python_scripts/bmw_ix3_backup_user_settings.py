"""
Script Python pour sauvegarder les paramètres utilisateur
pour BMW iX3
"""
import json
import datetime
import logging

logger = logging.getLogger(__name__)

def backup_user_settings(target_soc, departure_time, auto_stop_enabled, additional_settings=None):
    """
    Sauvegarde les paramètres utilisateur
    
    Args:
        target_soc: Pourcentage de charge cible
        departure_time: Heure de départ
        auto_stop_enabled: Arrêt automatique activé
        additional_settings: Paramètres supplémentaires
    
    Returns:
        dict: Résultat de la sauvegarde
    """
    try:
        # Préparation des données à sauvegarder
        settings = {
            "timestamp": datetime.datetime.now().isoformat(),
            "target_soc": target_soc,
            "departure_time": departure_time,
            "auto_stop_enabled": auto_stop_enabled,
            "additional_settings": additional_settings or {}
        }
        
        # Sauvegarde dans un fichier JSON
        backup_filename = f"/config/bmw_ix3_settings_backup_{datetime.date.today().strftime('%Y%m%d')}.json"
        
        with open(backup_filename, 'w') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        
        # Sauvegarde dans le fichier principal
        main_backup_file = "/config/bmw_ix3_user_settings.json"
        with open(main_backup_file, 'w') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "backup_file": backup_filename,
            "main_file": main_backup_file,
            "settings_count": len(settings)
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def restore_user_settings(backup_file=None):
    """
    Restaure les paramètres utilisateur depuis une sauvegarde
    
    Args:
        backup_file: Fichier de sauvegarde (optionnel)
    
    Returns:
        dict: Paramètres restaurés
    """
    try:
        if not backup_file:
            backup_file = "/config/bmw_ix3_user_settings.json"
        
        with open(backup_file, 'r') as f:
            settings = json.load(f)
        
        return {
            "success": True,
            "settings": settings,
            "restored_at": datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la restauration: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def get_backup_history():
    """
    Récupère l'historique des sauvegardes
    
    Returns:
        list: Liste des sauvegardes disponibles
    """
    try:
        import os
        import glob
        
        backup_files = glob.glob("/config/bmw_ix3_settings_backup_*.json")
        backups = []
        
        for backup_file in backup_files:
            try:
                with open(backup_file, 'r') as f:
                    settings = json.load(f)
                    backups.append({
                        "file": backup_file,
                        "timestamp": settings.get("timestamp"),
                        "target_soc": settings.get("target_soc"),
                        "departure_time": settings.get("departure_time")
                    })
            except:
                continue
        
        # Tri par date (plus récent en premier)
        backups.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return backups
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'historique: {e}")
        return []

def cleanup_old_backups(keep_days=30):
    """
    Nettoie les anciennes sauvegardes
    
    Args:
        keep_days: Nombre de jours à conserver
    """
    try:
        import os
        import glob
        
        backup_files = glob.glob("/config/bmw_ix3_settings_backup_*.json")
        cutoff_date = datetime.date.today() - datetime.timedelta(days=keep_days)
        
        deleted_count = 0
        for backup_file in backup_files:
            try:
                # Extraire la date du nom de fichier
                date_str = backup_file.split('_')[-1].replace('.json', '')
                file_date = datetime.datetime.strptime(date_str, '%Y%m%d').date()
                
                if file_date < cutoff_date:
                    os.remove(backup_file)
                    deleted_count += 1
            except:
                continue
        
        return {
            "success": True,
            "deleted_count": deleted_count,
            "cutoff_date": cutoff_date.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du nettoyage: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# Fonction principale pour Home Assistant
def main():
    """Fonction principale appelée par Home Assistant"""
    # Récupération des paramètres actuels
    target_soc = float(data.get("target_soc", 80))
    departure_time = data.get("departure_time", "08:00")
    auto_stop_enabled = data.get("auto_stop_enabled", True)
    
    # Paramètres supplémentaires
    additional_settings = {
        "charging_mode": data.get("charging_mode", "Économique (80%)"),
        "weather_optimization": data.get("weather_optimization", False),
        "off_peak_optimization": data.get("off_peak_optimization", True)
    }
    
    # Sauvegarde des paramètres
    backup_result = backup_user_settings(
        target_soc, departure_time, auto_stop_enabled, additional_settings
    )
    
    if backup_result["success"]:
        # Mise à jour des entités Home Assistant
        hass.states.set("sensor.bmw_ix3_last_backup", backup_result["timestamp"])
        hass.states.set("sensor.bmw_ix3_backup_status", "Sauvegardé")
        
        # Nettoyage des anciennes sauvegardes
        cleanup_result = cleanup_old_backups()
        
        # Notification de succès
        hass.services.call(
            "notify", "mobile_app_iphone",
            {
                "title": "BMW iX3 - Sauvegarde",
                "message": f"✅ Paramètres sauvegardés ({backup_result['settings_count']} éléments)"
            }
        )
        
        logger.info(f"Sauvegarde réussie: {backup_result}")
    else:
        # Notification d'erreur
        hass.services.call(
            "notify", "mobile_app_iphone",
            {
                "title": "BMW iX3 - Erreur sauvegarde",
                "message": f"❌ Erreur: {backup_result['error']}"
            }
        )
        
        logger.error(f"Échec de la sauvegarde: {backup_result}")

if __name__ == "__main__":
    main()

