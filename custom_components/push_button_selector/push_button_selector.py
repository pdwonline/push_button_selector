import jinja2
from homeassistant.helpers.entity import Entity
from homeassistant.core import callback
from homeassistant.components.input_select import InputSelectEntity

class PushButtonSelectorEntity(InputSelectEntity):
    def __init__(self, hass, name, options, icon=None, secondary_info_template=None, actions=None):
        self.hass = hass
        self._name = name
        self._icon_template = icon
        self._secondary_info_template = secondary_info_template
        self._options = options
        self._state = options[0] if options else None
        self._actions = actions if actions else {}

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        """Render icon based on a Jinja2 template if defined."""
        if self._icon_template:
            return self._render_template(self._icon_template)
        return None

    @property
    def state(self):
        return self._state

    @property
    def options(self):
        return self._options

    @property
    def extra_state_attributes(self):
        return {
            "secondary_info": self._render_template(self._secondary_info_template)
        }

    def _render_template(self, template_string):
        """Render a Jinja2 template."""
        if template_string:
            template = jinja2.Template(template_string)
            return template.render(self.hass.states.async_all())
        return None

    async def async_select_option(self, option):
        """Select the option and execute the action if available."""
        if option in self._options:
            self._state = option
            await self._handle_action(option)
            self.async_schedule_update_ha_state()

    async def _handle_action(self, option):
        """Handle the tap action for the selected option."""
        action = self._actions.get(option)
        if action:
            # Extract entity information and perform actions
            service = action.get("service")
            action_entity = action.get("entity")
            if service and action_entity:
                domain, service_name = service.split(".")
                service_data = {"entity_id": action_entity}
                await self.hass.services.async_call(domain, service_name, service_data)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    name = config.get("name")
    options = config.get("options")
    icon = config.get("icon")
    secondary_info = config.get("secondary_info")
    actions = config.get("actions", {})

    async_add_entities([PushButtonSelectorEntity(hass, name, options, icon, secondary_info, actions)])