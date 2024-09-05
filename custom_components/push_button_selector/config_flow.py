import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from . import DOMAIN  # Make sure you have a constant `DOMAIN` in __init__.py

class PushButtonSelectorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return PushButtonSelectorOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        schema = vol.Schema({
            vol.Required("name"): str,
            vol.Required("options"): str,  # This could be a list in UI
            vol.Optional("icon", default="mdi:help-circle"): str,
            vol.Optional("secondary_info"): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema)

class PushButtonSelectorOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_options()

    async def async_step_options(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema({
            vol.Optional("tap_action_service"): str,
            vol.Optional("tap_action_entity"): str,
        })

        return self.async_show_form(step_id="options", data_schema=schema)