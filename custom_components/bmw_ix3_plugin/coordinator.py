"""Coordinateur pour le plugin BMW iX3."""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    UPDATE_INTERVAL,
    CHARGING_UPDATE_INTERVAL,
    CONF_BMW_USERNAME,
    CONF_BMW_PASSWORD,
    CONF_V2C_IP,
    CONF_V2C_USERNAME,
    CONF_V2C_PASSWORD,
)

_LOGGER = logging.getLogger(__name__)


class BMWiX3Coordinator(DataUpdateCoordinator):
    """Coordinateur pour les données BMW iX3 et V2C."""

    def __init__(self, hass: HomeAssistant, config: Dict[str, Any]) -> None:
        """Initialise le coordinateur."""
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Intervalle de mise à jour dynamique
        update_interval = timedelta(seconds=UPDATE_INTERVAL)
        
        super().__init__(
            hass,
            _LOGGER,
            name="BMW iX3 Plugin",
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Mise à jour des données."""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            # Mise à jour des données BMW et V2C en parallèle
            bmw_task = self._update_bmw_data()
            v2c_task = self._update_v2c_data()
            
            bmw_data, v2c_data = await asyncio.gather(bmw_task, v2c_task)
            
            # Ajustement de l'intervalle de mise à jour selon l'état de charge
            if bmw_data.get("charging_status") == "CHARGING":
                self.update_interval = timedelta(seconds=CHARGING_UPDATE_INTERVAL)
            else:
                self.update_interval = timedelta(seconds=UPDATE_INTERVAL)
            
            return {
                "bmw": bmw_data,
                "v2c": v2c_data,
                "last_update": datetime.now().isoformat(),
            }
            
        except Exception as err:
            _LOGGER.error("Erreur lors de la mise à jour des données: %s", err)
            raise UpdateFailed(f"Erreur de mise à jour: {err}")

    async def _update_bmw_data(self) -> Dict[str, Any]:
        """Mise à jour des données BMW."""
        try:
            # Récupération des données depuis l'intégration BMW 
            # (Compatible avec BMW Connected Drive, BMW CarData, etc.)
            hass = self.hass
            
            # Recherche de l'entité BMW iX3 dans Home Assistant
            bmw_entities = {
                "battery_level": None,
                "charging_status": None,
                "charging_power": None,
                "range_electric": None,
            }
            
            detected_entities = []
            
            # Parcourir toutes les entités pour trouver celles de BMW
            for entity_id in hass.states.async_entity_ids():
                # Recherche flexible : bmw, ix3, cardata, etc.
                entity_lower = entity_id.lower()
                if not any(keyword in entity_lower for keyword in ["bmw", "ix3", "cardata"]):
                    continue
                
                state = hass.states.get(entity_id)
                if not state or state.state in ("unknown", "unavailable", "None"):
                    continue
                
                detected_entities.append(entity_id)
                
                # Niveau de batterie - recherche étendue
                if any(keyword in entity_lower for keyword in 
                       ["battery", "soc", "state_of_charge", "charge_level", "battery_percent"]):
                    try:
                        value = float(state.state)
                        if 0 <= value <= 100:  # Validation
                            bmw_entities["battery_level"] = value
                            _LOGGER.debug("Batterie trouvée: %s = %s%%", entity_id, value)
                    except (ValueError, TypeError):
                        pass
                
                # État de charge - recherche étendue
                elif any(keyword in entity_lower for keyword in 
                        ["charging_status", "charge_status", "charging_state"]):
                    status = state.state.upper()
                    bmw_entities["charging_status"] = status
                    _LOGGER.debug("État charge trouvé: %s = %s", entity_id, status)
                
                # Puissance de charge
                elif any(keyword in entity_lower for keyword in 
                        ["charging_power", "charge_power", "power_kw"]):
                    try:
                        value = float(state.state)
                        if value >= 0:  # Validation
                            bmw_entities["charging_power"] = value
                            _LOGGER.debug("Puissance trouvée: %s = %s kW", entity_id, value)
                    except (ValueError, TypeError):
                        pass
                
                # Autonomie électrique
                elif any(keyword in entity_lower for keyword in 
                        ["range", "autonomie", "remaining_range", "electric_range"]):
                    try:
                        value = float(state.state)
                        if value >= 0:  # Validation
                            bmw_entities["range_electric"] = value
                            _LOGGER.debug("Autonomie trouvée: %s = %s km", entity_id, value)
                    except (ValueError, TypeError):
                        pass
            
            # Log des entités détectées
            if detected_entities:
                _LOGGER.info("Entités BMW détectées: %s", ", ".join(detected_entities[:5]))
            else:
                _LOGGER.warning("Aucune entité BMW trouvée. Vérifiez l'installation de BMW Connected Drive ou BMW CarData")
            
            # Construction des données BMW
            bmw_data = {
                "battery_level": bmw_entities.get("battery_level") or 0.0,
                "charging_status": bmw_entities.get("charging_status") or "UNKNOWN",
                "charging_power": bmw_entities.get("charging_power") or 0.0,
                "range_electric": bmw_entities.get("range_electric") or 0.0,
                "last_update": datetime.now().isoformat(),
            }
            
            _LOGGER.info("🚗 BMW iX3 - Batterie: %s%%, État: %s, Autonomie: %s km", 
                        bmw_data["battery_level"], bmw_data["charging_status"], bmw_data["range_electric"])
            
            return bmw_data
            
        except Exception as err:
            _LOGGER.error("Erreur lors de la récupération des données BMW: %s", err)
            return {
                "battery_level": 0.0,
                "charging_status": "ERROR",
                "charging_power": 0.0,
                "range_electric": 0.0,
                "last_update": datetime.now().isoformat(),
            }

    async def _update_v2c_data(self) -> Dict[str, Any]:
        """Mise à jour des données V2C."""
        try:
            v2c_ip = self.config.get(CONF_V2C_IP)
            v2c_username = self.config.get(CONF_V2C_USERNAME, "admin")
            v2c_password = self.config.get(CONF_V2C_PASSWORD, "")
            
            if not v2c_ip:
                return {}
            
            # Simulation des données V2C - à remplacer par l'API réelle
            v2c_data = {
                "status": "CHARGING",  # CHARGING, READY, ERROR
                "charging_enabled": True,
                "charging_power": 7.4,  # kW
                "charging_current": 32,  # A
                "last_update": datetime.now().isoformat(),
            }
            
            _LOGGER.debug("Données V2C mises à jour: %s", v2c_data)
            return v2c_data
            
        except Exception as err:
            _LOGGER.error("Erreur lors de la récupération des données V2C: %s", err)
            return {}

    async def async_shutdown(self) -> None:
        """Arrêt du coordinateur."""
        if self.session:
            await self.session.close()

    async def control_v2c_charging(self, enabled: bool) -> bool:
        """Contrôle de la charge V2C."""
        try:
            v2c_ip = self.config.get(CONF_V2C_IP)
            if not v2c_ip:
                return False
            
            # Simulation du contrôle V2C - à remplacer par l'API réelle
            _LOGGER.info("Contrôle V2C: %s", "Activation" if enabled else "Désactivation")
            
            # Forcer une mise à jour après le contrôle
            await self.async_request_refresh()
            
            return True
            
        except Exception as err:
            _LOGGER.error("Erreur lors du contrôle V2C: %s", err)
            return False
