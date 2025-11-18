"""Système d'apprentissage des courbes de recharge BMW iX3."""
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Catégories de puissance de chargeur (kW)
CHARGER_CATEGORIES = {
    "7kw": (5.0, 9.0),      # 5-9 kW (chargeur domestique)
    "11kw": (9.0, 15.0),    # 9-15 kW (chargeur triphasé)
    "22kw": (15.0, 30.0),   # 15-30 kW (chargeur public)
    "50kw": (30.0, 70.0),   # 30-70 kW (charge rapide)
    "150kw": (70.0, 200.0), # 70-200 kW (charge ultra-rapide)
}


class ChargeLearning:
    """Système d'apprentissage des courbes de recharge."""
    
    def __init__(self, hass: HomeAssistant, entry_id: str) -> None:
        """Initialise le système d'apprentissage."""
        self.hass = hass
        self.entry_id = entry_id
        # Stocker dans le répertoire de configuration Home Assistant
        storage_dir = hass.config.path("bmw_ix3_learning")
        os.makedirs(storage_dir, exist_ok=True)
        self.storage_path = os.path.join(storage_dir, f"charge_history_{entry_id}.json")
        
        self.history: Dict[str, List[Dict[str, Any]]] = {}
        self.current_session: Optional[Dict[str, Any]] = None
        self.last_soc: Optional[float] = None
        self.last_time_remaining: Optional[float] = None
        
        # Charger l'historique existant
        self._load_history()
    
    def _load_history(self) -> None:
        """Charge l'historique depuis le fichier."""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
                _LOGGER.info("Historique de charge chargé: %s sessions", 
                           sum(len(sessions) for sessions in self.history.values()))
            else:
                self.history = {}
                _LOGGER.info("Aucun historique existant, création d'un nouveau")
        except Exception as err:
            _LOGGER.error("Erreur lors du chargement de l'historique: %s", err)
            self.history = {}
    
    def _save_history(self) -> None:
        """Sauvegarde l'historique dans le fichier."""
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
            _LOGGER.debug("Historique sauvegardé")
        except Exception as err:
            _LOGGER.error("Erreur lors de la sauvegarde de l'historique: %s", err)
    
    def _get_charger_category(self, power_kw: float) -> str:
        """Détermine la catégorie de chargeur selon la puissance."""
        for category, (min_power, max_power) in CHARGER_CATEGORIES.items():
            if min_power <= power_kw < max_power:
                return category
        # Par défaut, utiliser la catégorie la plus proche
        if power_kw < 9.0:
            return "7kw"
        elif power_kw < 15.0:
            return "11kw"
        elif power_kw < 30.0:
            return "22kw"
        elif power_kw < 70.0:
            return "50kw"
        else:
            return "150kw"
    
    def record_charging_data(
        self,
        soc: float,
        time_remaining: Optional[float],
        power_kw: float,
        target_soc: float,
        charging_status: str,
    ) -> None:
        """Enregistre les données de recharge pour l'apprentissage."""
        if charging_status != "CHARGING":
            # Si on n'est plus en charge, finaliser la session précédente
            if self.current_session:
                self._finalize_session()
            return
        
        charger_category = self._get_charger_category(power_kw)
        session_key = f"{charger_category}_{int(target_soc)}"
        
        # Démarrer une nouvelle session si nécessaire
        if not self.current_session or self.current_session.get("session_key") != session_key:
            if self.current_session:
                self._finalize_session()
            
            self.current_session = {
                "session_key": session_key,
                "charger_category": charger_category,
                "target_soc": target_soc,
                "power_kw": power_kw,
                "start_time": datetime.now().isoformat(),
                "start_soc": soc,
                "data_points": [],
            }
            _LOGGER.info("Nouvelle session d'apprentissage: %s (cible: %s%%, puissance: %s kW)",
                        session_key, target_soc, power_kw)
        
        # Enregistrer un point de données
        current_time = datetime.now()
        data_point = {
            "timestamp": current_time.isoformat(),
            "soc": soc,
            "time_remaining": time_remaining,
            "power_kw": power_kw,
        }
        
        self.current_session["data_points"].append(data_point)
        
        # Sauvegarder toutes les 10 minutes ou si le SOC a changé significativement
        if (self.last_soc is None or abs(soc - self.last_soc) >= 5.0 or
            (self.last_time_remaining and time_remaining and 
             abs(time_remaining - self.last_time_remaining) >= 10.0)):
            self._save_history()
            self.last_soc = soc
            self.last_time_remaining = time_remaining
    
    def _finalize_session(self) -> None:
        """Finalise la session en cours et l'ajoute à l'historique."""
        if not self.current_session:
            return
        
        session = self.current_session
        session["end_time"] = datetime.now().isoformat()
        
        # Calculer les statistiques de la session
        if session["data_points"]:
            start_soc = session["data_points"][0]["soc"]
            end_soc = session["data_points"][-1]["soc"]
            session["end_soc"] = end_soc
            session["soc_gained"] = end_soc - start_soc
            
            # Calculer le temps réel écoulé
            start_time = datetime.fromisoformat(session["start_time"])
            end_time = datetime.fromisoformat(session["end_time"])
            session["actual_duration_minutes"] = (end_time - start_time).total_seconds() / 60.0
        
        # Ajouter à l'historique
        session_key = session["session_key"]
        if session_key not in self.history:
            self.history[session_key] = []
        
        self.history[session_key].append(session)
        
        # Garder seulement les 50 dernières sessions par catégorie
        if len(self.history[session_key]) > 50:
            self.history[session_key] = self.history[session_key][-50:]
        
        _LOGGER.info("Session finalisée: %s (SOC: %s%% → %s%%, Durée: %s min)",
                    session_key, session.get("start_soc"), session.get("end_soc"),
                    session.get("actual_duration_minutes", 0))
        
        self._save_history()
        self.current_session = None
        self.last_soc = None
        self.last_time_remaining = None
    
    def predict_charge_time(
        self,
        current_soc: float,
        target_soc: float,
        power_kw: float,
    ) -> Optional[float]:
        """Prédit le temps de charge basé sur l'historique d'apprentissage."""
        charger_category = self._get_charger_category(power_kw)
        session_key = f"{charger_category}_{int(target_soc)}"
        
        # Si pas assez de données, retourner None (utiliser le calcul théorique)
        if session_key not in self.history or len(self.history[session_key]) < 2:
            _LOGGER.debug("Pas assez de données historiques pour %s (besoin: 2+, disponible: %s)",
                        session_key, len(self.history.get(session_key, [])))
            return None
        
        sessions = self.history[session_key]
        
        # Extraire les courbes d'apprentissage
        learning_curves = []
        for session in sessions:
            if not session.get("data_points"):
                continue
            
            # Construire une courbe SOC → temps restant
            curve = {}
            for point in session["data_points"]:
                soc = round(point["soc"], 1)
                time_remaining = point.get("time_remaining")
                if time_remaining is not None:
                    if soc not in curve:
                        curve[soc] = []
                    curve[soc].append(time_remaining)
            
            if curve:
                learning_curves.append(curve)
        
        if not learning_curves:
            return None
        
        # Prédire le temps pour le SOC actuel
        # Utiliser la moyenne des temps restants pour des SOC similaires
        predicted_times = []
        
        for curve in learning_curves:
            # Trouver les points les plus proches du SOC actuel
            closest_socs = sorted(
                curve.keys(),
                key=lambda x: abs(x - current_soc)
            )[:3]  # Prendre les 3 plus proches
            
            if not closest_socs:
                continue
            
            # Moyenne pondérée par la distance
            total_weight = 0.0
            weighted_time = 0.0
            
            for soc in closest_socs:
                times = curve[soc]
                avg_time = sum(times) / len(times)
                distance = abs(soc - current_soc)
                weight = 1.0 / (distance + 0.1)  # Éviter division par zéro
                weighted_time += avg_time * weight
                total_weight += weight
            
            if total_weight > 0:
                predicted_times.append(weighted_time / total_weight)
        
        if not predicted_times:
            return None
        
        # Moyenne des prédictions de toutes les courbes
        predicted_time = sum(predicted_times) / len(predicted_times)
        
        _LOGGER.debug("Prédiction basée sur l'apprentissage: %s min (SOC: %s%%, Cible: %s%%, Puissance: %s kW)",
                     predicted_time, current_soc, target_soc, power_kw)
        
        return predicted_time
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques d'apprentissage."""
        stats = {
            "total_sessions": sum(len(sessions) for sessions in self.history.values()),
            "categories": {},
        }
        
        for session_key, sessions in self.history.items():
            if sessions:
                stats["categories"][session_key] = {
                    "count": len(sessions),
                    "latest": sessions[-1].get("end_time", "N/A"),
                }
        
        return stats
