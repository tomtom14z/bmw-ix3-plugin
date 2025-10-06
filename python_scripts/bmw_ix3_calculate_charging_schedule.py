"""
Script Python pour calculer l'horaire de charge optimal
pour BMW iX3 avec prise en compte des heures creuses
"""
import datetime
import logging

# Configuration des heures creuses (à adapter selon votre tarif)
OFF_PEAK_START = datetime.time(22, 0)  # 22h00
OFF_PEAK_END = datetime.time(6, 0)     # 6h00

# Capacité batterie BMW iX3
BATTERY_CAPACITY = 80.0  # kWh
CHARGE_EFFICIENCY = 0.9  # 90% d'efficacité

logger = logging.getLogger(__name__)

def calculate_charging_schedule(departure_time_str, target_soc, current_soc, charging_power):
    """
    Calcule l'horaire de charge optimal
    
    Args:
        departure_time_str: Heure de départ au format "HH:MM"
        target_soc: Pourcentage de charge cible
        current_soc: Pourcentage de charge actuel
        charging_power: Puissance de charge en kW
    
    Returns:
        dict: Informations sur la planification
    """
    try:
        # Conversion de l'heure de départ
        departure_time = datetime.datetime.strptime(departure_time_str, "%H:%M").time()
        
        # Calcul de l'énergie nécessaire
        energy_needed = (target_soc - current_soc) / 100.0 * BATTERY_CAPACITY
        energy_needed = energy_needed / CHARGE_EFFICIENCY  # Prise en compte des pertes
        
        # Calcul du temps de charge
        charge_time_hours = energy_needed / charging_power
        
        # Date de départ (aujourd'hui ou demain)
        today = datetime.date.today()
        departure_datetime = datetime.datetime.combine(today, departure_time)
        
        # Si l'heure de départ est dans le passé, prendre demain
        if departure_datetime <= datetime.datetime.now():
            departure_datetime += datetime.timedelta(days=1)
        
        # Calcul de l'heure de début
        start_datetime = departure_datetime - datetime.timedelta(hours=charge_time_hours)
        
        # Vérification des heures creuses
        start_time = start_datetime.time()
        end_time = departure_time
        
        # Ajustement pour les heures creuses
        if not is_off_peak_time(start_time):
            # Déplacer le début vers les heures creuses
            if start_time < OFF_PEAK_START:
                # Commencer aux heures creuses
                start_datetime = datetime.datetime.combine(
                    start_datetime.date(), OFF_PEAK_START
                )
            else:
                # Commencer le lendemain aux heures creuses
                start_datetime = datetime.datetime.combine(
                    start_datetime.date() + datetime.timedelta(days=1), OFF_PEAK_START
                )
        
        # Vérification que la charge se termine avant l'heure de départ
        if start_datetime + datetime.timedelta(hours=charge_time_hours) > departure_datetime:
            # Ajuster la puissance ou l'heure de début
            charge_time_hours = (departure_datetime - start_datetime).total_seconds() / 3600
            required_power = energy_needed / charge_time_hours
            
            logger.warning(f"Puissance requise: {required_power:.1f} kW (limite: {charging_power} kW)")
        
        # Calcul des économies (heures creuses)
        off_peak_hours = calculate_off_peak_hours(start_datetime, departure_datetime)
        savings_percentage = (off_peak_hours / charge_time_hours) * 100 if charge_time_hours > 0 else 0
        
        return {
            "start_time": start_datetime.strftime("%H:%M"),
            "end_time": departure_time.strftime("%H:%M"),
            "charge_duration_hours": round(charge_time_hours, 2),
            "energy_needed_kwh": round(energy_needed, 2),
            "off_peak_hours": round(off_peak_hours, 2),
            "savings_percentage": round(savings_percentage, 1),
            "is_optimal": savings_percentage >= 80,
            "recommendations": generate_recommendations(charge_time_hours, savings_percentage)
        }
        
    except Exception as e:
        logger.error(f"Erreur dans le calcul de planification: {e}")
        return None

def is_off_peak_time(time_to_check):
    """Vérifie si une heure est en période creuse"""
    if OFF_PEAK_START <= OFF_PEAK_END:
        # Même jour (ex: 22h00 à 6h00)
        return OFF_PEAK_START <= time_to_check <= OFF_PEAK_END
    else:
        # Sur deux jours (ex: 22h00 à 6h00)
        return time_to_check >= OFF_PEAK_START or time_to_check <= OFF_PEAK_END

def calculate_off_peak_hours(start_datetime, end_datetime):
    """Calcule le nombre d'heures en période creuse"""
    off_peak_hours = 0
    current = start_datetime
    
    while current < end_datetime:
        next_hour = current + datetime.timedelta(hours=1)
        if next_hour > end_datetime:
            next_hour = end_datetime
        
        # Vérifier si cette heure est en période creuse
        if is_off_peak_time(current.time()):
            off_peak_hours += (next_hour - current).total_seconds() / 3600
        
        current = next_hour
    
    return off_peak_hours

def generate_recommendations(charge_time_hours, savings_percentage):
    """Génère des recommandations d'optimisation"""
    recommendations = []
    
    if savings_percentage < 50:
        recommendations.append("Considérez programmer la charge pendant les heures creuses")
    
    if charge_time_hours > 8:
        recommendations.append("Charge longue détectée - vérifiez la puissance de charge")
    
    if savings_percentage >= 80:
        recommendations.append("Planification optimale - maximum d'économies réalisées")
    
    return recommendations

# Fonction principale pour Home Assistant
def main():
    """Fonction principale appelée par Home Assistant"""
    # Récupération des données depuis Home Assistant
    departure_time = data.get("departure_time", "08:00")
    target_soc = float(data.get("target_soc", 80))
    current_soc = float(data.get("current_soc", 65))
    charging_power = float(data.get("charging_power", 7.4))
    
    # Calcul de la planification
    schedule = calculate_charging_schedule(
        departure_time, target_soc, current_soc, charging_power
    )
    
    if schedule:
        # Mise à jour des entités Home Assistant
        hass.states.set("input_datetime.bmw_ix3_charging_start_time", schedule["start_time"])
        hass.states.set("sensor.bmw_ix3_charge_duration", schedule["charge_duration_hours"])
        hass.states.set("sensor.bmw_ix3_energy_needed", schedule["energy_needed_kwh"])
        hass.states.set("sensor.bmw_ix3_off_peak_hours", schedule["off_peak_hours"])
        hass.states.set("sensor.bmw_ix3_savings_percentage", schedule["savings_percentage"])
        
        # Notification si la planification n'est pas optimale
        if not schedule["is_optimal"]:
            hass.services.call(
                "notify", "mobile_app_iphone",
                {
                    "title": "BMW iX3 - Planification",
                    "message": f"Charge planifiée à {schedule['start_time']} - Économies: {schedule['savings_percentage']}%"
                }
            )
        
        logger.info(f"Planification calculée: {schedule}")
    else:
        logger.error("Impossible de calculer la planification")

if __name__ == "__main__":
    main()

