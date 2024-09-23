from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from . import DOMAIN

class UfanetDoorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Ufanet Door", data=user_input)

        data_schema = vol.Schema({
            vol.Required("login"): str,
            vol.Required("password"): str,
            vol.Required("domf_id"): int,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
