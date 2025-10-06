"""Configuration flow pour le plugin BMW iX3."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_BMW_USERNAME,
    CONF_BMW_PASSWORD,
    CONF_V2C_IP,
    CONF_V2C_USERNAME,
    CONF_V2C_PASSWORD,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_BMW_USERNAME): str,
        vol.Required(CONF_BMW_PASSWORD): str,
        vol.Optional(CONF_V2C_IP, default=""): str,
        vol.Optional(CONF_V2C_USERNAME, default="admin"): str,
        vol.Optional(CONF_V2C_PASSWORD, default=""): str,
    }
)


class BMWiX3ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gestionnaire de configuration pour BMW iX3."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Étape de configuration utilisateur."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            # Validation des données
            try:
                # Test de connexion BMW (simulation)
                await self._test_bmw_connection(
                    user_input[CONF_BMW_USERNAME],
                    user_input[CONF_BMW_PASSWORD]
                )
                
                # Test de connexion V2C uniquement si IP fournie
                if user_input.get(CONF_V2C_IP):
                    await self._test_v2c_connection(
                        user_input[CONF_V2C_IP],
                        user_input.get(CONF_V2C_USERNAME, "admin"),
                        user_input.get(CONF_V2C_PASSWORD, "")
                    )
                    _LOGGER.info("Configuration V2C activée")
                else:
                    _LOGGER.info("Configuration V2C non activée (sera disponible ultérieurement)")

                return self.async_create_entry(
                    title="BMW iX3 Plugin",
                    data=user_input,
                )
            except Exception as err:
                _LOGGER.error("Erreur de configuration: %s", err)
                errors["base"] = "connection_error"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def _test_bmw_connection(self, username: str, password: str) -> bool:
        """Test de connexion à l'API BMW."""
        # Simulation - à remplacer par un vrai test d'API
        _LOGGER.info("Test de connexion BMW pour %s", username)
        return True

    async def _test_v2c_connection(self, ip: str, username: str, password: str) -> bool:
        """Test de connexion à la borne V2C."""
        # Simulation - à remplacer par un vrai test de connexion
        _LOGGER.info("Test de connexion V2C à %s", ip)
        return True

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Retourne le gestionnaire d'options."""
        return BMWiX3OptionsFlowHandler(config_entry)


class BMWiX3OptionsFlowHandler(config_entries.OptionsFlow):
    """Gestionnaire d'options pour BMW iX3."""

    def __init__(self, config_entry):
        """Initialise le gestionnaire d'options."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Gestion des options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional("update_interval", default=300): vol.All(
                    vol.Coerce(int), vol.Range(min=60, max=3600)
                ),
                vol.Optional("auto_stop_at_80", default=True): bool,
                vol.Optional("target_soc", default=80): vol.All(
                    vol.Coerce(int), vol.Range(min=50, max=100)
                ),
            }),
        )
