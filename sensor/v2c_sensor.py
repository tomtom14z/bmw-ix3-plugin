"""Capteurs V2C Trydan."""
import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class V2CSensor(CoordinatorEntity, SensorEntity):
    """Capteur V2C Trydan."""

    def __init__(
        self,
        coordinator,
        key: str,
        name: str,
        unit: Optional[str] = None,
        icon: Optional[str] = None,
    ) -> None:
        """Initialise le capteur."""
        super().__init__(coordinator)
        self._key = key
        self._name = name
        self._unit = unit
        self._icon = icon
        self._attr_unique_id = f"v2c_{key}"

    @property
    def name(self) -> str:
        """Nom du capteur."""
        return f"V2C {self._name}"

    @property
    def native_value(self) -> Any:
        """Valeur du capteur."""
        if not self.coordinator.data:
            return None
        
        v2c_data = self.coordinator.data.get("v2c", {})
        return v2c_data.get(self._key)

    @property
    def native_unit_of_measurement(self) -> Optional[str]:
        """Unité de mesure."""
        return self._unit

    @property
    def icon(self) -> Optional[str]:
        """Icône du capteur."""
        return self._icon

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

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Attributs supplémentaires."""
        if not self.coordinator.data:
            return {}
        
        v2c_data = self.coordinator.data.get("v2c", {})
        return {
            "status": v2c_data.get("status"),
            "charging_enabled": v2c_data.get("charging_enabled"),
            "charging_power": v2c_data.get("charging_power"),
            "charging_current": v2c_data.get("charging_current"),
        }
