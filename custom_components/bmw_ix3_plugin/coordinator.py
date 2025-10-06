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
            # Simulation des données BMW - à remplacer par l'API réelle
            # Ici, vous devriez utiliser l'intégration BMW Connected Drive existante
            # ou implémenter votre propre client API
            
            bmw_data = {
                "battery_level": 65.0,  # Pourcentage de charge
                "charging_status": "CHARGING",  # CHARGING, NOT_CHARGING, COMPLETE
                "charging_power": 7.4,  # kW
                "range_electric": 280,  # km
                "last_update": datetime.now().isoformat(),
            }
            
            _LOGGER.debug("Données BMW mises à jour: %s", bmw_data)
            return bmw_data
            
        except Exception as err:
            _LOGGER.error("Erreur lors de la récupération des données BMW: %s", err)
            return {}

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
