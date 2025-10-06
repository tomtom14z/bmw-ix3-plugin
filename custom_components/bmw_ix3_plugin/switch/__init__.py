"""Commutateurs pour le plugin BMW iX3."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import CONF_V2C_IP
from .v2c_switch import V2CChargingSwitch
from .auto_stop_switch import AutoStopSwitch

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configuration des commutateurs."""
    coordinator = hass.data["bmw_ix3_plugin"][config_entry.entry_id]["coordinator"]
    
    # Toujours ajouter l'auto-stop
    switches = [AutoStopSwitch(coordinator)]
    
    # Ajouter le switch V2C uniquement si la borne est configurée
    if config_entry.data.get(CONF_V2C_IP):
        switches.append(V2CChargingSwitch(coordinator))
    
    async_add_entities(switches)
