"""
Script Python pour générer les statistiques quotidiennes de charge
pour BMW iX3
"""
import datetime
import logging

logger = logging.getLogger(__name__)

def calculate_daily_statistics(date_str):
    """
    Calcule les statistiques quotidiennes de charge
    
    Args:
        date_str: Date au format "YYYY-MM-DD"
    
    Returns:
        dict: Statistiques quotidiennes
    """
    try:
        # Récupération des données depuis Home Assistant
        # (Ces données devraient être stockées dans des entités de type history)
        
        # Simulation des données - à remplacer par de vraies données
        stats = {
            "date": date_str,
            "total_energy_charged": 0.0,  # kWh
            "charging_sessions": 0,
            "average_charging_power": 0.0,  # kW
            "total_charging_time": 0.0,  # heures
            "cost_estimation": 0.0,  # euros
            "co2_savings": 0.0,  # kg CO2
            "efficiency_rating": "N/A"
        }
        
        # Calcul des statistiques (simulation)
        # Dans une vraie implémentation, vous récupéreriez ces données
        # depuis l'historique des entités Home Assistant
        
        # Estimation des coûts (tarif moyen 0.15€/kWh)
        stats["cost_estimation"] = stats["total_energy_charged"] * 0.15
        
        # Estimation des économies CO2 (0.4 kg CO2/kWh économisé)
        stats["co2_savings"] = stats["total_energy_charged"] * 0.4
        
        # Calcul de l'efficacité
        if stats["total_charging_time"] > 0:
            stats["average_charging_power"] = stats["total_energy_charged"] / stats["total_charging_time"]
            
            # Évaluation de l'efficacité
            if stats["average_charging_power"] >= 10:
                stats["efficiency_rating"] = "Excellent"
            elif stats["average_charging_power"] >= 7:
                stats["efficiency_rating"] = "Bon"
            elif stats["average_charging_power"] >= 5:
                stats["efficiency_rating"] = "Moyen"
            else:
                stats["efficiency_rating"] = "Faible"
        
        return stats
        
    except Exception as e:
        logger.error(f"Erreur dans le calcul des statistiques: {e}")
        return None

def generate_daily_report(stats):
    """
    Génère un rapport quotidien formaté
    
    Args:
        stats: Dictionnaire des statistiques
    
    Returns:
        str: Rapport formaté
    """
    if not stats:
        return "Aucune donnée disponible pour cette date"
    
    report = f"""
📊 RAPPORT QUOTIDIEN BMW iX3 - {stats['date']}

🔋 ÉNERGIE CHARGÉE
• Total: {stats['total_energy_charged']:.1f} kWh
• Sessions: {stats['charging_sessions']}
• Temps total: {stats['total_charging_time']:.1f} heures

⚡ PERFORMANCE
• Puissance moyenne: {stats['average_charging_power']:.1f} kW
• Efficacité: {stats['efficiency_rating']}

💰 ÉCONOMIES
• Coût estimé: {stats['cost_estimation']:.2f} €
• CO2 économisé: {stats['co2_savings']:.1f} kg

📈 RECOMMANDATIONS
{get_daily_recommendations(stats)}
"""
    
    return report.strip()

def get_daily_recommendations(stats):
    """
    Génère des recommandations basées sur les statistiques
    
    Args:
        stats: Dictionnaire des statistiques
    
    Returns:
        str: Recommandations
    """
    recommendations = []
    
    if stats["charging_sessions"] > 3:
        recommendations.append("• Considérez regrouper les sessions de charge")
    
    if stats["average_charging_power"] < 5:
        recommendations.append("• Vérifiez la puissance de votre borne")
    
    if stats["total_charging_time"] > 8:
        recommendations.append("• Optimisez les heures de charge")
    
    if stats["efficiency_rating"] == "Faible":
        recommendations.append("• Améliorez l'efficacité de charge")
    
    if not recommendations:
        recommendations.append("• Excellente utilisation de votre véhicule électrique!")
    
    return "\n".join(recommendations)

def save_statistics_to_file(stats, filename):
    """
    Sauvegarde les statistiques dans un fichier
    
    Args:
        stats: Dictionnaire des statistiques
        filename: Nom du fichier
    """
    try:
        with open(filename, 'a') as f:
            f.write(f"{stats['date']},{stats['total_energy_charged']},{stats['charging_sessions']},{stats['average_charging_power']},{stats['total_charging_time']},{stats['cost_estimation']},{stats['co2_savings']}\n")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde: {e}")

# Fonction principale pour Home Assistant
def main():
    """Fonction principale appelée par Home Assistant"""
    # Récupération de la date
    date_str = data.get("date", datetime.date.today().strftime("%Y-%m-%d"))
    
    # Calcul des statistiques
    stats = calculate_daily_statistics(date_str)
    
    if stats:
        # Mise à jour des entités Home Assistant
        hass.states.set("sensor.bmw_ix3_daily_energy", stats["total_energy_charged"])
        hass.states.set("sensor.bmw_ix3_daily_sessions", stats["charging_sessions"])
        hass.states.set("sensor.bmw_ix3_daily_avg_power", stats["average_charging_power"])
        hass.states.set("sensor.bmw_ix3_daily_cost", stats["cost_estimation"])
        hass.states.set("sensor.bmw_ix3_daily_co2_savings", stats["co2_savings"])
        hass.states.set("sensor.bmw_ix3_daily_efficiency", stats["efficiency_rating"])
        
        # Génération du rapport
        report = generate_daily_report(stats)
        hass.states.set("sensor.bmw_ix3_daily_report", report)
        
        # Sauvegarde des statistiques
        save_statistics_to_file(stats, "/config/bmw_ix3_statistics.csv")
        
        # Notification du rapport quotidien
        hass.services.call(
            "notify", "mobile_app_iphone",
            {
                "title": f"BMW iX3 - Rapport {date_str}",
                "message": f"Énergie: {stats['total_energy_charged']:.1f} kWh | Coût: {stats['cost_estimation']:.2f}€ | CO2: {stats['co2_savings']:.1f}kg"
            }
        )
        
        logger.info(f"Statistiques quotidiennes calculées: {stats}")
    else:
        logger.error("Impossible de calculer les statistiques quotidiennes")

if __name__ == "__main__":
    main()
