"""Calculateur de temps de charge pour BMW iX3."""
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import (
    DOMAIN,
    BATTERY_CAPACITY,
    CHARGE_EFFICIENCY,
    FAST_CHARGE_THRESHOLD,
    SLOW_CHARGE_FACTOR,
)

_LOGGER = logging.getLogger(__name__)


class ChargeTimeCalculator(CoordinatorEntity, SensorEntity):
    """Calculateur de temps de charge."""

    def __init__(
        self,
        coordinator,
        key: str,
        name: str,
        power_kw: str,
        target_soc: int = 80,
    ) -> None:
        """Initialise le calculateur."""
        super().__init__(coordinator)
        self._key = key
        self._name = name
        self._power_kw = float(power_kw)
        self._target_soc = target_soc
        self._attr_unique_id = f"bmw_ix3_{key}"

    @property
    def name(self) -> str:
        """Nom du capteur."""
        return f"BMW iX3 {self._name}"

    @property
    def native_value(self) -> Optional[float]:
        """Temps de charge calculé en minutes."""
        if not self.coordinator.data:
            return None
        
        bmw_data = self.coordinator.data.get("bmw", {})
        current_soc = bmw_data.get("battery_level")
        
        if current_soc is None:
            return None
        
        return self._calculate_charge_time(current_soc, self._target_soc, self._power_kw)

    @property
    def native_unit_of_measurement(self) -> str:
        """Unité de mesure."""
        return "min"

    @property
    def icon(self) -> str:
        """Icône du capteur."""
        return "mdi:timer"

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
        current_soc = bmw_data.get("battery_level")
        
        if current_soc is None:
            return {}
        
        charge_time = self._calculate_charge_time(current_soc, self._target_soc, self._power_kw)
        
        if charge_time is None:
            return {}
        
        # Calcul de l'heure d'atteinte du pourcentage cible
        now = datetime.now()
        target_time = now + timedelta(minutes=charge_time)
        
        return {
            "current_soc": current_soc,
            "target_soc": self._target_soc,
            "power_kw": self._power_kw,
            "target_time": target_time.isoformat(),
            "target_time_formatted": target_time.strftime("%H:%M"),
            "battery_capacity_kwh": BATTERY_CAPACITY,
        }

    def _calculate_charge_time(self, current_soc: float, target_soc: float, power_kw: float) -> Optional[float]:
        """Calcule le temps de charge en minutes."""
        if current_soc >= target_soc:
            return 0.0
        
        # Calcul de l'énergie nécessaire (kWh)
        energy_needed = (target_soc - current_soc) / 100.0 * BATTERY_CAPACITY
        
        # Prise en compte de l'efficacité de charge
        energy_needed = energy_needed / CHARGE_EFFICIENCY
        
        # Calcul du temps de charge
        if target_soc <= FAST_CHARGE_THRESHOLD:
            # Charge rapide jusqu'à 80%
            charge_time_hours = energy_needed / power_kw
        else:
            # Charge mixte : rapide jusqu'à 80%, puis lente
            energy_to_80 = (FAST_CHARGE_THRESHOLD - current_soc) / 100.0 * BATTERY_CAPACITY / CHARGE_EFFICIENCY
            energy_above_80 = (target_soc - FAST_CHARGE_THRESHOLD) / 100.0 * BATTERY_CAPACITY / CHARGE_EFFICIENCY
            
            time_to_80 = energy_to_80 / power_kw if current_soc < FAST_CHARGE_THRESHOLD else 0
            time_above_80 = energy_above_80 / (power_kw * SLOW_CHARGE_FACTOR)
            
            charge_time_hours = time_to_80 + time_above_80
        
        return charge_time_hours * 60  # Conversion en minutes
