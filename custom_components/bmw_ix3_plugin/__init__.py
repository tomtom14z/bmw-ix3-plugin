"""BMW iX3 Plugin pour Home Assistant."""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import BMWiX3Coordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Configuration du plugin BMW iX3."""
    _LOGGER.info("Initialisation du plugin BMW iX3")
    return True


async def async_setup_entry(hass: HomeAssistant, entry):
    """Configuration d'une entrée du plugin."""
    hass.data.setdefault(DOMAIN, {})
    
    # Création du coordinateur
    coordinator = BMWiX3Coordinator(hass, entry.data, entry.entry_id)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
    }
    
    # Configuration des composants
    await hass.config_entries.async_forward_entry_setups(
        entry, ["sensor", "switch", "number"]
    )
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry):
    """Déchargement d'une entrée du plugin."""
    # Arrêt du coordinateur
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    await coordinator.async_shutdown()
    
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, ["sensor", "switch", "number"]
    )
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
