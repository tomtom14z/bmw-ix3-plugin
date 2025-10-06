"""Entité numérique pour le pourcentage de charge cible."""
import logging
from typing import Any, Dict, Optional

from homeassistant.components.number import NumberEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class TargetSOCNumber(CoordinatorEntity, NumberEntity):
    """Entité numérique pour le pourcentage de charge cible."""

    def __init__(self, coordinator) -> None:
        """Initialise l'entité numérique."""
        super().__init__(coordinator)
        self._attr_unique_id = "bmw_ix3_target_soc"
        self._attr_name = "BMW iX3 SOC cible"
        self._target_soc = 80.0  # 80% par défaut

    @property
    def native_value(self) -> float:
        """Valeur actuelle du SOC cible."""
        return self._target_soc

    @property
    def native_min_value(self) -> float:
        """Valeur minimale (50%)."""
        return 50.0

    @property
    def native_max_value(self) -> float:
        """Valeur maximale (100%)."""
        return 100.0

    @property
    def native_step(self) -> float:
        """Pas d'incrémentation (5%)."""
        return 5.0

    @property
    def native_unit_of_measurement(self) -> str:
        """Unité de mesure."""
        return "%"

    @property
    def icon(self) -> str:
        """Icône de l'entité."""
        return "mdi:battery-charging"

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

    async def async_set_native_value(self, value: float) -> None:
        """Définit le SOC cible."""
        self._target_soc = value
        _LOGGER.info("SOC cible défini à %.1f%%", value)
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Attributs supplémentaires."""
        if not self.coordinator.data:
            return {}
        
        bmw_data = self.coordinator.data.get("bmw", {})
        current_soc = bmw_data.get("battery_level", 0)
        
        return {
            "current_soc": current_soc,
            "target_soc": self._target_soc,
            "soc_difference": self._target_soc - current_soc,
            "is_target_reached": current_soc >= self._target_soc,
        }
