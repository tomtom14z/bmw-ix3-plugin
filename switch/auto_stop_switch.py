"""Commutateur d'arrêt automatique à 80%."""
import logging
from typing import Any, Dict, Optional

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class AutoStopSwitch(CoordinatorEntity, SwitchEntity):
    """Commutateur d'arrêt automatique à 80%."""

    def __init__(self, coordinator) -> None:
        """Initialise le commutateur."""
        super().__init__(coordinator)
        self._attr_unique_id = "bmw_ix3_auto_stop_80"
        self._attr_name = "BMW iX3 Arrêt auto 80%"
        self._auto_stop_enabled = True  # Par défaut activé

    @property
    def is_on(self) -> bool:
        """État du commutateur."""
        return self._auto_stop_enabled

    @property
    def icon(self) -> str:
        """Icône du commutateur."""
        return "mdi:battery-charging-80" if self.is_on else "mdi:battery-charging-80-outline"

    @property
    def device_info(self) -> DeviceInfo:
        """Informations sur l'appareil."""
        return DeviceInfo(
            identifiers={(DOMAIN, "bmw_ix3")},
            name="BMW iX3",
            manufacturer="BMW",
            model="iX3",
            sw_version="1.0",
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Active l'arrêt automatique à 80%."""
        _LOGGER.info("Activation de l'arrêt automatique à 80%")
        self._auto_stop_enabled = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Désactive l'arrêt automatique à 80%."""
        _LOGGER.info("Désactivation de l'arrêt automatique à 80%")
        self._auto_stop_enabled = False
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Attributs supplémentaires."""
        if not self.coordinator.data:
            return {}
        
        bmw_data = self.coordinator.data.get("bmw", {})
        battery_level = bmw_data.get("battery_level", 0)
        charging_status = bmw_data.get("charging_status")
        
        return {
            "current_battery_level": battery_level,
            "charging_status": charging_status,
            "auto_stop_threshold": 80,
            "will_stop_at_80": self._auto_stop_enabled and charging_status == "CHARGING" and battery_level < 80,
        }
