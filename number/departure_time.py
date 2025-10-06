"""Entité numérique pour l'heure de départ."""
import logging
from datetime import datetime, time
from typing import Any, Dict, Optional

from homeassistant.components.number import NumberEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class DepartureTimeNumber(CoordinatorEntity, NumberEntity):
    """Entité numérique pour l'heure de départ."""

    def __init__(self, coordinator) -> None:
        """Initialise l'entité numérique."""
        super().__init__(coordinator)
        self._attr_unique_id = "bmw_ix3_departure_time"
        self._attr_name = "BMW iX3 Heure de départ"
        self._departure_hour = 8  # 8h00 par défaut
        self._departure_minute = 0

    @property
    def native_value(self) -> float:
        """Valeur actuelle (heure en format décimal)."""
        return self._departure_hour + self._departure_minute / 60.0

    @property
    def native_min_value(self) -> float:
        """Valeur minimale (0h00)."""
        return 0.0

    @property
    def native_max_value(self) -> float:
        """Valeur maximale (23h59)."""
        return 23.99

    @property
    def native_step(self) -> float:
        """Pas d'incrémentation (15 minutes)."""
        return 0.25

    @property
    def native_unit_of_measurement(self) -> str:
        """Unité de mesure."""
        return "h"

    @property
    def icon(self) -> str:
        """Icône de l'entité."""
        return "mdi:clock-outline"

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
        """Définit l'heure de départ."""
        self._departure_hour = int(value)
        self._departure_minute = int((value - self._departure_hour) * 60)
        
        _LOGGER.info("Heure de départ définie à %02d:%02d", self._departure_hour, self._departure_minute)
        
        # Calculer l'heure de début de charge optimale
        await self._calculate_optimal_start_time()
        
        self.async_write_ha_state()

    async def _calculate_optimal_start_time(self) -> None:
        """Calcule l'heure de début de charge optimale."""
        if not self.coordinator.data:
            return
        
        bmw_data = self.coordinator.data.get("bmw", {})
        current_soc = bmw_data.get("battery_level", 0)
        charging_power = bmw_data.get("charging_power", 7.4)
        
        # Calcul du temps de charge nécessaire (simplifié)
        # À améliorer avec les vrais calculs de temps de charge
        target_soc = 80  # Par défaut 80%
        energy_needed = (target_soc - current_soc) / 100.0 * 80.0  # 80kWh de capacité
        charge_time_hours = energy_needed / charging_power
        
        # Calcul de l'heure de début
        departure_time = time(self._departure_hour, self._departure_minute)
        departure_datetime = datetime.combine(datetime.now().date(), departure_time)
        
        # Si l'heure de départ est dans le passé, prendre le lendemain
        if departure_datetime <= datetime.now():
            departure_datetime = departure_datetime.replace(day=departure_datetime.day + 1)
        
        start_datetime = departure_datetime - datetime.timedelta(hours=charge_time_hours)
        
        _LOGGER.info("Heure de début de charge optimale: %s", start_datetime.strftime("%H:%M"))

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Attributs supplémentaires."""
        departure_time_str = f"{self._departure_hour:02d}:{self._departure_minute:02d}"
        
        return {
            "departure_time_formatted": departure_time_str,
            "departure_hour": self._departure_hour,
            "departure_minute": self._departure_minute,
        }
