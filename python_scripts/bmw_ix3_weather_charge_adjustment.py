"""
Script Python pour ajuster la charge selon les conditions météorologiques
pour BMW iX3
"""
import logging

logger = logging.getLogger(__name__)

def adjust_charging_for_weather(temperature, condition, current_charging_power):
    """
    Ajuste la puissance de charge selon les conditions météorologiques
    
    Args:
        temperature: Température en °C
        condition: Condition météorologique (sunny, rainy, snowy, etc.)
        current_charging_power: Puissance de charge actuelle en kW
    
    Returns:
        dict: Ajustements recommandés
    """
    try:
        adjustments = {
            "power_adjustment": 1.0,  # Facteur d'ajustement (1.0 = pas de changement)
            "recommendations": [],
            "safety_notes": []
        }
        
        # Ajustements selon la température
        if temperature < -10:
            # Très froid - réduction de puissance pour protéger la batterie
            adjustments["power_adjustment"] = 0.7
            adjustments["recommendations"].append("Température très basse - Réduction de puissance recommandée")
            adjustments["safety_notes"].append("Charge lente recommandée par temps très froid")
            
        elif temperature < 0:
            # Froid - légère réduction
            adjustments["power_adjustment"] = 0.8
            adjustments["recommendations"].append("Température froide - Charge modérée")
            
        elif temperature > 35:
            # Très chaud - réduction pour éviter la surchauffe
            adjustments["power_adjustment"] = 0.6
            adjustments["recommendations"].append("Température élevée - Réduction importante de puissance")
            adjustments["safety_notes"].append("Surveillance de la température de batterie recommandée")
            
        elif temperature > 25:
            # Chaud - légère réduction
            adjustments["power_adjustment"] = 0.9
            adjustments["recommendations"].append("Température chaude - Charge légèrement réduite")
        
        # Ajustements selon les conditions météorologiques
        if condition in ["rainy", "stormy", "thunderstorm"]:
            adjustments["recommendations"].append("Conditions pluvieuses - Vérifiez l'étanchéité de la borne")
            adjustments["safety_notes"].append("Évitez la charge en cas d'orage")
            
        elif condition in ["snowy", "sleet"]:
            adjustments["power_adjustment"] *= 0.8
            adjustments["recommendations"].append("Conditions neigeuses - Charge réduite")
            adjustments["safety_notes"].append("Nettoyez la borne avant la charge")
            
        elif condition == "sunny" and temperature > 20:
            adjustments["recommendations"].append("Conditions optimales - Charge normale")
        
        # Calcul de la nouvelle puissance
        new_power = current_charging_power * adjustments["power_adjustment"]
        adjustments["new_charging_power"] = round(new_power, 1)
        
        # Limites de sécurité
        if new_power < 3.7:
            adjustments["new_charging_power"] = 3.7
            adjustments["safety_notes"].append("Puissance minimale appliquée (3.7 kW)")
        elif new_power > 22:
            adjustments["new_charging_power"] = 22
            adjustments["safety_notes"].append("Puissance maximale appliquée (22 kW)")
        
        return adjustments
        
    except Exception as e:
        logger.error(f"Erreur dans l'ajustement météorologique: {e}")
        return {
            "power_adjustment": 1.0,
            "new_charging_power": current_charging_power,
            "recommendations": ["Erreur de calcul - Charge normale"],
            "safety_notes": []
        }

def get_weather_charging_recommendations(temperature, condition):
    """
    Génère des recommandations générales selon la météo
    
    Args:
        temperature: Température en °C
        condition: Condition météorologique
    
    Returns:
        list: Liste de recommandations
    """
    recommendations = []
    
    # Recommandations générales
    if temperature < 0:
        recommendations.append("Préchauffez l'habitacle pendant la charge")
        recommendations.append("Utilisez le mode éco pour préserver l'autonomie")
        
    if temperature > 30:
        recommendations.append("Activez la climatisation pendant la charge")
        recommendations.append("Garez à l'ombre si possible")
        
    if condition in ["rainy", "stormy"]:
        recommendations.append("Vérifiez l'étanchéité de la connexion")
        recommendations.append("Évitez la charge en extérieur par mauvais temps")
        
    if condition == "snowy":
        recommendations.append("Nettoyez la borne avant la charge")
        recommendations.append("Prévoyez plus de temps pour la charge")
        
    return recommendations

# Fonction principale pour Home Assistant
def main():
    """Fonction principale appelée par Home Assistant"""
    # Récupération des données depuis Home Assistant
    temperature = float(data.get("temperature", 20))
    condition = data.get("condition", "sunny")
    current_power = float(data.get("charging_power", 7.4))
    
    # Calcul des ajustements
    adjustments = adjust_charging_for_weather(temperature, condition, current_power)
    
    # Mise à jour des entités Home Assistant
    hass.states.set("sensor.bmw_ix3_weather_adjustment_factor", adjustments["power_adjustment"])
    hass.states.set("sensor.bmw_ix3_recommended_power", adjustments["new_charging_power"])
    
    # Notification si des ajustements sont nécessaires
    if adjustments["power_adjustment"] != 1.0:
        message = f"🌡️ Ajustement météo: {adjustments['new_charging_power']} kW"
        if adjustments["recommendations"]:
            message += f"\n{adjustments['recommendations'][0]}"
            
        hass.services.call(
            "notify", "mobile_app_iphone",
            {
                "title": "BMW iX3 - Ajustement météo",
                "message": message
            }
        )
    
    # Mise à jour des recommandations
    weather_recommendations = get_weather_charging_recommendations(temperature, condition)
    hass.states.set("sensor.bmw_ix3_weather_recommendations", "; ".join(weather_recommendations))
    
    logger.info(f"Ajustements météo appliqués: {adjustments}")

if __name__ == "__main__":
    main()

