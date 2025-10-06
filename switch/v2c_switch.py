"""Commutateur de contrôle V2C."""
import logging
from typing import Any, Dict, Optional

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class V2CChargingSwitch(CoordinatorEntity, SwitchEntity):
    """Commutateur de contrôle de la charge V2C."""

    def __init__(self, coordinator) -> None:
        """Initialise le commutateur."""
        super().__init__(coordinator)
        self._attr_unique_id = "v2c_charging_switch"
        self._attr_name = "V2C Charging"

    @property
    def is_on(self) -> bool:
        """État du commutateur."""
        if not self.coordinator.data:
            return False
        
        v2c_data = self.coordinator.data.get("v2c", {})
        return v2c_data.get("charging_enabled", False)

    @property
    def icon(self) -> str:
        """Icône du commutateur."""
        return "mdi:ev-station" if self.is_on else "mdi:ev-station-outline"

    @property
    def device_info(self) -> DeviceInfo:
        """Informations sur l'appareil."""
        return DeviceInfo(
            identifiers={(DOMAIN, "v2c_trydan")},
            name="V2C Trydan",
            manufacturer="V2C",
            model="Trydan",
            sw_version="1.0",
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Active la charge."""
        _LOGGER.info("Activation de la charge V2C")
        success = await self.coordinator.control_v2c_charging(True)
        if success:
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Échec de l'activation de la charge V2C")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Désactive la charge."""
        _LOGGER.info("Désactivation de la charge V2C")
        success = await self.coordinator.control_v2c_charging(False)
        if success:
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Échec de la désactivation de la charge V2C")

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Attributs supplémentaires."""
        if not self.coordinator.data:
            return {}
        
        v2c_data = self.coordinator.data.get("v2c", {})
        return {
            "status": v2c_data.get("status"),
            "charging_power": v2c_data.get("charging_power"),
            "charging_current": v2c_data.get("charging_current"),
        }
