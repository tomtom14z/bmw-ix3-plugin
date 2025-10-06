"""Capteurs pour le plugin BMW iX3."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .bmw_sensor import BMWiX3Sensor
from .charge_calculator import ChargeTimeCalculator
from .v2c_sensor import V2CSensor

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configuration des capteurs."""
    coordinator = hass.data["bmw_ix3_plugin"][config_entry.entry_id]["coordinator"]
    
    # Capteurs BMW
    bmw_sensors = [
        BMWiX3Sensor(coordinator, "battery_level", "Niveau de batterie", "%", "mdi:battery"),
        BMWiX3Sensor(coordinator, "charging_status", "État de charge", None, "mdi:ev-station"),
        BMWiX3Sensor(coordinator, "charging_power", "Puissance de charge", "kW", "mdi:lightning-bolt"),
        BMWiX3Sensor(coordinator, "range_electric", "Autonomie électrique", "km", "mdi:map-marker-distance"),
    ]
    
    # Calculateurs de temps de charge
    charge_calculators = [
        ChargeTimeCalculator(coordinator, "charge_time_80_3_7kw", "Temps charge 80% (3.7kW)", "3.7"),
        ChargeTimeCalculator(coordinator, "charge_time_100_3_7kw", "Temps charge 100% (3.7kW)", "3.7", target_soc=100),
        ChargeTimeCalculator(coordinator, "charge_time_80_7_4kw", "Temps charge 80% (7.4kW)", "7.4"),
        ChargeTimeCalculator(coordinator, "charge_time_100_7_4kw", "Temps charge 100% (7.4kW)", "7.4", target_soc=100),
        ChargeTimeCalculator(coordinator, "charge_time_80_11kw", "Temps charge 80% (11kW)", "11"),
        ChargeTimeCalculator(coordinator, "charge_time_100_11kw", "Temps charge 100% (11kW)", "11", target_soc=100),
        ChargeTimeCalculator(coordinator, "charge_time_80_22kw", "Temps charge 80% (22kW)", "22"),
        ChargeTimeCalculator(coordinator, "charge_time_100_22kw", "Temps charge 100% (22kW)", "22", target_soc=100),
    ]
    
    # Capteurs V2C
    v2c_sensors = [
        V2CSensor(coordinator, "v2c_status", "État V2C", None, "mdi:ev-station"),
        V2CSensor(coordinator, "v2c_charging_power", "Puissance V2C", "kW", "mdi:lightning-bolt"),
        V2CSensor(coordinator, "v2c_charging_current", "Courant V2C", "A", "mdi:current-ac"),
    ]
    
    async_add_entities(bmw_sensors + charge_calculators + v2c_sensors)
