import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_NAME, CONF_OPTIONS, CONF_ICON, CONF_INITIAL_VALUE, CONF_SECONDARY_INFO

# Dit wordt gebruikt om de invoer van de gebruiker te valideren
CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): str,
    vol.Required(CONF_OPTIONS): vol.All(vol.Length(min=1), [str]),
    vol.Optional(CONF_ICON, default="mdi:help-circle"): str,
    vol.Optional(CONF_INITIAL_VALUE): str,
    vol.Optional(CONF_SECONDARY_INFO): str,
})

class PushButtonSelectorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Push Button Selector component."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step of the config flow."""
        if user_input is not None:
            # Als de gebruiker gegevens invoert, valideren we deze en slaan we de configuratie op
            return self.async_create_entry(title=user_input["name"], data=user_input)

        # Geen invoer, toon het formulier aan de gebruiker
        return self.async_show_form(step_id="user", data_schema=CONFIG_SCHEMA)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Define the options flow."""
        return PushButtonSelectorOptionsFlow(config_entry)


class PushButtonSelectorOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Push Button Selector."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options for the Push Button Selector."""
        if user_input is not None:
            # Verwerk de opties die zijn ingevoerd
            return self.async_create_entry(title="", data=user_input)

        # Als er geen invoer is, tonen we het optiesformulier
        options_schema = vol.Schema({
            vol.Optional("tap_action_service"): str,
            vol.Optional("tap_action_entity"): str,
        })

        return self.async_show_form(step_id="init", data_schema=options_schema)