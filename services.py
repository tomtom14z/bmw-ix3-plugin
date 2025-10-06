"""Services pour le plugin BMW iX3."""
import logging
from datetime import datetime, timedelta
from typing import Any, Dict

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import (
    DOMAIN,
    NOTIFICATION_CHARGING_START,
    NOTIFICATION_CHARGING_80,
    NOTIFICATION_CHARGING_100,
    NOTIFICATION_CHARGING_STOP,
)

_LOGGER = logging.getLogger(__name__)

# Schémas de validation pour les services
SERVICE_SEND_CHARGING_NOTIFICATION = vol.Schema({
    vol.Required("notification_type"): vol.In([
        NOTIFICATION_CHARGING_START,
        NOTIFICATION_CHARGING_80,
        NOTIFICATION_CHARGING_100,
        NOTIFICATION_CHARGING_STOP,
    ]),
    vol.Optional("battery_level"): vol.All(vol.Coerce(float), vol.Range(min=0, max=100)),
    vol.Optional("charging_power"): vol.All(vol.Coerce(float), vol.Range(min=0, max=22)),
    vol.Optional("estimated_completion"): cv.datetime,
})

SERVICE_UPDATE_IOS_WIDGET = vol.Schema({
    vol.Optional("force_update"): bool,
})

SERVICE_SCHEDULE_CHARGING = vol.Schema({
    vol.Required("departure_time"): cv.time,
    vol.Required("target_soc"): vol.All(vol.Coerce(float), vol.Range(min=50, max=100)),
    vol.Optional("charging_power"): vol.All(vol.Coerce(float), vol.Range(min=3.7, max=22)),
})


async def async_setup_services(hass: HomeAssistant) -> None:
    """Configuration des services."""
    
    async def send_charging_notification(call: ServiceCall) -> None:
        """Envoie une notification de charge."""
        notification_type = call.data["notification_type"]
        battery_level = call.data.get("battery_level")
        charging_power = call.data.get("charging_power")
        estimated_completion = call.data.get("estimated_completion")
        
        # Création du message de notification
        message = _create_notification_message(
            notification_type, battery_level, charging_power, estimated_completion
        )
        
        # Envoi de la notification via le service de notification Home Assistant
        await hass.services.async_call(
            "notify",
            "mobile_app_iphone",  # À adapter selon votre configuration
            {
                "title": "BMW iX3 - État de charge",
                "message": message,
                "data": {
                    "notification_type": notification_type,
                    "battery_level": battery_level,
                    "charging_power": charging_power,
                    "estimated_completion": estimated_completion.isoformat() if estimated_completion else None,
                }
            }
        )
        
        _LOGGER.info("Notification de charge envoyée: %s", message)

    async def update_ios_widget(call: ServiceCall) -> None:
        """Met à jour le widget iOS."""
        force_update = call.data.get("force_update", False)
        
        # Récupération des données actuelles
        for entry_id in hass.data[DOMAIN]:
            coordinator = hass.data[DOMAIN][entry_id].get("coordinator")
            if coordinator:
                await coordinator.async_request_refresh()
        
        # Envoi d'une notification pour forcer la mise à jour du widget
        if force_update:
            await hass.services.async_call(
                "notify",
                "mobile_app_iphone",
                {
                    "title": "BMW iX3 - Mise à jour widget",
                    "message": "Données mises à jour",
                    "data": {"action": "update_widget"}
                }
            )
        
        _LOGGER.info("Widget iOS mis à jour")

    async def schedule_charging(call: ServiceCall) -> None:
        """Planifie une session de charge."""
        departure_time = call.data["departure_time"]
        target_soc = call.data["target_soc"]
        charging_power = call.data.get("charging_power", 7.4)
        
        # Calcul de l'heure de début de charge
        start_time = await _calculate_charging_start_time(
            hass, departure_time, target_soc, charging_power
        )
        
        if start_time:
            # Création d'une automatisation temporaire pour démarrer la charge
            await _create_charging_automation(hass, start_time, target_soc)
            
            _LOGGER.info(
                "Charge planifiée: début à %s pour atteindre %d%% à %s",
                start_time.strftime("%H:%M"),
                target_soc,
                departure_time.strftime("%H:%M")
            )
        else:
            _LOGGER.error("Impossible de planifier la charge")

    # Enregistrement des services
    hass.services.async_register(
        DOMAIN,
        "send_charging_notification",
        send_charging_notification,
        schema=SERVICE_SEND_CHARGING_NOTIFICATION,
    )
    
    hass.services.async_register(
        DOMAIN,
        "update_ios_widget",
        update_ios_widget,
        schema=SERVICE_UPDATE_IOS_WIDGET,
    )
    
    hass.services.async_register(
        DOMAIN,
        "schedule_charging",
        schedule_charging,
        schema=SERVICE_SCHEDULE_CHARGING,
    )


def _create_notification_message(
    notification_type: str,
    battery_level: float = None,
    charging_power: float = None,
    estimated_completion: datetime = None,
) -> str:
    """Crée le message de notification."""
    messages = {
        NOTIFICATION_CHARGING_START: "🚗 Charge démarrée",
        NOTIFICATION_CHARGING_80: "🔋 Charge à 80% atteinte",
        NOTIFICATION_CHARGING_100: "✅ Charge terminée (100%)",
        NOTIFICATION_CHARGING_STOP: "⏹️ Charge arrêtée",
    }
    
    message = messages.get(notification_type, "État de charge mis à jour")
    
    if battery_level is not None:
        message += f"\nBatterie: {battery_level:.1f}%"
    
    if charging_power is not None:
        message += f"\nPuissance: {charging_power:.1f} kW"
    
    if estimated_completion is not None:
        message += f"\nFin prévue: {estimated_completion.strftime('%H:%M')}"
    
    return message


async def _calculate_charging_start_time(
    hass: HomeAssistant,
    departure_time,
    target_soc: float,
    charging_power: float,
) -> datetime:
    """Calcule l'heure de début de charge optimale."""
    # Récupération des données actuelles
    current_soc = 65.0  # À récupérer depuis le coordinateur
    battery_capacity = 80.0  # kWh
    
    # Calcul de l'énergie nécessaire
    energy_needed = (target_soc - current_soc) / 100.0 * battery_capacity
    charge_time_hours = energy_needed / charging_power
    
    # Calcul de l'heure de début
    departure_datetime = datetime.combine(datetime.now().date(), departure_time)
    if departure_datetime <= datetime.now():
        departure_datetime += timedelta(days=1)
    
    start_datetime = departure_datetime - timedelta(hours=charge_time_hours)
    
    return start_datetime


async def _create_charging_automation(
    hass: HomeAssistant,
    start_time: datetime,
    target_soc: float,
) -> None:
    """Crée une automatisation temporaire pour la charge."""
    # Cette fonction devrait créer une automatisation temporaire
    # qui démarre la charge à l'heure calculée
    _LOGGER.info("Création d'une automatisation de charge temporaire")
