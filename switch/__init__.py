"""Commutateurs pour le plugin BMW iX3."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .v2c_switch import V2CChargingSwitch
from .auto_stop_switch import AutoStopSwitch

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configuration des commutateurs."""
    coordinator = hass.data["bmw_ix3_plugin"][config_entry.entry_id]["coordinator"]
    
    switches = [
        V2CChargingSwitch(coordinator),
        AutoStopSwitch(coordinator),
    ]
    
    async_add_entities(switches)
