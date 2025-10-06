"""Capteurs BMW iX3."""
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class BMWiX3Sensor(CoordinatorEntity, SensorEntity):
    """Capteur BMW iX3."""

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
        self._attr_unique_id = f"bmw_ix3_{key}"

    @property
    def name(self) -> str:
        """Nom du capteur."""
        return f"BMW iX3 {self._name}"

    @property
    def native_value(self) -> Any:
        """Valeur du capteur."""
        if not self.coordinator.data:
            return None
        
        bmw_data = self.coordinator.data.get("bmw", {})
        return bmw_data.get(self._key)

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
            identifiers={(DOMAIN, "bmw_ix3")},
            name="BMW iX3",
            manufacturer="BMW",
            model="iX3",
            sw_version="1.0",
        )

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Attributs supplémentaires."""
        if not self.coordinator.data:
            return {}
        
        bmw_data = self.coordinator.data.get("bmw", {})
        return {
            "last_update": bmw_data.get("last_update"),
            "charging_status": bmw_data.get("charging_status"),
            "battery_level": bmw_data.get("battery_level"),
        }
