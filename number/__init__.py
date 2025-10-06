"""Entités numériques pour le plugin BMW iX3."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .departure_time import DepartureTimeNumber
from .target_soc import TargetSOCNumber

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configuration des entités numériques."""
    coordinator = hass.data["bmw_ix3_plugin"][config_entry.entry_id]["coordinator"]
    
    numbers = [
        DepartureTimeNumber(coordinator),
        TargetSOCNumber(coordinator),
    ]
    
    async_add_entities(numbers)
